from pyModbusTCP.client import ModbusClient
import pandas as pd
import time
from datetime import datetime
import os



class DataLogger:
    '''
    
    '''
    def __init__(self, save_folder: str, tag_map: dict=None, log_freq: float=1.0) -> None:
        # Absolute path to log save location
        self.save_folder = save_folder

        # Dictionary map of tag locations and scaling
        self.tag_map = tag_map

        # Time between Modbus requests (seconds)
        self.log_freq = log_freq

        # Currently loaded data
        self.log = pd.DataFrame()
    
    def logRegisters(self) -> None:
        # Get the current time 
        t = datetime.now()

        # Append the data to the active log 
        self.log = pd.concat([self.log, self.readAllRegisters()], axis=0)

    def connect(self, ip: str, port: int, unit_id: int=1) -> ModbusClient:
        try:
            self.client = ModbusClient(host=ip, port=port, unit_id=unit_id, auto_open=True, auto_close=False) 
            return self.client
        except:
            raise Exception('Failed to connect')
    
    def readAllRegisters(self) -> None:
        regs = self.client.read_holding_registers(0, len(self.tag_map))
        if regs is not None:
            return pd.DataFrame([regs], index=[datetime.now()])
        else:
            raise Exception('Failed to read registers')
        
    def isConnected(self) -> bool:
        return self.client.is_open



'''
- List index corresponds to holding register index
- Each index has the tag name and scaling that needs to be applied

tag_map = [
    {tag: 'Inlet Purity', scaling: 0.01},
    {tag: 'Outlet Purity', scaling: 0.01}
]
'''



if __name__ == '__main__':

    # Settings
    poll_time = 1
    plc_ip = "192.168.0.1"
    csv_path = "Logs/ModbusTestLog.csv"

    logger = DataLogger(csv_path, tag_map=[0 for _ in range(50)])
    logger.connect(plc_ip, 503, 2)

    # Try 2 logging cycles and print result
    logger.logRegisters()
    time.sleep(1)
    logger.logRegisters()
    print(logger.log)

    # Dump csv
    print(logger.log.to_csv('C:\\Users\\Quantum\\Desktop\\Data Log Visualization\\test.csv'))

    # response = os.system("ping " + plc_ip)
    # print('Response: ' + str(response))

    # # TCP auto connect on first modbus request
    # c = ModbusClient(host=plc_ip, port=503, unit_id=2, auto_open=True, auto_close=False)
    # print(c.open())

    # while 1:
    #     # Read several registers 
    #     regs = c.read_holding_registers(28, 3)

    #     # Open csv to append value 
    #     # with open(csv_path, 'a') as f:
    #     #     f.write(regs)

    #     # Display the read values 
    #     print('\n')
    #     print(regs)
    #     print('\n')

    #     # Wait for logging frequency
    #     time.sleep(poll_time)



