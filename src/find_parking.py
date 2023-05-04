#!/usr/bin/env python3

import rospy, math
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import tf2_ros

class FindParking:
    def __init__(self):
        rospy.init_node('find_parking')
        rospy.loginfo("Node Started")
        self.client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        self.cmd_pub = rospy.Publisher("/catvehicle/cmd_vel", Twist, queue_size=10)
        self.client.wait_for_server()
        self.goal = MoveBaseGoal()
        self.goal.target_pose.header.frame_id = "map"
        rospy.Subscriber("/catvehicle/front_laser_points", LaserScan, self.laser_callback)
        self.got_parking = False
        self.tfBuffer = tf2_ros.Buffer()
        self.listener = tf2_ros.TransformListener(self.tfBuffer)
   
    
    def laser_callback(self, msg):

        # rospy.sleep(rospy.Duration(5.0))
        # msg = LaserScan()
        # print("len ", len(msg.ranges))
        # print("left", msg.ranges[0])
        # print("center", msg.ranges[90])
        # print("right", msg.ranges[179])
        angle_min = msg.angle_min
        angle_increment = msg.angle_increment
        angles = []
        ranges = []
        for idx, item in enumerate(msg.ranges):
            angle = angle_min + idx * angle_increment
            if (angle > 0.0):
                if (not math.isinf((item))):
                    angles.append(angle)
                    ranges.append(item)
        
        for i in range(1,len(angles)):
            ang_diff = angles[i] - angles[i-1]
            if (ang_diff > 0.7 and ranges[i] > 3.0):
                self.got_parking = True
                rospy.sleep(rospy.Duration(2.0))

                twist = Twist()
                self.cmd_pub.publish(twist)

                x = (ranges[i]) * math.sin(angles[i])  + 1.0
                y = (ranges[i-1]) * math.cos(angles[i-1]) - 3.0
                # print('range i', ranges[i])
                # print('range i-1', ranges[i-1])
                # print('x', x)
                # print('y', y)
                try:
                    trans = self.tfBuffer.lookup_transform('map', 'catvehicle/base_link', rospy.Time(), rospy.Duration((3)))
                    # print('x', trans.transform.translation.x)
                    # print('y', trans.transform.translation.y)
                except:
                    print('error')

                self.goal.target_pose.pose.position.x = y + trans.transform.translation.x
                self.goal.target_pose.pose.position.y = x + trans.transform.translation.y
                print("parking found")
                self.goal.target_pose.pose.orientation.x = 0.0
                self.goal.target_pose.pose.orientation.y = 0.0
                self.goal.target_pose.pose.orientation.z = 0.0
                self.goal.target_pose.pose.orientation.w = 1.0
                print(self.goal.target_pose.pose)

                self.goal.target_pose.header.stamp = rospy.Time.now()
                rospy.loginfo("goal send")
                self.client.send_goal_and_wait(self.goal)
                rospy.loginfo("goal done")
                rospy.signal_shutdown("goal done")

    
    def run(self):
        rate = rospy.Rate(10) # 10 hz
        twist = Twist()
        twist.linear.x = 0.5
        print("Moving Car Forward")

        while not rospy.is_shutdown():
            # move forward until robot finds parking
            if not self.got_parking:
                self.cmd_pub.publish(twist)
            rate.sleep()
        pass

def main():
    find_parking = FindParking()
    find_parking.run()

if __name__ == '__main__':
    main()
        
