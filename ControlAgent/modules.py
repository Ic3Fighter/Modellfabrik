import mqtt_handler
from order_queue import Queue


class MainUnit:
    status = "startup"

    def module_online():
        return "MainUnit" in mqtt_handler.MqttHandler.modules

    def process_message(topic, payload):
        if str(topic).endswith("Status"):
            MainUnit.status = payload
            print("MainUnit changed status to", payload)

            if payload == "inbound":
                print("Color inbound for MainUnit")

            # check availability for new order
            elif payload == "ready":
                Queue.send_order()

            # commence transport to next module
            elif payload == "done":
                pass

    def send_order(id):
        if not MainUnit.status == "ready":
            print("MainUnit is not ready for new order!")
        else:
            print("Sending order", id, "to MainUnit")
            mqtt_handler.MqttHandler.client.publish("Order/Send", id, 2)
            MainUnit.status = "inbound"
            mqtt_handler.MqttHandler.client.publish("Modules/MainUnit/Status", MainUnit.status, 1, True)

    # move order to next module
    def move_order(id):
        if MainUnit.status == "ready" and ProcessingStation.status == "ready":
            print("Moving order out of MainUnit")
            MainUnit.status = "outbound"
            mqtt_handler.MqttHandler.client.publish("Modules/MainUnit/Status", MainUnit.status, 1, True)
            ProcessingStation.status = "inbound"
            mqtt_handler.MqttHandler.client.publish("Modules/ProcessingStation/Status", ProcessingStation.status, 1, True)
        else:
            print("Modules are not yet ready!")


class ProcessingStation:
    status = "startup"

    def module_online():
        return "ProcessingStation" in mqtt_handler.MqttHandler.modules

    def process_message(topic, payload):
        if str(topic).endswith("Status"):
            ProcessingStation.status = payload
            print("ProcessingStation changed status to", payload)

            if payload == "inbound":
                print("New order inbound for ProcessingStation")

    # move order to next module
    def move_order(id):
        if ProcessingStation.status == "ready" and SortingLine.status == "ready":
            print("Moving order out of ProcessingStation")
            ProcessingStation.status = "outbound"
            mqtt_handler.MqttHandler.client.publish("Modules/ProcessingStation/Status", ProcessingStation.status, 1, True)
            SortingLine.status = "inbound"
            mqtt_handler.MqttHandler.client.publish("Modules/SortingLine/Status", SortingLine.status, 1, True)
        else:
            print("Modules are not yet ready!")


class SortingLine:
    status = "startup"

    def module_online():
        return "SortingLine" in mqtt_handler.MqttHandler.modules

    def process_message(topic, payload):
        if str(topic).endswith("Status"):
            ProcessingStation.status = payload
            print("SortingLine changed status to", payload)

            if payload == "inbound":
                print("New order inbound for SortingLine")

    # move order to next module
    def move_color():
        if SortingLine.status == "ready" and MainUnit.status == "ready":
            print("Moving color out of SortingLine")
            SortingLine.status = "outbound"
            mqtt_handler.MqttHandler.client.publish("Modules/SortingLine/Status", SortingLine.status, 1, True)
            MainUnit.status = "inbound"
            mqtt_handler.MqttHandler.client.publish("Modules/MainUnit/Status", MainUnit.status, 1, True)
        else:
            print("Modules are not yet ready!")
