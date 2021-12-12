import time

from mqtt_handler import MqttHandler


def main():
    MqttHandler.init()

    time.sleep(60)

    MqttHandler.shutdown()


if __name__ == '__main__':
    main()
