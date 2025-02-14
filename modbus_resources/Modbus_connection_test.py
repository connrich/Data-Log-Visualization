from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
import struct


if __name__ == '__main__':
    plc_ip = "192.168.0.1"
    unit_id = 2
    int_port = 503
    float_port = 502

    num_reg_to_read = 49

    '''
    Used for integer values
    '''
    client = ModbusClient(host=plc_ip, port=int_port, unit_id=unit_id, auto_open=True, auto_close=False) 
    regs = client.read_holding_registers(0, num_reg_to_read)
    print(f'Integer values: {utils.get_list_2comp(regs, 16)}')
    
    '''
    Used for float values
    '''
    client = ModbusClient(host=plc_ip, port=float_port, unit_id=unit_id, auto_open=True, auto_close=False) 
    regs = client.read_holding_registers(0, num_reg_to_read)
    # Convert registers to float values
    float_values = []
    for i in range(0, num_reg_to_read-1, 2):
        raw = struct.pack(">HH", regs[i], regs[i + 1])  # Big Endian format
        float_values.append(struct.unpack(">f", raw)[0])  # Convert to float
    print("Float values:", float_values)


