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

            # check availability for new order
            if payload == "ready":
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
            mqtt_handler.MqttHandler.client.publish("Modules/MainUnit/Status", MainUnit.status, 2)
