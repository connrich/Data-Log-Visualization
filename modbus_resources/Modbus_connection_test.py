from pyModbusTCP.client import ModbusClient


if __name__ == '__main__':
    plc_ip = "192.168.0.1"
    port = 502
    unit_id = 2

    client = ModbusClient(host=plc_ip, port=port, unit_id=unit_id, auto_open=True, auto_close=False) 
    regs = client.read_holding_registers(0, 48)

    print(regs)
