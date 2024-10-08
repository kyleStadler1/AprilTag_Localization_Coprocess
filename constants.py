#Constants page for AT-Localization-2024
#If constant var ends with '_' its meant to be private to this page only


#Camera Constants
IMG_WIDTH=1280
IMG_HEIGHT=720
FPS=120
    #Intrinsics - EACH CAMERA/RES IS DIFFERENT
A_1280x720_=(736.7768191440488,736.2961055601097, 677.4377656155549, 415.6514377281292)
B_1280x720_=(681.5075313929896, 679.8204600575391, 698.4064829330795, 444.0096508816774)
C_1280x720_=(777.9858077469355, 787.865785962896,693.6964019087006,363.42498640499366)
D_1280x720_=(774.1742415627957, 772.7421443141125, 690.9956504165392,359.0690284333276)
E_1280x720_=(783.4822537032863, 806.9585559642111, 656.6550441716648, 399.12438106905194)



#Camera pose from center of robot: {x,y,z,yaw,pitch} 
#pitch UP = +
#yaw CLOCKWISE = +
FRONT_CAM_SPECS = {
    'name' : "cam_front",
    'addr' : '/dev/video0',
    'intrinsics' : A_1280x720_,
    'x' : 0,
    'y' : 0,
    'z' : 0,
    'pitch' : 0,
    'yaw' : 0
}

REAR_CAM_SPECS = {
    'name' : "cam_rear",
    'addr' : '/dev/video2',
    'intrinsics' : A_1280x720_,
    'x' : 0,
    'y' : 0,
    'z' : 0,
    'pitch' : 0,
    'yaw' : 0
}


#Detector Constants
CONFIDENCE_THRESH=30
AT_FAMILY='tag36h11'#'tag36h11'
DETECTOR_DEBUG=False
    #dont mess with these
BORDER=1 #min pixel for boarder
NTHREADS=1
QUAD_DECIMATE=2 #higher = faster, less accurate
QUAD_BLUR=0.0
REFINE_EDGES=True
REFINE_DECODE=True
REFINE_POSE=True
QUAD_CONTOURS=True #false makes a lot of small false positives
    #

#FRC 2024 Field Specific Constants
VALID_IDS=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)
AT_SIZE_MM=165.1
AT_HEIGHTS_M = {
        #plastic mounted: 266.7mm outer square plate, half: 133.35mm
        #metal mounted: 228.6mm outer square plate, half: 114.3mm
    1 : 1.355725, #SOURCE
    2 : 1.355725, #SOURCE
    9 : 1.355725, #SOURCE
    10 : 1.355725, #SOURCE
    3 : 1.450975, #SPEAKER
    4 : 1.450975, #SPEAKER
    7 : 1.450975, #SPEAKER
    8 : 1.450975, #SPEAKER
    5 : 1.355725, #AMP
    6 : 1.355725, #AMP
    11 : 1.3208, #STAGE
    12 : 1.3208, #STAGE
    13 : 1.3208, #STAGE
    14 : 1.3208, #STAGE
    15 : 1.3208, #STAGE
    16 : 1.3208, #STAGE 
}
AT_HEIGHT_THRESH = 9000.5 #meters 
AT_ROLL_THRESH = 9 #rads (10deg)

#Multiprocess Pipe Constants
PIPE_TIMEOUT = 0.001
RECV_BUF_SIZE = 5 #in pose unites AKA the buf will hold n poses

#Socket Constants
HOST='stadlerpi.local'
PORT=5590
SENDBUF=8192
RIOHOST='google.com'

#Debug Print Modes
CAM_DEBUG_STAT = True
CAM_DEBUG_ERR = True
PIPE_DEBUG = False
POSE_DEBUG = True
SOCKET_DEBUG = False

#DONT USE
UC10MPC_INTRINSIC_95 = (603.4989347246805, 607.8401692891746, 522.8554938311737, 279.0464033043424)


