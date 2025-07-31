# utils_robot.py
# 同济子豪兄 2024-5-22
# 启动并连接机械臂，导入各种工具包

print('导入机械臂连接模块')

import math
from libs.auxiliary import create_folder_with_date, get_ip, popup_message 
import cv2
import numpy as np
import time
from utils_pump import *


from Robotic_Arm.rm_robot_interface import *

robot = RoboticArm(rm_thread_mode_e.RM_TRIPLE_MODE_E)
handle = robot.rm_create_robot_arm("192.168.1.18", 8080)


Robot_speed=50

cap = cv2.VideoCapture(1)
cap.open(0)


def back_zero():
    '''
    机械臂归零
    '''
    print('机械臂归零')
    init = [0, 3, -10, 0, -90, 12]
    robot.rm_movej(init, Robot_speed, 0, 0, 1)  # 移动到0位姿

def head_shake():
    # 左右摆头
    #mc.send_angles([0.87,(-50.44),47.28,0.35,(-0.43),(-0.26)],70)
    init = [0, 3, -10, 0, -90, 12]
    robot.rm_movej(init, Robot_speed, 0,0,1)  # 移动到0位姿

    time.sleep(1)
    for count in range(2):
        init = [-25, 3, -8, 0, -90, 12]
        robot.rm_movej(init, Robot_speed,0,0,1)  # 移动到0位姿
        init = [-25, 3, -6, 53, -90, 12]
        robot.rm_movej(init, Robot_speed, 0,0,1)  # 移动到0位姿
    init = [0, 3, -10, 0, -90, 12]
    robot.rm_movej(init, Robot_speed, 0,0,1)  # 移动到0位姿

def head_dance():
    # 跳舞
    init = [0, 3, -10, 0, -90, 12]
    robot.rm_movej(init, Robot_speed, 0,0,1)  # 移动到位姿
    for count in range(1):
        robot.rm_movej([0, 33, -2, -7, -96, 12], Robot_speed, 0,0,1)  # 移动到位姿
        robot.rm_movej([0,-33, 61, -10, -84, 12], Robot_speed, 0,0,1)  # 移动到位姿
        robot.rm_movej([-57, -34, 58, -15, -78, 12], Robot_speed, 0,0,1)  # 移动到位姿
        robot.rm_movej([35, -24, 46, 3, -80, 12], Robot_speed, 0,0,1)  # 移动到位姿
        robot.rm_movej([37, 47,-93, -36,-74, 12], Robot_speed, 0,0,1)  # 移动到位姿

def head_nod():
    # 点头
    init = [0, 3, -10, 0, -90, 12]
    robot.rm_movej(init, Robot_speed, 0,0,1)  # 移动到位姿
    for count in range(2):
        robot.rm_movej([0, 3, -10, 0, -63, 12], Robot_speed, 0,0,1) # 移动到位姿
        robot.rm_movej(init, 10, 0,0,1)  # 移动到位姿
        robot.rm_movej([0, 3, -15, 0, -102, 12], Robot_speed,0,0,1)  # 移动到位姿
    robot.rm_movej(init, Robot_speed,0,0,1)  # 移动到位姿

def move_to_coords(X=0.24, Y=0, HEIGHT_SAFE=0.370):
    print('移动至指定坐标：X {} Y {}'.format(X, Y))
    robot.rm_movej_p([X, Y, HEIGHT_SAFE, 0, 0, 0], Robot_speed,0,0,1)

def single_joint_move(joint_index, angle):
    print('关节 {} 旋转至 {} 度'.format(joint_index, angle))
    status, current_pose= robot.rm_get_joint_degree()
    print("current_pose")
    print(current_pose)  # 打印当前位姿信息
    if joint_index==1:
       robot.rm_movej([angle, 
                        current_pose[1], 
                        current_pose[2], 
                        current_pose[3], 
                        current_pose[4], 
                        current_pose[5]], Robot_speed, 0,0,1)  # 移动到位姿
    if joint_index==2:
       robot.rm_movej([current_pose[0], 
                        angle, 
                        current_pose[2], 
                        current_pose[3], 
                        current_pose[4], 
                        current_pose[5]], Robot_speed, 0,0,1)  # 移动到位姿
    if joint_index==3:
       robot.rm_movej([current_pose[0], 
                        current_pose[1], 
                        angle, 
                        current_pose[3], 
                        current_pose[4], 
                        current_pose[5]], Robot_speed,0,0,1)  # 移动到位姿

    if joint_index==4:
       robot.rm_movej([current_pose[0], 
                        current_pose[1], 
                        current_pose[2], 
                        angle, 
                        current_pose[4], 
                        current_pose[5]], Robot_speed, 0,0,1)  # 移动到位姿
    if joint_index==5:
       robot.rm_movej([current_pose[0], 
                        current_pose[1], 
                        current_pose[2], 
                        current_pose[3], 
                        angle, 
                        current_pose[5]], Robot_speed, 0,0,1)  # 移动到位姿
    if joint_index==6:
       robot.rm_movej([current_pose[0], 
                        current_pose[1], 
                        current_pose[2], 
                        current_pose[3], 
                        current_pose[4], 
                        angle], Robot_speed, 0,0,1)  # 移动到位姿


def move_to_top_view():
    print('移动至俯视姿态')
    robot.rm_movej([0, -4, -81, 0, -92, 12], Robot_speed, 0,0,1)  # 移动到位姿
    pump_on()

def top_view_shot(check=False):
    '''
    拍摄一张图片并保存
    check：是否需要人工看屏幕确认拍照成功，再在键盘上按q键确认继续
    '''
    move_to_top_view()
    
    # 获取摄像头，传入0表示获取系统默认摄像头
    
    success, img_bgr = cap.read()
    
    # 保存图像
    print('    保存至temp/vl_now.jpg')
    cv2.imwrite('temp/vl_now.jpg', img_bgr)

    # 屏幕上展示图像
    cv2.destroyAllWindows()   # 关闭所有opencv窗口
    cv2.imshow('zihao_vlm', img_bgr) 
    
    if check:
        print('请确认拍照成功，按c键继续，按q键退出')
        while(True):
            #key = cv2.waitKey(10) & 0xFF
            #if key == ord('c'): # 按c键继续
                break
            #if key == ord('q'): # 按q键退出
                # exit()
               # cv2.destroyAllWindows()   # 关闭所有opencv窗口
                #raise NameError('按q退出')
    else:
        if cv2.waitKey(10) & 0xFF == None:
            pass
        
    # 关闭摄像头
    #cap.release()
    # 关闭图像窗口
    # cv2.destroyAllWindows()

def eye2hand(X_im, Y_im):
    '''
    输入目标点在图像中的像素坐标，转换为机械臂坐标
    '''

    # 整理两个标定点的坐标
    cali_1_im = [221,561]                       # 左下角，第一个标定点的像素坐标，要手动填！
    cali_1_mc = [230.454/1000.0, 163.154/1000.0]                  # 左下角，第一个标定点的机械臂坐标，要手动填！
    cali_2_im = [722,193]                         # 右上角，第二个标定点的像素坐标
    cali_2_mc = [337.237/1000.0, -3.9098/1000.0]                    # 右上角，第二个标定点的机械臂坐标，要手动填！
    
    X_cali_im = [cali_1_im[0], cali_2_im[0]]     # 像素坐标
    X_cali_mc = [cali_2_mc[1], cali_1_mc[1]]     # 机械臂坐标
    Y_cali_im = [cali_1_im[1], cali_2_im[1]]     # 像素坐标，先小后大
    Y_cali_mc = [cali_2_mc[1], cali_1_mc[1]]     # 机械臂坐标，先大后小

    # X差值
    X_mc = float(np.interp(X_im, X_cali_im, X_cali_mc))

    # Y差值
    Y_mc = float(np.interp(Y_im, Y_cali_im, Y_cali_mc))

    return X_mc, Y_mc


import numpy as np

def map_image_to_robot(x, y):
      # 标定点 - 图像坐标（像素）
    pts_img = np.float32([
        [25, 429],     # 点 A
        [133, 225],     # 点 B
        [442, 196],     # 点 C
    ])

    # 标定点 - 机械臂坐标（单位：米）
    pts_arm = np.float32([
        [197.539 / 1000.0, 186.841/ 1000.0],   # A
        [310.942 / 1000.0, 126.077 / 1000.0],   # B
        [334.373  / 1000.0, -50.772   / 1000.0],   # C
    ])

    # 计算仿射变换矩阵（2x3）
    M = cv2.getAffineTransform(pts_img, pts_arm)

    # 输入点
    input_point = np.array([[x, y]], dtype=np.float32)  # shape: (1, 2)
    input_point = np.expand_dims(input_point, axis=0)   # shape: (1, 1, 2)

    # 应用仿射变换
    transformed = cv2.transform(input_point, M)
    X, Y = transformed[0][0]
    return X, Y





# 吸泵吸取并移动物体
def pump_move(XY_START=[230,-50], HEIGHT_START=0.190, XY_END=[100,220], HEIGHT_END=0.205, HEIGHT_SAFE=0.370):

    '''
    用吸泵，将物体从起点吸取移动至终点

    mc：机械臂实例
    XY_START：起点机械臂坐标
    HEIGHT_START：起点高度，方块用90，药盒子用70
    XY_END：终点机械臂坐标
    HEIGHT_END：终点高度
    HEIGHT_SAFE：搬运途中安全高度
    '''
    
    # 吸泵移动至物体上方
    print('    吸泵移动至物体上方')
    robot.rm_movej_p([XY_START[0], XY_START[1], HEIGHT_SAFE, 3.14, 0, 0], Robot_speed,0,0,1)
    

    # 开启吸泵
    pump_off()
    time.sleep(1)

    # 吸泵向下吸取物体
    print('    吸泵向下吸取物体')
    robot.rm_movej_p([XY_START[0], XY_START[1], HEIGHT_START, 3.14, 0, 0], Robot_speed,0,0,1)
    

    
    pump_on()
    time.sleep(2)
    # 升起物体
    print('    升起物体')
    robot.rm_movej_p([XY_START[0], XY_START[1], HEIGHT_SAFE, 3.14, 0, 0], Robot_speed,0,0,1)

    # 搬运物体至目标上方
    print('    搬运物体至目标上方')
    robot.rm_movej_p([XY_END[0], XY_END[1], HEIGHT_SAFE, 3.14, 0, 0],  Robot_speed,0,0,1)

    # 向下放下物体
    print('    向下放下物体')
    robot.rm_movej_p([XY_END[0], XY_END[1], HEIGHT_END, 3.14, 0, 0],  Robot_speed,0,0,1)

    # 关闭吸泵
    pump_off()
    time.sleep(2)
    # 机械臂归零

    robot.rm_movej_p([XY_END[0], XY_END[1], HEIGHT_SAFE, 3.14, 0, 0],  Robot_speed,0,0,1)
    print('    机械臂归零')
    init = [0, 3, -10, 0, -90, 12]
    robot.rm_movej(init, Robot_speed, 0,0,1)  # 移动到0位姿
