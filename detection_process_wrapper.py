import camera
import detector
import frame_processor
import multiprocessing
from multiprocessing import Process, Value
import time as t
import constants as C


class Detection_Process:
    _process = None
    _recv = None
    _recvCt = 0
    _run_flag = multiprocessing.Value('i', 0)
    
    _cam_name = "NO_NAME"

    def __init__(self, cam_specs):
        self._recv, sender = multiprocessing.Pipe()
        cam = camera.UC10MPC_ND(cam_specs)
        at_detector = detector.detector()
        processor = frame_processor.Frame_Processor(cam, at_detector, sender, self._run_flag)
        self._process = Process(target=processor.run_detections, args=(), daemon=False)

        self._cam_name = cam_specs['name']
        

    def start(self):
        self._run_flag.value = 1
        self._process.start()

    def pause(self):
        self._run_flag.value = 2
    def unpause(self):
        print(f"{self._cam_name} unpause")
        self._run_flag.value = 1

    def close(self):
        self._run_flag.value = 0
        print(f"{self._cam_name}, recvCt:{self._recvCt}")
        self._recv.close()
        print(f"{self._cam_name} clsoe proc-", end = '\t')
        self._process.join()
        print("success")





    # def get_robot_rel_pose(self):
    #     pose = ()
    #     if (self._recv.poll(timeout=C.PIPE_TIMEOUT)):
    #         self._recvCt+=1
    #         pose = self._recv.recv()
    #     return pose
    
    def get_all_robot_rel_pose(self):
        poses = []
        while (self._recv.poll(timeout=C.PIPE_TIMEOUT)):
            poses.append(self._recv.recv())
            self._recvCt+=1
        return poses