# coding:utf-8
from PCA9685 import PCA9685


class Servo:
    def __init__(self):
        # minimum and maximum angle of the servo
        self.angleMin = 18
        self.angleMax = 162

        # PWM frequency is 50Hz, which is the standard for servos
        self.pwm = PCA9685(address=0x40, debug=True)
        self.pwm.setPWMFreq(50)

    # Convert the input angle to the value of PCA9685
    def map(self, value, fromLow, fromHigh, toLow, toHigh):
        return (toHigh - toLow) * (value - fromLow) / (fromHigh - fromLow) + toLow

    def setServoAngle(self, channel, angle):
        if angle < self.angleMin:
            angle = self.angleMin
        elif angle > self.angleMax:
            angle = self.angleMax
        # The PCA9685 uses a 12-bit resolution, so the range is 0-4095
        # The pulse width for the servo is between 0.5ms and 2.5ms
        # The pulse width is mapped to the range of 102-512
        # 102 corresponds to 0.5ms and 512 corresponds to 2.5ms
        MIN_PULSE = 102
        MAX_PULSE = 512
        data = self.map(angle, 0, 180, MIN_PULSE, MAX_PULSE)
        self.pwm.setPWM(channel, 0, int(data))

    def stopServo(self, channel):
        """Stops the servo by setting the pulse width to 0"""
        self.pwm.setPWM(channel, 0, 0)


# Main program logic follows:
if __name__ == "__main__":
    print("Now servos will rotate to 90°.")
    print("If they have already been at 90°, nothing will be observed.")
    print("Please keep the program running when installing the servos.")
    print("After that, you can press ctrl-C to end the program.")
    # XXX: It does not seems to stop the servos after ctrl-C
    S = Servo()
    while True:
        try:
            for i in range(16):
                S.setServoAngle(i, 90)
        except KeyboardInterrupt:
            print("\nEnd of program")
            for i in range(16):
                S.stopServo(i)
            break
