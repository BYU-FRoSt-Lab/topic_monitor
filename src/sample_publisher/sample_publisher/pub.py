import rclpy
from rclpy.node import Node

# Sensor imports
from sensor_msgs.msg import NavSatFix, Imu

class SamplePublisher(Node):
    def __init__(self):
        super().__init__('sample_publisher')
        period = 0.1
        self.timer = self.create_timer(period, self.publish_nav_sat_fix)
        self.timer = self.create_timer(period, self.publish_imu)

        self.nav_sat_fix_count = 0
        self.nav_sat_fix_pub = self.create_publisher(NavSatFix, "sample_nav_sat_fix", 10)

        self.imu_count = 0
        self.imu_pub = self.create_publisher(Imu, "sample_imu", 10)

    def publish_nav_sat_fix(self):
        msg = NavSatFix()
        # Populate
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = f"{self.nav_sat_fix_count}"
        msg.latitude =  0.0
        msg.longitude = 0.0
        msg.altitude =  0.0
        msg.position_covariance_type = 0

        self.nav_sat_fix_pub.publish(msg)
        self.get_logger().info(f"Publishing frame {self.nav_sat_fix_count}", throttle_duration_sec=5)

        self.nav_sat_fix_count += 1

    def publish_imu(self):
        msg = Imu()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = f"{self.imu_count}"
        self.imu_pub.publish(msg)
        self.get_logger().info(f"Publishing frame {self.imu_count}", throttle_duration_sec=5)
        self.imu_count += 1



def main():
    rclpy.init()
    
    node = SamplePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down from Keyboard Interrupt")
    except Exception as e:
        node.get_logger().warn(f"Unknown error encountered: {e}")

    node.destroy_node()
    rclpy.shutdown()
