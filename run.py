import cv2
import time
import constants as C
import socket_sender
import detection_process_wrapper


def run():
  
    

    #cam pose POV: from behind the robot looking forward: right: +x, up: +y, closerToFront: +z
    #cam angles: ax: pitch : pitch up = +
    # ay: yaw: from cam pov, yaw right = +
    # az: keep that 0 bruh idek


    proc_front = detection_process_wrapper.Detection_Process(C.FRONT_CAM_SPECS)
    proc_rear =  detection_process_wrapper.Detection_Process(C.REAR_CAM_SPECS)
    rio_sender = socket_sender.Socket_Sender_Host()

    proc_front.start()
    proc_rear.start()
    

    start_time = time.time()
    eth_stat = True
    #while(time.time() < start_time+10):
    while 1:
        pose_front = proc_front.get_all_robot_rel_pose()
        pose_rear = proc_rear.get_all_robot_rel_pose()
        for pose in pose_front:
            eth_stat = rio_sender.send_robot_rel_tag_data(pose)
            pass
        for pose in pose_rear:
            eth_stat = rio_sender.send_robot_rel_tag_data(pose)
            pass
        
        if (not(eth_stat)):
            proc_front.pause()
            proc_rear.pause()
            rio_sender = socket_sender.Socket_Sender_Host()
            eth_stat = True
            proc_front.unpause()
            proc_rear.unpause()

    proc_front.close()
    proc_rear.close()
    return 0
    



if __name__ == "__main__":
   run()