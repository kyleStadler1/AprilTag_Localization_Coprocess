import cv2
import time as t
import numpy as np
import constants as C

class UC10MPC_ND():
    _cap = None
    is_running = True
    name = 'NO_NAME'
    x_pos = 0
    y_pos = 0
    z_pos = 0
    pitch = 0
    yaw = 0
    intrinsics = ()
    _addr= ''
    rotation_matrix = []

    def __init__(self, cam_specs):
        self.is_running = True
        self.name = cam_specs['name']
        self.x_pos = cam_specs['x']
        self.y_pos = cam_specs['y']
        self.z_pos = cam_specs['z']
        self.pitch = cam_specs['pitch']
        self.yaw = cam_specs['yaw']
        self.intrinsics = cam_specs['intrinsics']
        self._addr = cam_specs['addr']
        self.rotation_matrix = np.matmul(rotation_matrix_y(self.yaw), rotation_matrix_x(-self.pitch))
        self._cap = self._init_cam(self._addr, C.IMG_WIDTH, C.IMG_HEIGHT)
        if (C.CAM_DEBUG):
            status, frame = self._cap.read()
            print(f"{self.name} Status:{status}, Addr:{self._addr}")
        

    def camera_read(self):
        read_time = t.perf_counter()
        ret, frame = self._cap.read()
        if ret:
            frame = cv2.imdecode(frame, cv2.IMREAD_GRAYSCALE)
        else:
            frame = ()
        return (frame, read_time)
    
    def run_camera(self, set_frame_ref):
        while self.is_running:
            frame, time_ = self.camera_read()
            if (frame == ()):
                print("sending bad frame")
            set_frame_ref(frame, time_)
        self._cap.release()
        if C.CAM_DEBUG: print(f"{self.name} clean stop")
        return False

    def _init_cam(self, addr, w, h):
        cap = cv2.VideoCapture(addr)
        cap.set(cv2.CAP_PROP_FPS, C.FPS)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))
        cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
        return cap
    
def rotation_matrix_x(ax):
    return np.array([
        [1, 0, 0],
        [0, np.cos(ax), -np.sin(ax)],
        [0, np.sin(ax), np.cos(ax)]
    ])

def rotation_matrix_y(ay):
    return np.array([
        [np.cos(ay), 0, np.sin(ay)],
        [0, 1, 0],
        [-np.sin(ay), 0, np.cos(ay)]
    ])

# def rotation_matrix_z(az): 
#     return np.array([
#         [np.cos(az), -np.sin(az), 0],
#         [np.sin(az), np.cos(az), 0],
#         [0, 0, 1]
#     ])


