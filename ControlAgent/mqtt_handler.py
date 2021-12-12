import paho.mqtt.client as mqttc
import json

import config
import modules
import order_queue


class MqttHandler:
    client = mqttc.Client()
    modules = []

    def init():
        # setup client
        # MqttHandler.client = mqttc.Client()
        MqttHandler.client.on_connect = MqttHandler.on_connect
        MqttHandler.client.on_disconnect = MqttHandler.on_disconnect
        MqttHandler.client.on_message = MqttHandler.on_message
        MqttHandler.client.on_publish = MqttHandler.on_publish
        MqttHandler.client.on_subscribe = MqttHandler.on_subscribe
        MqttHandler.client.on_unsubscribe = MqttHandler.on_unsubscribe

        # connect to broker
        MqttHandler.client.connect(config.MQTT_BROKER_HOST, config.MQTT_BROKER_PORT, config.MQTT_BROKER_KEEPALIVE)
        MqttHandler.client.loop_start()

        # subscribe to monitoring topics
        MqttHandler.client.subscribe([
            ("Discovery/+", 2),
            ("Modules/+/Status", 2),
            ("Order/Queue", 2)
        ])  # + is single level placeholder

    def shutdown():
        MqttHandler.client.loop_stop()
        print("MQTT shutdown successful!")

    def on_connect(client, userdata, flags, rc):
        if rc == 5:
            print("Authentication error on connect!")
        else:
            print("Connected with result code", str(rc))

    def on_disconnect(client, userdata, rc):
        print("Disconnected with result code", str(rc))

    def on_message(client, userdata, msg):
        msg.payload = msg.payload.decode("utf-8")

        if msg.topic == "Discovery/Login":
            MqttHandler.register_module(msg.payload)
        elif msg.topic == "Discovery/Logout":
            MqttHandler.unregister_module(msg.payload)
        elif str(msg.topic).startswith('Modules'):
            module = msg.topic.split('/')[1]  # Modules/<Name>/Status

            if module == "MainUnit":
                modules.MainUnit.process_message(msg.topic, msg.payload)
            elif module == "ProcessingStation":
                pass
            elif module == "SortingLine":
                pass
            else:
                print("Unknown module:", module)
        elif msg.topic == "Order/Queue":
            try:
                order_queue.Queue.new_order(int(msg.payload))
            except ValueError as exc:
                print(str(msg.payload), "could not be converted to int!")

    def on_publish(client, userdata, mid):
        pass

    def on_subscribe(client, userdata, mid, granted_qos):
        pass

    def on_unsubscribe(client, userdata, mid):
        pass

    def register_module(module_name):
        # check for possible duplicate
        if not module_name in MqttHandler.modules:
            MqttHandler.modules.append(module_name)
            msg = json.dumps({"name": module_name, "ack": True})
            print(f"Module {module_name} has been approved")
        else:
            msg = json.dumps({"name": module_name, "ack": False})
            print(f"Module {module_name} hasn't been approved")

        MqttHandler.client.publish("Discovery/LoginAck", msg, 2)

    def unregister_module(module_name):
        if module_name in MqttHandler.modules:
            print(f"Unregister module {module_name}")
            MqttHandler.modules.remove(module_name)
            MqttHandler.client.publish("Modules/" + module_name + "/Status", "disconnected", 1, True)
