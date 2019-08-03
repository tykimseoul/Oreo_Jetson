from connection.connector import Connector
from connection.controller import Controller
from multiprocessing import Queue
from self_driving.model import *

command_queue = Queue()
model = Model()
model.load_model()
connector = Connector()
connector.connect()


# controller = Controller()
# controller.start_controls()


def push_command(command):
    command_queue.put(command)


def pop_command():
    return command_queue.get(block=True)


def predict(depth_map):
    return model.predict_single(depth_map)
