import cv2
import time
import multiprocessing
from multiprocessing import Process, Pipe, Value
import camera
import detector
import frame_processor
import constants as C
import socket_sender


def run():
    run_flag = Value('i', 1)
    

    #cam pose POV: from behind the robot looking forward: right: +x, up: +y, closerToFront: +z
    #cam angles: ax: pitch : pitch up = +
    # ay: yaw: from cam pov, yaw right = +
    # az: keep that 0 bruh idek
    detection_process0, result_receiver0 = init_detector_process(C.FRONT_CAM_SPECS, run_flag)
    p0_recvCt = 0
    detection_process1, result_receiver1 = init_detector_process(C.REAR_CAM_SPECS, run_flag)
    p1_recvCt = 0

    rio_sender = socket_sender.Socket_Sender_Host()
    
    detection_process0.start()
    detection_process1.start()

    start_time = time.time()
    try:
        while(time.time() < start_time+10):
            pose0, p0_recvCt = get_all_robot_rel_pose(result_receiver0, C.PIPE_TIMEOUT, p0_recvCt)
            pose1, p1_recvCt = get_all_robot_rel_pose(result_receiver1, C.PIPE_TIMEOUT, p1_recvCt)
            for pose in pose0:
                rio_sender.send_robot_rel_tag_data(pose)
            for pose in pose1:
                rio_sender.send_robot_rel_tag_data(pose)
        run_flag.value = 0
        

        detection_process0.join()
        print("end0")
        detection_process1.join()
        print("end1")

        close_detection_process(detection_process0, result_receiver0, "cam0", p0_recvCt)
        close_detection_process(detection_process1, result_receiver1, "cam1", p1_recvCt)
    except KeyboardInterrupt:
        print("FORCED EXIT")
        run_flag.value = 0
        close_detection_process(detection_process0, result_receiver0, "cam0", p0_recvCt)
        close_detection_process(detection_process1, result_receiver1, "cam1", p1_recvCt)

    return 0
    
def get_robot_rel_pose(result_receiver, timeout_s, ct):
    pose = ()
    if (result_receiver.poll(timeout=timeout_s)):
        ct+=1
        pose = result_receiver.recv()
    return pose, ct
def get_all_robot_rel_pose(result_receiver, timeout_s, ct):
    poses = []
    while (result_receiver.poll(timeout=timeout_s)):
        poses.append(result_receiver.recv())
        ct+=1
    return poses, ct
 
def close_detection_process(process, result_receiver, identifier, ct):
    print(f"{identifier}, recvCt: {ct}")
    result_receiver.close()
    print(f"{identifier} close proc - ", end = '\t')
    process.join()
    print("success")
    
        
def init_detector_process(cam_specs, run_flag):
    result_receiver, result_sender = multiprocessing.Pipe()
    cam = camera.UC10MPC_ND(cam_specs)
    at_detector = detector.detector()
    processor = frame_processor.Frame_Processor(cam, at_detector, result_sender, run_flag)
    process = Process(target=processor.run_detections, args=(), daemon=False)
    return(process, result_receiver)








if __name__ == "__main__":
   run()