import json

import mqtt_handler
from order_queue import Queue


class MainUnit:
    status = {
        "status": "startup",
        "order": "null"
    }

    def module_online():
        return "MainUnit" in mqtt_handler.MqttHandler.modules

    def process_message(topic, payload):
        if str(topic).endswith("Status"):
            try:
                MainUnit.status = json.loads(payload)
                print("MainUnit changed status to", payload)
            except:
                MainUnit.status = {"status": "error", "order": "null"}
                mqtt_handler.MqttHandler.client.publish("Modules/MainUnit/Status", json.dumps(MainUnit.status), 1, True)
                # print("MainUnit changed status to", MainUnit.status)

            # check availability for new order
            if MainUnit.status['status'] == "ready":
                Queue.send_order()

            elif MainUnit.status['status'] == "inbound":
                print("Color inbound for MainUnit")

            elif MainUnit.status['status'] == "busy":
                # no depending previous module
                pass

            # commence transport to next module
            elif MainUnit.status['status'] == "done":
                try:
                    MainUnit.move_order(MainUnit.status['order'])
                except ValueError:
                    print("MainUnit is status done, but could not process order id!")

    # check next module in cycle and send if available
    def send_order(id):
        if not MainUnit.status['status'] == "ready":
            print("MainUnit is not ready for new order!")
        else:
            print("Sending order", id, "to MainUnit")
            mqtt_handler.MqttHandler.client.publish("Order/Send", id, 2)
            MainUnit.status = {"status": "inbound", "order": id}
            mqtt_handler.MqttHandler.client.publish("Modules/MainUnit/Status", json.dumps(MainUnit.status), 1, True)

    # move order to next module
    def move_order(id):
        if MainUnit.status['status'] == "done" and ProcessingStation.status['status'] == "ready":
            print("Moving order out of MainUnit")
            MainUnit.status = {"status": "outbound", "order": id}
            mqtt_handler.MqttHandler.client.publish("Modules/MainUnit/Status", json.dumps(MainUnit.status), 1, True)
            ProcessingStation.status = {"status": "inbound", "order": id}
            mqtt_handler.MqttHandler.client.publish("Modules/ProcessingStation/Status", json.dumps(ProcessingStation.status), 1, True)
        else:
            print("Modules are not yet ready!")


class ProcessingStation:
    status = {
        "status": "startup",
        "order": "null"
    }

    def module_online():
        return "ProcessingStation" in mqtt_handler.MqttHandler.modules

    def process_message(topic, payload):
        if str(topic).endswith("Status"):
            try:
                ProcessingStation.status = json.loads(payload)
                print("ProcessingStation changed status to", payload)
            except:
                ProcessingStation.status = {"status": "error", "order": "null"}
                mqtt_handler.MqttHandler.client.publish("Modules/ProcessingStation/Status", json.dumps(ProcessingStation.status), 1, True)
                # print("ProcessingStation changed status to", ProcessingStation.status)

            # check availability for new order
            if ProcessingStation.status['status'] == "ready":
                try:
                    MainUnit.move_order(MainUnit.status['order'])
                except ValueError:
                    print("ProcessingStation is status ready, but no new order id was provided!")

            elif ProcessingStation.status['status'] == "inbound":
                print("New order inbound for ProcessingStation")

            elif ProcessingStation.status['status'] == "busy":
                # part received succesfully, change previous to ready
                MainUnit.status = {"status": "ready", "order": "null"}
                mqtt_handler.MqttHandler.client.publish("Modules/MainUnit/Status", json.dumps(MainUnit.status), 1, True)

            # start transport to next module
            elif ProcessingStation.status['status'] == "done":
                try:
                    ProcessingStation.move_order(ProcessingStation.status['order'])
                except ValueError:
                    print("ProcessingStation is status done, but could not process order id!")

    # move order to next module
    def move_order(id):
        if ProcessingStation.status['status'] == "done" and SortingLine.status['status'] == "ready":
            print("Moving order out of ProcessingStation")
            ProcessingStation.status = {"status": "outbound", "order": id}
            mqtt_handler.MqttHandler.client.publish("Modules/ProcessingStation/Status", json.dumps(ProcessingStation.status), 1, True)
            SortingLine.status = {"status": "inbound", "order": id}
            mqtt_handler.MqttHandler.client.publish("Modules/SortingLine/Status", json.dumps(SortingLine.status), 1, True)
        else:
            print("Modules are not yet ready!")


class SortingLine:
    status = {
        "status": "startup",
        "order": "null"
    }

    def module_online():
        return "SortingLine" in mqtt_handler.MqttHandler.modules

    def process_message(topic, payload):
        if str(topic).endswith("Status"):
            try:
                SortingLine.status = json.loads(payload)
                print("SortingLine changed status to", payload)
            except:
                SortingLine.status = {"status": "error", "order": "null"}
                mqtt_handler.MqttHandler.client.publish("Modules/SortingLine/Status", json.dumps(SortingLine.status), 1, True)
                # print("SortingLine changed status to", SortingLine.status)

            # check availability for new order
            if SortingLine.status['status'] == "ready":
                try:
                    ProcessingStation.move_order(ProcessingStation.status['order'])
                except ValueError:
                    print("SortingLine is status ready, but no new order id was provided!")

            elif SortingLine.status['status'] == "inbound":
                print("New order inbound for SortingLine")

            elif SortingLine.status['status'] == "busy":
                # part received succesfully, change previous to ready
                ProcessingStation.status = {"status": "ready", "order": "null"}
                mqtt_handler.MqttHandler.client.publish("Modules/ProcessingStation/Status", json.dumps(ProcessingStation.status), 1, True)

            # start transport to next module
            elif SortingLine.status['status'] == "done":
                # try:
                #     ProcessingStation.move_order(ProcessingStation.status['order'])
                # except ValueError:
                #     print("ProcessingStation is status done, but could not process order id!")
                SortingLine.status = {"status": "ready", "order": "null"}
                mqtt_handler.MqttHandler.client.publish("Modules/SortingLine/Status", json.dumps(SortingLine.status), 1, True)

    # move order to next module
    def move_color():
        # SortingLine status does not really matter for this operation
        if SortingLine.status['status'] == "ready" and MainUnit.status['status'] == "ready":
            print("Moving color out of SortingLine")
            SortingLine.status['status'] = "outbound"
            mqtt_handler.MqttHandler.client.publish("Modules/SortingLine/Status", json.dumps(SortingLine.status), 1, True)
            MainUnit.status = {"status": "inbound", "order": "color"}
            mqtt_handler.MqttHandler.client.publish("Modules/MainUnit/Status", json.dumps(MainUnit.status), 1, True)
        else:
            print("Modules are not yet ready!")
