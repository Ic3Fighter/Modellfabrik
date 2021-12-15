import modules


class Queue:
    orders = []

    def first():
        if len(Queue.orders) > 0:
            return Queue.orders[0]
        else:
            return None

    def last():
        if len(Queue.orders) > 0:
            return Queue.orders[-1]
        else:
            return None

    def enqueue(id):
        if not id in Queue.orders:
            Queue.orders.append(id)
            return True
        else:
            return False

    def dequeue(id):
        if id in Queue.orders:
            Queue.orders.remove(id)
            return True
        else:
            return False

    # create new order entry
    def new_order(id):
        print("New order with id", str(id))
        Queue.enqueue(id)
        Queue.send_order()

    # send first order of queue to MainUnit
    def send_order():
        id = Queue.first()
        if modules.MainUnit.status == "ready" and modules.MainUnit.module_online() and id is not None:
            print("Next order with id", str(id))
            Queue.dequeue(id)
            # send order to MainUnit
            modules.MainUnit.send_order(id)
        else:
            print("MainUnit is not ready!")
