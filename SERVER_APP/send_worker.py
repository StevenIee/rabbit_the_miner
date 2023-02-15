from PySide6.QtCore import QThread, Signal
import time
import rpyc


# rPyc 라이브러릴 사용하여, 데이터를 외부 프로세스에 전달한다.
class SendWorker(QThread):
    parent = None
    rpy = None
    is_running = True
    _send_queue = None

    log_signal = Signal(str)

    def __init__(self, parent, send_queue):
        self.parent = parent
        super().__init__()
        self._send_queue = send_queue

        # signal 등록
        self.log_signal.connect(parent.add_log)

    # 수신받는 프로그램에 연결 처리
    def connect_server(self):
        while True:
            try:

                self.rpy = rpyc.connect("localhost", 18861, config ={'allow_all_attrs': True, 'allow_pickle':True})
                self.log_signal.emit("수신 프로그램 연결 완료")
                break
            except Exception as e:
                self.log_signal.emit("수신 프로그램 연결 오류!! - 수신프로그램이 실행되어 있는지 확인하세요.")
                time.sleep(2)

    def run(self):
        self.connect_server()
        while True:

            if self._send_queue.empty():  # SendQueue에 데이터가 없을때 잠시 Sleep
                time.sleep(0.1)
                continue

            # data_list = []
            # while not self._send_queue.empty():
            #     data = self._send_queue.get_nowait()
            #     data_list.append(data)
            #     if len(data_list) > 500:
            #         break
         
            data_list = self._send_queue.get_nowait()
            try:
                self.rpy.root.recv_data(data_list)  # 수신받는 프로그램으로 전송(rpyc 라이브러리)
            except EOFError as e:
                print(str(e))
                self.log_signal.emit("수신 프로그램 연결 오류로 재연결 합니다.")
                self.connect_server()
                self.rpy.root.recv_data(data_list)
            except Exception as e:
                print(str(e))
                self.log_signal.emit("수신 프로그램 에서 알수 없는 오류 발생")

        print("SendWorker 쓰레드 종료")

    def stop(self):
        self.is_running = False
        self.rpy.close()
