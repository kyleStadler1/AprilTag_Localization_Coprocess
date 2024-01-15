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

    _frameCt = 0
    _detectCt = 0
    _latencySum = 0
    _sendCt = 0

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
        self._frameCt+=1
 

    def run_detections(self):
        self._camera_thread.start()
        start_time = t.time()
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
                robot_rel_tag_data_list = self._detector.get_robot_rel_tags(frame_to_proc, frame_to_proc_date, self._cam.intrinsics, self._cam.x_pos, self._cam.y_pos, self._cam.z_pos, self._cam.pitch, self._cam.yaw, self._cam.rotation_matrix)
                self._detectCt+=1
                for robot_rel_tag_data in robot_rel_tag_data_list:
                    self._send_with_timeout(robot_rel_tag_data, C.PIPE_TIMEOUT)
                self._latencySum+=(t.perf_counter() - frame_to_proc_date)
            else:
                self._lock.release()
        elapsed_time = t.time() - start_time
        self._result_pipe.close()
        print(f"{self._cam.name} FPS: {self._frameCt/elapsed_time}", end='\t')
        print(f" DPS: {self._detectCt/elapsed_time}", end='\t')
        print(f" # of pipe sends: {str(self._sendCt)}", end='\t')
        if (self._detectCt > 0):
            print(f" Lens to pose latency_ms: {(self._latencySum/self._detectCt)*1000}", end='\n')
        else:
            print(f"ZERO DETECTOR RUNS")
        
        self._cam.is_running = False
        self._camera_thread.join()
        print(f"{self._cam.name} thread status: {str(self._camera_thread.is_alive())}")

    def _send_with_timeout(self, tag_pose, timeout):
        def sender_thread():
            try:
                self._result_pipe.send(tag_pose)
                self._sendCt+=1
            except Exception as e:
                print(f"{self._cam.name} Error sending data: {e}")
        sender = threading.Thread(target=sender_thread, daemon=True)
        sender.start()
        sender.join(timeout)
        if (sender.is_alive()):
            print(f"{self._cam.name} pipe_send_timeout(s): {timeout}, active_threads: {threading.active_count()}")
            return False
        else:
            return True
