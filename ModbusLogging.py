from pyModbusTCP.client import ModbusClient
import time
import os



if __name__ == '__main__':

    # Settings
    sleep_time = 1
    plc_ip = "192.168.0.1"
    csv_path = "Logs/ModbusTestLog.csv"

    response = os.system("ping -c 1 " + plc_ip)
    print('Response: ' + str(response))

    # TCP auto connect on first modbus request
    c = ModbusClient(host=plc_ip, port=502, unit_id=1, auto_open=True)

    while 1:
        # Read several registers 
        regs = c.read_holding_registers(29)

        # Open csv to append value 
        # with open(csv_path, 'a') as f:
        #     f.write(regs)

        # Display the read values 
        print('\n')
        print(regs)
        print('\n')

        # Wait for logging frequency
        time.sleep(sleep_time)



