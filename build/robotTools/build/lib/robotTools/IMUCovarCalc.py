import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
import numpy as np
import transforms3d as maths
import statistics as stat

class PythonStats(Node):
    def __init__(self):
        super().__init__("IMUCovarCalc")
        self.covarData = {
            "orientation_roll" : [],
            "orientation_pitch" : [],
            "orientation_yaw" : [],

            "accel_x" : [],
            "accel_y" : [],
            "accel_z" : [],

            "vel_x" : [],
            "vel_y" : [],
            "vel_z" : []
        }
        self.trialNum = 0
        self.subscription = self.create_subscription(
            Imu,
            "/drive/imu",
            self.listener_callback,
            15
        )

    def listener_callback(self, msg):
        if(self.trialNum < 1000):
            rpy = maths.euler.quat2euler([msg.orientation.w, msg.orientation.x, msg.orientation.y, msg.orientation.z])
            self.covarData["orientation_roll"].append(rpy[0])
            self.covarData["orientation_pitch"].append(rpy[1])
            self.covarData["orientation_yaw"].append(rpy[2])

            self.covarData["accel_x"].append(msg.linear_acceleration.x)
            self.covarData["accel_y"].append(msg.linear_acceleration.y)
            self.covarData["accel_z"].append(msg.linear_acceleration.z)

            self.covarData["vel_x"].append(msg.angular_velocity.x)
            self.covarData["vel_y"].append(msg.angular_velocity.y)
            self.covarData["vel_z"].append(msg.angular_velocity.z)
        else:
            Ovars = [stats.variance(self.covarData[orientation_roll]), stats.variance(self.covarData[orientation_pitch]), stats.variance(self.covarData[orientation_yaw])]
            Avars = [stats.variance(self.covarData[accel_x]), stats.variance(self.covarData[accel_y]), stats.variance(self.covarData[accel_z])]
            Vvars = [stats.variance(self.covarData[vel_x]), stats.variance(self.covarData[vel_y]), stats.variance(self.covarData[vel_z])]
            print("Orientation covar matrix: {} \n".format(Ovars))
            print("Orientation covar matrix: {} \n".format(Avars))
            print("Orientation covar matrix: {} \n".format(Vvars))
            self.trialNum = 0

        



def main(args = none):
    print('Something valuable')
    rclpy.init(args=args)
    pythonStats = PythonStats()
    rclpy.spin(pythonStats)
    pythonStats.destroy_node()
    rclpy.shutdown()
    

if __name__ == '__main__':
    main()
