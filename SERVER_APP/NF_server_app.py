import rpyc
import numpy as np
from datetime import datetime
import time
import random

class RecvService(rpyc.Service):
    # exposed_data_storage = np.zeros((5, 5000))
    
    now = datetime.now()
    current_time = now.strftime("%y-%m-%d-%H-%M-%S");
    #fn = current_time + '.txt';

    # 파일생성방지 61번줄 참고
    # file_temp = open(fn, 'w')
    
    def __init__(self):
        print("수신 프로그램 초기화")
        self.exposed_data_storage = np.zeros((5, 5000))
        
    def on_connect(self, conn):
        # code that runs when a connection is created
        # (to init the service, if needed)
        print("송신 프로그램 연결 완료")
        pass

    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        # self.file_temp.close()
        
        pass

    def exposed_recv_data(self, data_list):
        # data 변수 예
        '''
                    0          1                2                3             4            5            6            7               8                 9                   10                  11              12                                                       13                 14                                                      
        {'mode': '측정모드', 'ch1': -5.01234, 'ch2': -45.14712, 'ch3': 0.0, 'ch3_n': 295, 'ch4': 16238, 'ch5': -3888, 'ch6': 0, 'ch1_status': 32, 'ch2_status': 16, 'ref_status': 8, 'battery_status': None, 'org_packet': 'fffe016206ff783e3f753b1c00003f6e30d00000', 'packet_count': 6, 'timestamp': 1655271402.7795827}
        {'mode': '측정모드', 'ch1': -5.30082, 'ch2': -47.92374, 'ch3': 0.0, 'ch3_n': 296, 'ch4': 16238, 'ch5': -3393, 'ch6': 0, 'ch1_status': 32, 'ch2_status': 16, 'ref_status': 8, 'battery_status': None, 'org_packet': 'fffe016207ffa93e3f6d3acf00003f6e32bf0000', 'packet_count': 7, 'timestamp': 1655271402.7805839}
        {'mode': '측정모드', 'ch1': 0.10818, 'ch2': -43.19988, 'ch3': 0.0, 'ch3_n': 297, 'ch4': 16240, 'ch5': -2789, 'ch6': 0, 'ch1_status': 32, 'ch2_status': 16, 'ref_status': 8, 'battery_status': None, 'org_packet': 'fffe016208ffa93e40033b5200003f70351b0000', 'packet_count': 8, 'timestamp': 1655271402.781586}
        '''

        # for i in range(chunklength):
           
        #     data = data_list[i];
        #     self.exposed_data_storage = np.roll(self.exposed_data_storage, -1)
        #     self.exposed_data_storage[0][-1] = data['ch1']
        #     self.exposed_data_storage[1][-1] = data['ch2']
        #     self.exposed_data_storage[2][-1] = data['ch4']
        #     self.exposed_data_storage[3][-1] = data['packet_count']
        #     self.exposed_data_storage[4][-1] = data['timestamp']

        # 게임으로 전송되는 데이터의 양식. 5 by 5000의 데이터가 지속적으로 전송된다.
        self.exposed_data_storage = np.roll(self.exposed_data_storage, -1)
        self.exposed_data_storage[0][-1] = round(data_list['ch1'], 2)  # 좌측 채널 데이터 전송
        self.exposed_data_storage[1][-1] = round(data_list['ch2'], 2)  # 우측 채널 데이터 전송
        self.exposed_data_storage[2][-1] = round(data_list['ch4'], 2)  # PPG 데이터 전송
        self.exposed_data_storage[3][-1] = data_list['packet_count']  # 패킷관련 데이터
        self.exposed_data_storage[4][-1] = round(data_list['timestamp'], 3)   # 측정 timestamp 전송.
                                                                    # Game 단위에서 receive할 때의
                                                                    # timestamp는 별도로 기록 해야 할 듯.
                                                                    # ms보다 작은 단위를 버리기 위해 round함.
        # print(round(data_list['ch1'],3))
        # 파일생성방지. 파일은 게임차원에서 받도록 바꿀예정.
        # self.file_temp.write(str(data_list).strip('{').strip('}') + '\n');

# Activating Server
if __name__ == "__main__":
    t = rpyc.utils.server.ThreadedServer(RecvService(), port=18861, protocol_config={
    'allow_all_attrs': True, 'allow_pickle': True
    })
    t.start()
    
    


