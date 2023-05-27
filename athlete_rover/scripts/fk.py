import rospy
import time
from std_msgs.msg import Float64
import numpy as np
from threading import Thread

def foward_kinematics():
    pub_link_one = rospy.Publisher('/pipla_bot/link_one_ctrl/command', Float64, queue_size=10)
    pub_link_two = rospy.Publisher('/pipla_bot/link_two_ctrl/command', Float64, queue_size=10)
    pub_link_three = rospy.Publisher('/pipla_bot/link_three_ctrl/command', Float64, queue_size=10)
    pub_link_four = rospy.Publisher('/pipla_bot/link_four_ctrl/command', Float64, queue_size=10)
    rospy.init_node('straight_line_pub', anonymous=True)
    rate = rospy.Rate(50) # 50hz

    def first_link():
        for i in np.arange(0,1.8,0.1):
            pub_link_one.publish(i)
            print("Steering Velocity: ", i)
            time.sleep(0.1)
            rate.sleep()
    def second_link():
        for i in np.arange(0,-1,-0.1):
            pub_link_two.publish(i)
            print("Steering Velocity: ", i)
            time.sleep(0.1)
            rate.sleep()

    def third_link():
        for i in np.arange(0,1.3,0.2):
            pub_link_three.publish(i)
            print("Steering Velocity: ", i)
            time.sleep(0.1)
            rate.sleep()
    def fourth_link():
        for i in np.arange(0,-1.4,-0.1):
            pub_link_four.publish(i)
            print("Steering Velocity: ", i)
            time.sleep(0.1)
            rate.sleep()           

    
    while not rospy.is_shutdown():
        print("Commanding Velocity")
        t1 = Thread(target = first_link)
        t2 = Thread(target = second_link)
        t3 = Thread(target = third_link)
        t4 = Thread(target = fourth_link)

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        break

if __name__ == '__main__':
    try:
        foward_kinematics()
    except rospy.ROSInterruptException:
        pass
