import dependencies.apriltag as at
from dependencies.apriltag import Detection
import math as m
import numpy as np
import constants as C
import array
HALF_PI = m.pi/2.0





class detector():
    _detector = None
    _once = False
    _fake_results = None
    def __init__(self):
        self._detector = at.Detector()
        options = at.DetectorOptions(
                families= C.AT_FAMILY,
                border= C.BORDER, 
                nthreads= C.NTHREADS,
                quad_decimate= C.QUAD_DECIMATE, 
                quad_blur= C.QUAD_BLUR,
                refine_edges= C.REFINE_EDGES,
                refine_decode= C.REFINE_DECODE,
                refine_pose= C.REFINE_POSE,
                debug= C.DETECTOR_DEBUG,
                quad_contours= C.QUAD_CONTOURS 
            )
        self._detector = at.Detector(options = options)
        
    def get_robot_rel_tags(self, frame, frame_time, intrinsics, cam_x_pos, cam_y_pos, cam_z_pos, cam_pitch, cam_yaw, cam_rot_matrix):
        raw_results = self._detector.detect(frame)

        intermediate_results = self._reject_ID_confThresh(raw_results)
        final_results = []
        for result in intermediate_results:
            robot_rel_tag_data = self._get_pose(result, intrinsics, cam_x_pos, cam_y_pos, cam_z_pos, cam_pitch, cam_yaw, cam_rot_matrix)
            
            rel_tag_pose_dict = {
                'ID' : result.tag_id,
                'x' : robot_rel_tag_data[0],
                'y' : robot_rel_tag_data[1],
                'z' : robot_rel_tag_data[2],
                'pitch' : robot_rel_tag_data[3],
                'yaw' : robot_rel_tag_data[4],
                'roll' : robot_rel_tag_data[5],
                'capture_time' : frame_time,
            }
            if (self._reject_bad_pose(rel_tag_pose_dict)): final_results.append(rel_tag_pose_dict)
        return final_results
    
    def _reject_ID_confThresh(self, results):
        trueResults = []
        for i in range(0, len(results)):
            result = results[i]
            if (result.decision_margin > C.CONFIDENCE_THRESH and result.tag_id in C.VALID_IDS): #and result.tag_id in C.VALID_IDs
                trueResults.append(results[i])
        return trueResults
    
    def _reject_bad_pose(self, rel_tag_pose_dict):
        valid = True
        AT_height_err = rel_tag_pose_dict['y'] - C.AT_HEIGHTS_M[rel_tag_pose_dict['ID']]
        if (abs(AT_height_err) > C.AT_HEIGHT_THRESH):
            if C.POSE_DEBUG: print(f"Height_Reject: ID{rel_tag_pose_dict['ID']}, Tag_H:{rel_tag_pose_dict['y']}, Field_H:{C.AT_HEIGHTS_M[rel_tag_pose_dict['ID']]}")
            valid = False
        else:
            if (abs(rel_tag_pose_dict['roll']) > C.AT_ROLL_THRESH):
                if C.POSE_DEBUG: print(f"Roll_Reject: ID{rel_tag_pose_dict['ID']}, Tag_Roll:{rel_tag_pose_dict['roll']}")
                valid = False
        return valid
    
    def _get_pose(self, result, intrinsics, cam_x_pos, cam_y_pos, cam_z_pos, cam_pitch, cam_yaw, cam_rot_matrix): #return (x,y,z,ax,ay,az)
        pose = [
            [ 6.10479750e-01, -1.86923614e-01, -7.69658390e-01, -3.85752478e+02],
            [ 4.17101512e-01,  9.01959509e-01,  1.11782704e-01,  1.55553878e+02],
            [ 6.73305877e-01, -3.89266755e-01,  6.28594137e-01,  1.39231544e+03],
            [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]
        ]
        
        
        #pose, init_err, final_error = self._detector.detection_pose(result, intrinsics, C.AT_SIZE_MM) #at_size=145mm #PROBLEM LINE
        TAG_X_RAW, TAG_Y_RAW, TAG_Z_RAW = _get_tag_xyz(pose)
        TAG_AX_RAW, TAG_AY_RAW, TAG_AZ_RAW = _get_tag_angles(pose)
        point = np.array([[TAG_X_RAW], [TAG_Y_RAW], [TAG_Z_RAW]])
        rotated_pose = np.matmul(cam_rot_matrix, point).flatten()
        rotated_offset_pose = tuple(rotated_pose - (cam_x_pos, cam_y_pos, - cam_z_pos))
        rotated_angles = (TAG_AX_RAW - cam_pitch, TAG_AY_RAW + cam_yaw, TAG_AZ_RAW)
        return rotated_offset_pose + rotated_angles


   

def _get_tag_xyz(pose):
    # X_RAW = pose[0][3] / 1000
    # Y_RAW = pose[1][3] / 1000
    # Z_RAW = pose[2][3] / 1000
    return(pose[0][3] / 1000, pose[1][3] / -1000, pose[2][3] / 1000)

def _get_tag_angles(pose):
    R11 = pose[0][0]
    R12 = pose[0][1]
    R13 = pose[0][2]
    R21 = pose[1][0]
    R31 = pose[2][0]
    R32 = pose[2][1]
    R33 = pose[2][2]
    if R31 != 1 and R31 != -1: #trig function may be undefined - should never hit this in our application
        ay1 = -1*m.asin(R31)
        ax1 = m.atan2(R32 / m.cos(ay1), R33 / m.cos(ay1))
        az1 = m.atan2(R21 / m.cos(ay1), R11 / m.cos(ay1))
    else:
        az1 = 0
        if R31 == -1:
            ay1 = HALF_PI
            ax1 = az1 + m.atan2(R12, R13)
        else:
            ay1 = HALF_PI * -1
            ax1 = -1 * az1 + m.atan2(-1*R12, -1*R13)
    return(ax1, ay1, az1)






