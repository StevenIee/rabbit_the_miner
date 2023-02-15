import serial
from PySide6.QtCore import QThread, Signal
import time


def byte_to_bit_array(byte_data):
    return [int(i) for i in "{0:08b}".format(0x00)]


# testBit() returns a nonzero result, 2**offset, if the bit at 'offset' is one.

def testBit(int_type, offset):
    mask = 1 << offset
    return (int_type & mask)


# setBit() returns an integer with the bit at 'offset' set to 1.

def setBit(int_type, offset):
    mask = 1 << offset
    return (int_type | mask)


# clearBit() returns an integer with the bit at 'offset' cleared.

def clearBit(int_type, offset):
    mask = ~(1 << offset)
    return (int_type & mask)


# toggleBit() returns an integer with the bit at 'offset' inverted, 0 -> 1 and 1 -> 0.

def toggleBit(int_type, offset):
    mask = 1 << offset
    return (int_type ^ mask)


# 기기에서 전송된 패킷(바이트)를 분석/사용하기 위한 클래스
class Packet:
    org_packet = None

    def __init__(self, packet: bytes):
        self.org_packet = bytearray(packet)

    # 현재 기기 실행 모드
    def get_mode(self):
        # 0=대기모드, 1=실행(측정)모드, 2=충전모드
        if self.org_packet[2] == 0x00:
            return "대기모드"
        if self.org_packet[2] == 0x01:
            return "측정모드"
        if self.org_packet[2] == 0x02:
            return "충전모드"

    def is_init_powerspectrum(self):
        # Power Spectrum 의 2초 단위 개시시점일때 ch3_n 초기화
        if testBit(self.org_packet[3], 0) == 1:
            return True
        else:
            return False

    def packet_count(self):
        return self.org_packet[4]

    # CH1(좌뇌) 데이터 값
    def get_ch1_value(self):
        high_value = clearBit(self.org_packet[8], 7)
        low_value = self.org_packet[9]
        return ((256 * high_value + low_value) - 16384) * 0.03606

    # CH2(우뇌) 데이터 값
    def get_ch2_value(self):
        high_value = clearBit(self.org_packet[10], 7)
        low_value = self.org_packet[11]
        return ((256 * high_value + low_value) - 16384) * 0.03606

    # CH3(Power Spectrum) 데이터 값
    def get_ch3_value(self):
        high_value = clearBit(self.org_packet[12], 7)
        low_value = self.org_packet[13]
        return (256 * high_value + low_value) / 10

    # CH4 (맥파(ppg)) 데이터 값
    def get_ch4_value(self):
        high_value = clearBit(self.org_packet[14], 7)
        low_value = self.org_packet[15]

        return 256 * high_value + low_value

    # CH5 (이차미분 맥파(sdPPG)) 데이터 값
    def get_ch5_value(self):
        high_value = clearBit(self.org_packet[16], 7)
        low_value = self.org_packet[17]
        return 256 * high_value + low_value

    # CH6 (peak-interval(심박간격 데이터)) 데이터 값
    def get_ch6_value(self):
        high_value = clearBit(self.org_packet[18], 7)
        low_value = self.org_packet[19]
        return 256 * high_value + low_value

    # CH1 전극 부착상태
    def get_ch1_status(self):
        return testBit(self.org_packet[7], 5)

    # CH2 전극 부착상태7
    def get_ch2_status(self):
        return testBit(self.org_packet[7], 4)

    # REF 전극 부착상태
    def get_ref_status(self):
        return testBit(self.org_packet[7], 3)

    # 배터리 상태
    def get_battery_status(self):
        if self.get_mode() == "측정모드":
            if (self.org_packet[4] == 1):
                return self.org_packet[6]
            else:
                return None
        elif self.get_mode() == "대기모드" or self.get_mode() == "충전모드":
            return self.org_packet[5]


# 기기에 접속하여 데이터 수신하는 쓰레드
class ReceiveWorker(QThread):
    parent = None
    is_running = True
    data_signal = Signal(dict)  # 수신된 데이터 Signal
    log_signal = Signal(str)  # MainWindow에 로그 전달 Singal
    queue_count_signal = Signal(int)  # MainWindow에 SendQueue 카운트 전달 Signal
    ch3_n = 0  # ch3(power_spectrum)의 n 값

    _send_queue = None

    def __init__(self, parent, port, send_queue):
        self.parent = parent
        self._send_queue = send_queue

        super().__init__(parent)

        # 시그널 / 슬롯 등록
        self.data_signal.connect(parent.update_data)
        self.log_signal.connect(parent.add_log)
        self.queue_count_signal.connect(parent.update_send_queue_count)

        # 시리얼 연결 정보 초기화
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = 115200
        self.ser.timeout = 3
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.parity = serial.PARITY_NONE

    def init_ch3_n(self):
        self.ch3_n = 0

    def run(self):

        self.connect_serial()

        while self.is_running:
            self.queue_count_signal.emit(self._send_queue.qsize())  # 현재 SendQueue의 카운트를 MainWindow에 전달

            sync_byte = self.ser.read(1)  # 첫번째 byte가 0xff, 두번째 byte가 0xfe 이여야 정상정진 패킷으로 판단함
            if sync_byte == b'\xff':
                sync_byte = self.ser.read(1)
                if sync_byte == b'\xfe':
                    body_packet = self.ser.read(18)
                    packet = Packet(b'\xff\xfe' + body_packet)

                    if packet.is_init_powerspectrum():  # Power Spectrum의 n값을 초기화
                        self.ch3_n = 0

                    if packet.get_mode() == "측정모드":  # 측정모드 일때
                        # ch1(좌뇌)/ch2(우뇌) 데이터, 맥박 데이터
                        data = {
                            "mode": packet.get_mode(),  # 실행모드
                            "ch1": packet.get_ch1_value(),  # 좌뇌(CH1)
                            "ch2": packet.get_ch2_value(),  # 우뇌(CH2)
                            "ch3": packet.get_ch3_value(),  # Power Spectrum
                            "ch3_n": self.ch3_n,  # Power Spectrum N value
                            "ch4": packet.get_ch4_value(),  # CH4(맥파(ppg))
                            "ch5": packet.get_ch5_value(),  # CH5(이차미분맥파)
                            "ch6": packet.get_ch6_value(),  # CH6(peak-interavl)
                            "ch1_status": packet.get_ch1_status(),  # CH1 부착상태
                            "ch2_status": packet.get_ch2_status(),  # CH2 부착상태
                            "ref_status": packet.get_ref_status(),  # 귓볼 부착상태
                            "battery_status": packet.get_battery_status(),  # 배터리 상태
                            "org_packet": packet.org_packet.hex(),  # Packet 분석 전 origianl 패킷bytes
                            "packet_count": packet.packet_count(),  # Packet Cyclic Count
                            "timestamp": time.time(),  # timestamp
                        }
                        self.data_signal.emit(data)
                        self.ch3_n += 1
                        self._send_queue.put(data)

                    else:  # 대기, 충전모드 일때
                        data = {
                            "mode": packet.get_mode(),
                            "org_packet": packet.org_packet.hex(),
                            "battery_status": packet.get_battery_status(),
                        }

                        self.log_signal.emit(f"현재 {packet.get_mode()} 입니다..")
                        self.data_signal.emit(data)
            else:
                print(f"잘못된 패킷:{sync_byte}")
                if sync_byte == b'':
                    self.log_signal.emit(f"잘못된 패킷으로 연결을 종료합니다.")
                    self.parent.disconnect()
                    self.is_running = False
                    
        print("ReceiveWorker 쓰레드 종료")

    def connect_serial(self):
        self.log_signal.emit(f"{self.ser.port}에 연결 시도 중...")
        try:
            self.parent.button1.setText("연결중..")
            self.ser.open()
            self.log_signal.emit(f"{self.ser.port} 연결 완료!!")
            self.parent.button1.setText("연결종료")
        except Exception as e:
            self.log_signal.emit(f"{str(e)}")
            self.parent.button1.setText("기기연결")

    def stop(self):
        self.is_running = False
        self.ser.close()
