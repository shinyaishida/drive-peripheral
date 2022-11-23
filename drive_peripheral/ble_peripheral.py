import os
import subprocess
from logging import getLogger
from pybleno import Bleno, BlenoPrimaryService, Characteristic


logger = getLogger(__name__)


class DrivePeripheral:
    def __init__(self, service_name):
        self.__service_name = service_name
        self.__service_uuid = os.environ['SERVICE_UUID']
        self.bleno = Bleno()
        self.bleno.on('stateChange', self.on_state_change)
        self.bleno.on('advertisingStart', self.on_advertising_start)
        self.__control_characteristic = ControlCharacteristic()
        self.__drive_characteristic = DriveCharacteristic()

    def on_state_change(self, state):
        logger.info(f'state changed to {state}')
        if (state == 'poweredOn'):
            self.bleno.startAdvertising(self.__service_name,
                                        [self.__service_uuid])
        else:
            self.bleno.stopAdvertising()

    def on_advertising_start(self, error):
        result = f'error {error}' if error else 'success'
        logger.info(f'started advertising: {result}')
        if not error:
            self.bleno.setServices([
                BlenoPrimaryService({
                    'uuid': self.__service_uuid,
                    'characteristics': [
                        self.__control_characteristic,
                        self.__drive_characteristic
                    ]
                })
            ])

    def start(self):
        self.bleno.start()


class ControlCharacteristic(Characteristic):
    def __init__(self):
        Characteristic.__init__(self, {
            'uuid': os.environ['CONTROL_CHAR_UUID'],
            'properties': ['read', 'notify'],
            'value': None
        })
        self.__update_value_callback = None

    def onSubscribe(self, max_value_size, update_value_callback):
        logger.info('subscribed')
        self.__update_value_callback = update_value_callback

    def onUnsubscribe(self):
        logger.info('unsubscribed')
        self.__update_value_callback = None


class DriveCharacteristic(Characteristic):
    def __init__(self):
        Characteristic.__init__(self, {
            'uuid': os.environ['DRIVE_CHAR_UUID'],
            'properties': ['write'],
            'value': None
        })
        self.servo = ServoDriver()

    def onWriteRequest(self, data, offset, without_response, callback):
        if data == b'Neutral':
            logger.debug('neutral')
            self.servo.drive(0)
        elif data == b'Forward':
            logger.debug('forward')
            self.servo.drive(1)
        elif data == b'Backward':
            logger.debug('backward')
            self.servo.drive(-5)
        elif data.startswith(b'Steering '):
            angle = int(data.split(b'Steering ')[1])
            logger.debug(f"steering '{angle}'")
            self.servo.steer(angle)
        else:
            logger.warning(f"unknown signal '{data}'")
        callback(self.RESULT_SUCCESS)


class ServoDriver:
    def drive(self, accel):
        freq = self.__driving_servo_freq(accel)
        subprocess.call(['./servoblaster.sh', f'2={freq}'])

    def __driving_servo_freq(self, accel):
        # accel is an integer value.
        # ServoBlaster drives forward with frequency between 149 and 100 while
        # backward with frequency between 159 and 200.
        # accel |  50 |   1 |   0 |     |  -1 | -50 |
        # freq  | 100 | 149 | 150 | 158 | 159 | 200 |
        if accel > 50:
            return 100
        elif accel < -50:
            return 200
        elif accel > 0:
            return 150 - accel
        elif accel < 0:
            return 158 - accel
        else:
            return 151

    def steer(self, angle):
        freq = self.__steering_servo_freq(angle)
        subprocess.call(['./servoblaster.sh', f'1={freq}'])

    def __steering_servo_freq(self, angle):
        # angle is an integer value; positive/negative to turn left/right.
        # ServoBlaster steers to left with frequency between 151 and 200 while
        # to right with frequency between 149 and 100.
        # angle |  50 |   1 |   0 |  -1 | -50 |
        # freq  | 200 | 151 | 150 | 149 | 100 |
        if angle > 50:
            return 200
        elif angle < -50:
            return 100
        else:
            return angle + 150
