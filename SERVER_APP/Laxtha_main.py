# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Slot, QEvent
from mainwindow import Ui_MainWindow
import pyqtgraph as pg
from receive_worker import ReceiveWorker
from send_worker import SendWorker
from datetime import datetime
import serial.tools.list_ports
import queue
import time
import os

class MainWindow(QMainWindow, Ui_MainWindow):
    _MAX_X_AXIS = 2048  # ch1, ch2의 최대 X값
    _battery_percent = 0
    _mode = ""
    _receive_worker = None
    _send_worker = None
    _send_queue = queue.SimpleQueue()  # 다른 App으로 발송을 위한 Send Queue

    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # signal 등록
        self.button1.clicked.connect(self.connect)

        # send worker
        self._send_worker = SendWorker(self, self._send_queue)
        self._send_worker.start()

        # port 목록
        self.port_combobox.installEventFilter(self)

        # 그래프 그리기(CH1)7
        self.graph_ch1 = pg.PlotWidget(title="좌뇌(uV)")
        # self.graph_ch1.disableAutoRange()
        # self.graph_ch1.setLimits(yMin=-300, yMax=300)
        self.graph_ch1.enableAutoRange(axis="y")
        self.graph_ch1.setXRange(1, self._MAX_X_AXIS)
        # self.graph_ch1.setYRange(-300, 300)
        self.graph_ch1.plotItem.setMouseEnabled(x=False, y=False)
        self.ch1_plot = self.graph_ch1.plot(pen='g')

        self.ch1_x = []
        self.ch1_y = []
        self.graph_1_layout.addWidget(self.graph_ch1)

        # 그래프 그리기(CH2)
        self.graph_ch2 = pg.PlotWidget(title="우뇌(uV)")
        # self.graph_ch2.disableAutoRange()
        # self.graph_ch2.setLimits(yMin=-300, yMax=300)
        self.graph_ch2.enableAutoRange(axis="y")
        self.graph_ch2.setXRange(1, self._MAX_X_AXIS)
        # self.graph_ch2.setYRange(-300, 300)
        self.graph_ch2.plotItem.setMouseEnabled(x=False, y=False)
        self.ch2_plot = self.graph_ch2.plot(pen='g')

        self.ch2_x = []
        self.ch2_y = []
        self.graph_2_layout.addWidget(self.graph_ch2)

        # 그래프 그리기(ch4-ppg)
        self.graph_ppg = pg.PlotWidget(title="PPG(au)")
        self.graph_ppg.enableAutoRange(axis="y")
        # self.graph_ch2.setLimits(yMin=-300, yMax=300)
        self.graph_ppg.setXRange(1, self._MAX_X_AXIS)
        # self.graph_ch2.setYRange(-300, 300)
        self.graph_ppg.plotItem.setMouseEnabled(x=False, y=False)
        self.ppg_plot = self.graph_ppg.plot(pen='y')

        self.ppg_x = []
        self.ppg_y = []
        self.graph_ppg_layout.addWidget(self.graph_ppg)

        # 그래프 그리기 (ch3-sepctrum)
        self.graph_spectrum = pg.PlotWidget(title="Power Spectrum")
        self.graph_spectrum.enableAutoRange(axis="y")
        self.graph_spectrum.setXRange(0, 80)
        self.graph_spectrum.plotItem.setMouseEnabled(x=False, y=False)
        self.spectrum_plot = self.graph_spectrum.plot(pen='w')

        self.spectrum_x = [n for n in range(0, 80 + 1)]
        self.spectrum_y = [0 for n in range(0, 80 + 1)]

        self.graph_spectrum_layout.addWidget(self.graph_spectrum)
        #os.system('python Nf_server_app.py')

    def init_status_label(self):
        self.ch1_status.setStyleSheet("background-color: red;")
        self.ch2_status.setStyleSheet("background-color: red;")
        self.ref_status.setStyleSheet("background-color: red;")

    @Slot(dict)
    def update_data(self, data_dict: dict):
        # print(f"update graph:{data_dict}")

        if data_dict["mode"] != "측정모드":  # 대기모드 or 충전모드 일때
            self._battery_percent = self._battery_percent if data_dict['battery_status'] == None else data_dict[
                'battery_status']
            self._mode = data_dict['mode']
            self.battery.setText(str(self._battery_percent) + "%")
            self.mode.setText(self._mode)
            self.init_status_label()
            return

        # CH1, CH2, ppg 부착상태
        if data_dict["ch1_status"] > 0:
            self.ch1_status.setStyleSheet("background-color: green;")
        else:
            self.ch1_status.setStyleSheet("background-color: red;")

        if data_dict["ch2_status"] > 0:
            self.ch2_status.setStyleSheet("background-color: green;")
        else:
            self.ch2_status.setStyleSheet("background-color: red;")

        if data_dict["ref_status"] > 0:
            self.ref_status.setStyleSheet("background-color: green;")
        else:
            self.ref_status.setStyleSheet("background-color: red;")

        # 배터리, 모드 상태
        self._battery_percent = self._battery_percent if data_dict['battery_status'] == None else data_dict[
            'battery_status']
        self._mode = data_dict['mode']
        self.battery.setText(str(self._battery_percent) + "%")
        self.mode.setText(self._mode)

        # 그래프 출력 (CH1)
        if len(self.ch1_x) == self._MAX_X_AXIS:
            self.ch1_x = []
            self.ch1_y = []

        last_x = 0 if len(self.ch1_x) == 0 else self.ch1_x[-1] + 1
        self.ch1_x.append(last_x)
        self.ch1_y.append(int(data_dict["ch1"]))
        self.ch1_plot.setData(self.ch1_x, self.ch1_y)

        # 그래프 출력 (CH2)
        if len(self.ch2_x) == self._MAX_X_AXIS:
            self.ch2_x = []
            self.ch2_y = []

        last_x = 0 if len(self.ch2_x) == 0 else self.ch2_x[-1] + 1
        self.ch2_x.append(last_x)
        self.ch2_y.append(int(data_dict["ch2"]))
        self.ch2_plot.setData(self.ch2_x, self.ch2_y)

        # 그래프 출력 (ch4-PPG)
        if len(self.ppg_x) == self._MAX_X_AXIS:
            self.ppg_x = []
            self.ppg_y = []

        last_x = 0 if len(self.ppg_x) == 0 else self.ppg_x[-1] + 1
        self.ppg_x.append(last_x)
        self.ppg_y.append(int(data_dict["ch4"]))
        self.ppg_plot.setData(self.ppg_x, self.ppg_y)

        # 그래프 출력 (Spectrum)
        if (data_dict['ch3'] is not None) and (data_dict['ch3_n'] <= 80):
            self.spectrum_y[data_dict['ch3_n']] = data_dict['ch3']
            self.spectrum_plot.setData(self.spectrum_x, self.spectrum_y)

    def closeEvent(self, e):
        print("close event()")
        self.hide()
        self._receive_worker.stop()
        time.sleep(2)

    def eventFilter(self, target, event):
        if target == self.port_combobox and event.type() == QEvent.MouseButtonPress:
            self.fillComboBox()

        return False

    def fillComboBox(self):
        self.port_combobox.clear()
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
            if hwid.startswith("BTHENUM"):  # 블루투스 장치만 출력
                self.port_combobox.addItem(port)

    @Slot(str)
    def add_log(self, log_str):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.info.appendPlainText(f"[{now}] {log_str}")

    def disconnect(self):
        self.button1.setText("기기연결")
        self.add_log("기기 연결 종료!")
        self.mode.setText("연결대기")
        self.battery.setText("??%")
        self.init_status_label()

    @Slot(int)
    def update_send_queue_count(self, count):

        self.send_queue_size.setText("Queue:" + str(count))

    def connect(self):
        if self.button1.text() == "연결종료":
            self.disconnect()
            self._receive_worker.stop()
            return

        if self.button1.text() == "연결중..":
            return

        port = str(self.port_combobox.currentText())
        if port == "":
            self.add_log("com port를 선택하세요.")
            return

        # 리시브 쓰레드 시작
        self._receive_worker = ReceiveWorker(self, port, self._send_queue)
        self._receive_worker.start()


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()

    app.exec()


