#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
import math
import sys, select, termios, tty
from threading import Thread

joints = ['coxa','femur','tibia','pitch','roll','wheel']
sides = ['l', 'r']
legs = []
leg = []
for i in range(6):
    for j in joints:
        z = '/athlete_rover/' + j + '_' + str(i+1) + '_controller/command'
        leg.append(rospy.Publisher(z,Float64,queue_size=10))
    legs.append(leg)
    leg = []

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def joint_pos_pub(joint, pos):
    joint.publish(pos)
    return

def wheel_vel_pub(wheel, vel):
    wheel.publish(vel)
    return 

def leg_publisher(leg,coxa_pos, femur_pos, tibia_pos, pitch_pos, roll_pos):
    leg[0].publish(coxa_pos)
    leg[1].publish(femur_pos)
    leg[2].publish(tibia_pos)
    leg[3].publish(pitch_pos)
    leg[4].publish(roll_pos)
    return

def legs_publisher(legs,joint_states):
    if not rospy.is_shutdown():
        leg_publisher(legs[0],joint_states[0][0],joint_states[0][1],joint_states[0][2],joint_states[0][3],joint_states[0][4])
        leg_publisher(legs[1],joint_states[1][0],joint_states[1][1],joint_states[1][2],joint_states[1][3],joint_states[1][4])
        leg_publisher(legs[2],joint_states[2][0],joint_states[2][1],joint_states[2][2],joint_states[2][3],joint_states[2][4])
        leg_publisher(legs[3],joint_states[3][0],joint_states[3][1],joint_states[3][2],joint_states[3][3],joint_states[3][4])
        leg_publisher(legs[4],joint_states[4][0],joint_states[4][1],joint_states[4][2],joint_states[4][3],joint_states[4][4])
        leg_publisher(legs[5],joint_states[5][0],joint_states[5][1],joint_states[5][2],joint_states[5][3],joint_states[5][4])
    return

def home():
    leg1_joints = [math.radians(0),math.radians(0),math.radians(0),math.radians(0),math.radians(0)]
    leg2_joints = [math.radians(0),math.radians(0),math.radians(0),math.radians(0),math.radians(0)]
    leg3_joints = [math.radians(0),math.radians(0),math.radians(0),math.radians(0),math.radians(0)]
    leg4_joints = [math.radians(0),math.radians(0),math.radians(0),math.radians(0),math.radians(0)]
    leg5_joints = [math.radians(0),math.radians(0),math.radians(0),math.radians(0),math.radians(0)]
    leg6_joints = [math.radians(0),math.radians(0),math.radians(0),math.radians(0),math.radians(0)]
    all_joints = [leg1_joints,leg2_joints,leg3_joints,leg4_joints,leg5_joints,leg6_joints]
    legs_publisher(legs,all_joints)

def athlete_stand():
    leg1_joints = [math.radians(0),math.radians(-90),math.radians(70),math.radians(35),math.radians(0)]
    leg2_joints = [math.radians(0),math.radians(-90),math.radians(70),math.radians(35),math.radians(0)]
    leg3_joints = [math.radians(0),math.radians(-90),math.radians(70),math.radians(35),math.radians(0)]
    leg4_joints = [math.radians(0),math.radians(-90),math.radians(70),math.radians(35),math.radians(0)]
    leg5_joints = [math.radians(0),math.radians(-90),math.radians(70),math.radians(35),math.radians(0)]
    leg6_joints = [math.radians(0),math.radians(-90),math.radians(70),math.radians(35),math.radians(0)]
    all_joints = [leg1_joints,leg2_joints,leg3_joints,leg4_joints,leg5_joints,leg6_joints]
    legs_publisher(legs,all_joints)
    leg1_joints = [math.radians(0),math.radians(30),math.radians(30),math.radians(30),math.radians(0)]
    leg2_joints = [math.radians(0),math.radians(30),math.radians(30),math.radians(30),math.radians(0)]
    leg3_joints = [math.radians(0),math.radians(30),math.radians(30),math.radians(30),math.radians(0)]
    leg4_joints = [math.radians(0),math.radians(30),math.radians(30),math.radians(30),math.radians(0)]
    leg5_joints = [math.radians(0),math.radians(30),math.radians(30),math.radians(30),math.radians(0)]
    leg6_joints = [math.radians(0),math.radians(30),math.radians(30),math.radians(30),math.radians(0)]
    all_joints = [leg1_joints,leg2_joints,leg3_joints,leg4_joints,leg5_joints,leg6_joints]
    legs_publisher(legs,all_joints)
    return

def commander():
    while not rospy.is_shutdown():
        key_press = getKey()
        if key_press == 'u':
            athlete_stand()
        elif key_press == 'h':
            home()
        elif key_press == 'c':
            break
    return

if __name__ == '__main__':
    # it is good practice to maintain
    settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('athlete_commander')
    rospy.loginfo("athlete commander node initiated")
    # a 'try'-'except' clause
    try:
        commander()
    except Exception as e:
        print(e)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)