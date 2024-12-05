from machine import Pin, time_pulse_us
from time import ticks_ms, ticks_diff

class DSM501:
    """
    DSM501 class for DSM501A/B particulate matter sensor
    pin1: PM1.0 output pin
    pin25: PM2.5 output pin
    sample_time: sampling time in ms, can be between 5000 and 30000
    """
    def __init__(self, pin1, pin25, sample_time=5000):
        self._warm_up_time = 30000
        self._pins = [Pin(pin1, Pin.IN), Pin(pin25, Pin.IN)]
        self.pulse_duration_sum = [0.0, 0.0]
        self.sample_time = sample_time
        self._boot_time = ticks_ms()


    def is_ready(self):
        if ticks_diff(ticks_ms(), self._boot_time) < self._warm_up_time:
            return False
        return True

    def update(self):
        if not self.is_ready():
            return
        start = ticks_ms()
        while ticks_diff(ticks_ms(), start) < self.sample_time:
            for i in range(2):
                pulse_duration = time_pulse_us(self._pins[i], 0, 5000000)
                # print(f"Pulse duration {i}: {pulse_duration}")
                if pulse_duration >= 0:
                    self.pulse_duration_sum[i] += pulse_duration / 1000.0

    def getLowRatio(self, i):
        return self.pulse_duration_sum[i] / self.sample_time * 100.0

    def getParticalWeight(self, i):
        # Using regression function from the datasheet
        low_ratio = self.getLowRatio(i)
        concentration = 0.00258425 * (low_ratio ** 2) + 0.0858521 * low_ratio - 0.01345549
        return max(0, concentration)

    def getPM25(self):
        return self.getParticalWeight(0) - self.getParticalWeight(1)
