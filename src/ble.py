import asyncio
from bleak import BleakScanner
from bleak.backends.scanner import AdvertisementData
from send_message_mqtt import send_message, TyreMessage


def extract_sensor_number(x, name):
    # print(type(bytes[256]))
    # test5 = [0, 1,2,3,4,5,6,7,8,9]
    # print(test5[0:2])
    # x =  b'\x83\xea\xcaB\x19\xf9\x91\xcd\x03\x00g\x08\x00\x00`\x00'
    # print(test)
    # manufactuer = test[0:4]
    # print(manufactuer)
    x=x[256]
    psi = x[6] | (x[7] << 8) | (x[8] << 16) | (x[9] << 24)
    psi *= 0.000145038
    print("psi: ", psi)
    temp = (x[10] | (x[11] << 8) ) / 100.0 
    print("temp: ", temp)
    battery =  x[14]
    print("bat: ", battery)
    warn = x[15]
    print("warn: ", warn)
    sensor_id = f"{x[3]}{x[4]}{x[5]}"
    print("sensor: ",x[3], x[4],x[5])
    # print(test)
    # decoded = test.decode('unicode_escape')
    # print(decoded)
    print("")
    number = int(name.split("TPMS")[1][0])
    send_message(message=TyreMessage(number=number,name=name,psi=psi,temp=temp,battery=battery, warning=warn,sensor_id=sensor_id))
    

async def main():
    stop_event = asyncio.Event()

    # TODO: add something that calls stop_event.set()

    def callback(device: str, advertising_data: AdvertisementData):
        # TODO: do something with incoming data
        # if device == "81:EA:CA:22:4A:7B":
        if advertising_data.local_name is None:
            return
        if 'TPMS' in advertising_data.local_name:
            # print(device)
            # print(advertising_data.manufacturer_data)
            print(advertising_data.local_name)
            extract_sensor_number(advertising_data.manufacturer_data, advertising_data.local_name)

    async with BleakScanner(callback):
        ...
        # Important! Wait for an event to trigger stop, otherwise scanner
        # will stop immediately.
        # await scanner.find_device_by_address(device_identifier='81:EA:CA:22:4A:7B')
        await stop_event.wait()

    # scanner stops when block exits
    ...
