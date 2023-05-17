from pyModbusTCP.client import ModbusClient
import pandas as pd
import time
from datetime import datetime
import os



'''
Tag Map

- List index corresponds to holding register index
- Each index has the tag name and scaling that needs to be applied

tag_map = [
    {tag: 'Inlet Purity', scaling: 0.01},
    {tag: 'Outlet Purity', scaling: 0.01}
]
'''


class ModbusLogger:
    '''
    Class for handling connection to Modbus server and caching a log
    log_path: str = Absolute path to CSV log location
    tag_map: str = Mapping modbus registers to tag names and scaling
    log_freq: float = Time between modbus calls
    '''
    def __init__(self, log_path: str=None, tag_map: list=None, log_freq: float=1.0) -> None:
        # Absolute path to log save location
        self.log_path = log_path

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

    def connect(self, ip: str='192.168.0.1', port: int=503, unit_id: int=2) -> ModbusClient:
        # Tries to initialize a connection to a Modbus server 
        try:
            self.client = ModbusClient(host=ip, port=port, unit_id=unit_id, auto_open=True, auto_close=False) 
            return self.client
        except:
            raise Exception('Failed to connect')
    
    def readAllRegisters(self) -> pd.DataFrame:
        # Read all registers
        regs = self.client.read_holding_registers(0, len(self.tag_map))

        # Check if the read was succesful
        # If success return a dataframe with the read time as the index
        if regs is not None:
            return pd.DataFrame([regs], index=[datetime.now()])
        else:
            raise Exception('Failed to read registers')
        
    def toCsv(self, path: str) -> None:
        '''
        Save the currently loaded log to csv
        '''
        self.log = self.log.rename_axis('time')
        self.log.to_csv(path)

    def clearLogData(self) -> None:
        '''
        Clears all currently loaded data
        '''
        self.log = self.log[0:0]
        
    def isConnected(self) -> bool:
        '''
        Check if the connection to the server is open
        '''
        return self.client.is_open

    def setTagMap(self, tag_map: list[dict]) -> None:
        '''
        Set the tag map for the registers
        '''
        self.tag_map = tag_map



if __name__ == '__main__':

    # Settings
    poll_time = 1
    plc_ip = "192.168.0.1"
    csv_path = "Logs/ModbusTestLog.csv"
        
    # response = os.system("ping " + plc_ip)
    # print('Response: ' + str(response))

    logger = ModbusLogger(csv_path, tag_map=[0 for _ in range(60)])
    logger.connect(plc_ip, 503, 2)

    # Try 2 logging cycles and print result
    logger.logRegisters()
    time.sleep(1)
    logger.logRegisters()
    print(logger.log)

    # Dump csv
    logger.toCsv('C:\\Users\\Quantum\\Desktop\\Data Log Visualization\\modbus_test.csv')