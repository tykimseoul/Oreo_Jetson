from multiprocessing import Process
from video_processing.stereo_camera import *
from main import *


class Controller:
    def start_controls(self):
        control_thread = Process(name='android', target=self.apply_control)
        control_thread.start()

    def apply_control(self):
        while True:
            try:
                control = pop_command()
                if not control[0]:
                    self.steer(control[1][0])
                    self.accelerate(control[1][1])
                else:
                    depth_map = calculate_depth_map()
                    prediction = predict(depth_map)
                    self.steer(prediction[0])
                    self.accelerate(prediction[1])
            except Exception:
                print('exp')

    def steer(self, angle):
        pass

    def accelerate(self, speed):
        pass
