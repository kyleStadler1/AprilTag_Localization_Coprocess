
import camera
import constants as C
import time as t
import threading
from threading import Lock



def test():
    c_front = camera.UC10MPC_ND(C.FRONT_CAM_SPECS)
    c_rear= camera.UC10MPC_ND(C.REAR_CAM_SPECS)
    print("run cams on main thread - 10 sec")
    startTime = t.time()
    frameCt = 0
    while(t.time() < startTime + 10):
        c_front.camera_read()
        c_rear.camera_read()
        frameCt+=1
    print(f"cam fps: {frameCt}")

    print("run cams parallel threads")



    t_front = threading.Thread(target=c_front.run_camera, args=(set_frame_ref_front,), daemon=True)
    t_rear = threading.Thread(target=c_rear.run_camera, args=(set_frame_ref_rear,), daemon=True)

    t_front.start()
    t_rear.start()
    t.sleep(10)
    c_front.is_running = False
    c_rear.is_running = False
    t_front.join()
    t_rear.join()
    print("done")



    













def set_frame_ref_front(frame, time):
    if (len(frame) == 0):
        print("BAD FRAME")
        return


def set_frame_ref_rear(frame, time):
    if (len(frame) == 0):
        print("BAD FRAME")
        return
    





if __name__ == "__main__":
   test()