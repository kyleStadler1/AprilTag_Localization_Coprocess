import threading
from threading import Lock
import time as t
import numpy
import constants as C


class Frame_Processor():
    _result_pipe = None
    _camera_thread = None
    _cam = None
    _frame_ref = None
    _frame_date = None
    _lock = Lock()
    _detector = None
    _run_flag = None


    def __init__(self, camera, detector, result_pipe, run_flag):
        self._result_pipe = result_pipe
        self._detector = detector
        self._cam = camera
        t = threading.Thread(target=camera.run_camera, args=(self.set_frame_ref,), daemon=True)
        self._camera_thread = t
        self._run_flag = run_flag

    def set_frame_ref(self, frame, time):
        if (len(frame) == 0):
            if (C.CAM_DEBUG_ERR): print(f"{self._cam.name} BAD FRAME {t.time()}")
            return
        self._lock.acquire()
        self._frame_ref = frame
        self._frame_date = time
        self._lock.release()
 

    def run_detections(self):
        self._camera_thread.start()
        while self._run_flag.value:
            while self._run_flag.value == 2:
                t.sleep(0.1)
            self._lock.acquire()
            if (not self._frame_ref is None):
                frame_to_proc = self._frame_ref
                frame_to_proc_date = self._frame_date
                self._frame_ref = None
                self._frame_date = None
                self._lock.release()
                # self._detector._detector.detect(frame_to_proc)
                # rel_tag_pose_dict0 = {
                #     'ID' : 1,
                #     'x' : 2.67897,
                #     'y' : 2.67897,
                #     'z' : 2.67897,
                #     'pitch' : 2.67897,
                #     'yaw' : 2.67897,
                #     'roll' : 2.67897,
                #     'capture_time' : t.time(),
                # }
                robot_rel_tag_data_list = self._detector.get_robot_rel_tags(frame_to_proc, frame_to_proc_date, self._cam.intrinsics, self._cam.x_pos, self._cam.y_pos, self._cam.z_pos, self._cam.pitch, self._cam.yaw, self._cam.rotation_matrix)
                for robot_rel_tag_data in robot_rel_tag_data_list:
                    self._send_with_without_timeout(robot_rel_tag_data, C.PIPE_TIMEOUT)
            else:
                self._lock.release()
        self._result_pipe.close()
        
        
        self._cam.is_running = False
        self._camera_thread.join()
        print(f"{self._cam.name} thread status: {str(self._camera_thread.is_alive())}")

    # def _send_with_timeout(self, tag_pose, timeout):
    #     def sender_thread():
    #         try:
    #             self._result_pipe.send(tag_pose)
    #             self._sendCt+=1
    #         except Exception as e:
    #             print(f"{self._cam.name} Error sending data: {e}")
    #     sender = threading.Thread(target=sender_thread, daemon=True)
    #     sender.start()
    #     sender.join(timeout)
    #     if (sender.is_alive()):
    #         print(f"{self._cam.name} pipe_send_timeout(s): {timeout}, active_threads: {threading.active_count()}")
    #         return False
    #     else:
    #         return True
        

    def _send_with_without_timeout(self, tag_pose, timeout):
        #start = t.perf_counter()
        try:
            self._result_pipe.send(tag_pose)
        except Exception as e:
            print(f"{self._cam.name} Error sending data: {e}")
            return False
        #print(t.perf_counter() - start)
        return True
