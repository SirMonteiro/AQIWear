# main.py -- put your code here!

import machine
try:
    import uasyncio as asyncio
except ImportError:
    import asyncio
from bluetooth import UUID as BLUUID
import aioble

from struct import pack
from micropython import const
from math import log

# import hdc1080
import micropython_hdc1080.hdc1080 as hdc1080
from ccs811 import CCS811
from dsm501 import DSM501

# org.bluetooth.service.environmental_sensing
_ENV_SENSE_UUID = BLUUID(0x181A)

# org.bluetooth.characteristic.temperature
_ENV_SENSE_TEMP_UUID = BLUUID(0x2A6E)

# org.bluetooth.characteristic.humidity
_ENV_SENSE_HUMIDITY_UUID = BLUUID(0x2A6F)

# org.bluetooth.characteristic.dew_point
_ENV_SENSE_DEW_POINT_UUID = BLUUID(0x2A7B)

# org.bluetooth.characteristic.carbon_dioxide_concentration
_ENV_SENSE_CO2_UUID = BLUUID(0x2B8C)

# org.bluetooth.characteristic.volatil_organic_compound_concentration
_ENV_SENSE_VOC_UUID = BLUUID(0x2BE7)

# org.bluetooth.characteristic.particulate_matter_pm1_concentration
_ENV_SENSE_PM1_UUID = BLUUID(0x2BD5)

# org.bluetooth.characteristic.particulate_matter_2_5
_ENV_SENSE_PM25_UUID = BLUUID(0x2BD6)

# org.bluetooth.characteristic.particulate_matter_pm10_concentration
# _ENV_SENSE_PM10_UUID = BLUUID(0x2BD7)

# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_AIR_QUALITY_SENSOR = const(1346)

# How frequently to send advertising beacons.
_ADV_INTERVAL_MS = 250_000

# Register GATT server.
device_service = aioble.Service(_ENV_SENSE_UUID)
temp_characteristic = aioble.Characteristic( device_service, _ENV_SENSE_TEMP_UUID, read=True, notify=True)
humidity_characteristic = aioble.Characteristic( device_service, _ENV_SENSE_HUMIDITY_UUID, read=True, notify=True)
dew_point_characteristic = aioble.Characteristic( device_service, _ENV_SENSE_DEW_POINT_UUID, read=True, notify=True)

co2_characteristic = aioble.Characteristic( device_service, _ENV_SENSE_CO2_UUID, read=True, notify=True)
voc_characteristic = aioble.Characteristic( device_service, _ENV_SENSE_VOC_UUID, read=True, notify=True)

pm1_characteristic = aioble.Characteristic( device_service, _ENV_SENSE_PM1_UUID, read=True, notify=True)
pm25_characteristic = aioble.Characteristic( device_service, _ENV_SENSE_PM25_UUID, read=True, notify=True)
# pm10_characteristic = aioble.Characteristic( device_service, _ENV_SENSE_PM10_UUID, read=True, notify=True)

aioble.register_services(device_service)

class CCS811_AND_HDC1080_SENSOR:
    def __init__(self, i2c):
        self.ccs811 = CCS811(i2c)
        self.hdc1080 = hdc1080.HDC1080(i2c)
        self.temperature = None
        self.humidity = None

    async def ccs811_sensor(self):
        # while True:
        #     if self.temperature is not None and self.humidity is not None:
        #         if self.ccs811.data_is_ready: # type: ignore
        #             self.ccs811.temperature = self.temperature # type: ignore
        #             self.ccs811.humidity = self.humidity # type: ignore
        #             encoded_co2 = pack("<H", int(self.ccs811.eco2)) # type: ignore
        #             co2_characteristic.write(encoded_co2, send_update=True)

        #             encoded_voc = pack("<H", int(self.ccs811.etvoc)) # type: ignore
        #             voc_characteristic.write(encoded_voc, send_update=True)

        #             print(f"CO2: {self.ccs811.eco2}, VOC: {self.ccs811.etvoc}") # type: ignore

        #             await asyncio.sleep(1)
        #     await asyncio.sleep(1)
        while True:
            if self.ccs811.data_ready():
                eCO2 = self.ccs811.eCO2
                tVOC = self.ccs811.tVOC
                encoded_co2 = pack("<H", int(eCO2))
                co2_characteristic.write(encoded_co2, send_update=True)

                encoded_voc = pack("<H", int(tVOC))
                voc_characteristic.write(encoded_voc, send_update=True)

                print(f"CO2: {eCO2}, VOC: {tVOC}")

                await asyncio.sleep(1)
            await asyncio.sleep(1)

    async def hs1080_sensor(self):
        while True:
            self.temperature, self.humidity = self.hdc1080.measurements

            encoded_temp = pack("<h", int(self.temperature * 100))
            temp_characteristic.write(encoded_temp, send_update=True)

            encoded_humidity = pack("<H", int(self.humidity * 100))
            humidity_characteristic.write(encoded_humidity, send_update=True)

            print(f"Temperature: {self.temperature}, Humidity: {self.humidity}")

            await self.dew_point_calculation()
            await asyncio.sleep(1)

    async def dew_point_calculation(self):
        if self.temperature is not None and self.humidity is not None:
            # Dew point calculation based on magnus formula
            a = 17.271
            b = 237.7
            if self.humidity == 0:
                self.humidity = 50.0
            alpha = ((a * self.temperature) / (b + self.temperature)) + log(self.humidity / 100.0)
            dew_point = (b * alpha) / (a - alpha)
            encoded_dew_point = pack("<h", int(dew_point * 100))
            dew_point_characteristic.write(encoded_dew_point, send_update=True)

            print(f"Dew Point: {dew_point}")

            # self.temperature = None
            # self.humidity = None

class PM_SENSOR:
    def __init__(self, pin_PM1, pin_PM25):
        self.DSM501 = DSM501(pin_PM1, pin_PM25)

    async def measure(self):
        while True:
            if not self.DSM501.is_ready():
                print("DSM501 is warming up")
                await asyncio.sleep(1)
                continue
            self.DSM501.update()
            pm1 = self.DSM501.getParticalWeight(0)
            pm25 = self.DSM501.getParticalWeight(1)

            print(f"PM1: {pm1:.2f}, PM2.5: {pm25:.2f}")

            encoded_pm1 = pack("<H", int(pm1 * 100))
            pm1_characteristic.write(encoded_pm1, send_update=True)
            encoded_pm25 = pack("<H", int(pm25 * 100))
            pm25_characteristic.write(encoded_pm25, send_update=True)

            await asyncio.sleep(1)

    # async def measure(self):
    #     while True:
    #         current_time = time.ticks_ms()

    #         # Warm-up countdown
    #         if not self.PM25.is_ready() and time.ticks_diff(current_time, self.timer) >= self.interval_countdown:
    #             print(f"DSM501 warm up: {self.PM25.get_ready_countdown()} seconds")
    #             self.timer = current_time

    #         # Read PM values
    #         elif self.PM25.is_ready() and time.ticks_diff(current_time, self.timer) >= self.interval_read:
    #             self.timer = current_time
    #             pm10 = self.PM10.read_pm()
    #             pm25 = self.PM25.read_pm()
    #             encoded_pm10 = pack("<H", int(pm10 * 100))
    #             pm10_characteristic.write(encoded_pm10, send_update=True)

    #             encoded_pm25 = pack("<H", int(pm25 * 100))
    #             pm25_characteristic.write(encoded_pm25, send_update=True)

    #             print(f"PM10: {pm10:.2f}, PM2.5: {pm25:.2f}")

    #         await asyncio.sleep(0.1)

    # async def pm25_sensor(self):
    #     while True:
    #         while not self.DSM501.is_ready():
    #             await asyncio.sleep(1)
    #         self.DSM501.handle_pulse()
    #         pm25 = self.DSM501.read_pm()
    #         print(f"PM25: {pm25}")
    #         encoded_pm25 = pack("<H", int(pm25 * 100))
    #         pm25_characteristic.write(encoded_pm25, send_update=True)
    #         await asyncio.sleep(1)

async def peripheral_task():
    while True:
        async with await aioble.advertise(
            _ADV_INTERVAL_MS,
            name="AQIWear",
            services=[_ENV_SENSE_UUID],
            appearance=_ADV_APPEARANCE_AIR_QUALITY_SENSOR,
        ) as connection:
            print("Connection from", connection.device)
            while connection.is_connected() == True:
                #print(f'Connection status: {connection.is_connected()}')
                await asyncio.sleep(1)
            print('Connection lost. switching back to advertising mode')

async def main():
    print("Initializing I2C")
    i2c = machine.SoftI2C(scl=machine.Pin(7), sda=machine.Pin(6))
    print("Initializing CCS811")
    ccs_hdc_sensor = CCS811_AND_HDC1080_SENSOR(i2c)

    print("Initializing PM Sensor")
    pm1_pin = 1
    pm25_pin = 2
    pm_sensor = PM_SENSOR(pm1_pin, pm25_pin)

    sensors = [
        asyncio.create_task(ccs_hdc_sensor.ccs811_sensor()),
               asyncio.create_task(ccs_hdc_sensor.hs1080_sensor()),
               asyncio.create_task(pm_sensor.measure())
               ]

    peripheral = asyncio.create_task(peripheral_task())

    print("Starting main loop")
    await asyncio.gather(peripheral, *sensors) # type: ignore

asyncio.run(main())
