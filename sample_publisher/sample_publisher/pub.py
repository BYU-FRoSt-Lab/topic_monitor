import rclpy
from rclpy.node import Node

# Sensor imports
from sensor_msgs.msg import NavSatFix

class SamplePublisher(Node):
    def __init__(self):
        super().__init__('sample_publisher')
        period = 0.1
        self.timer = self.create_timer(period, self.timer_callback)
        self.i = 0
        self.publisher = self.create_publisher(NavSatFix, "sample_nav_sat_fix", 10)

    def timer_callback(self):
        msg = NavSatFix()
        # Populate
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = f"{self.i}"
        msg.latitude =  0.0
        msg.longitude = 0.0
        msg.altitude =  0.0
        msg.position_covariance_type = 0

        self.publisher.publish(msg)
        self.get_logger().info(f"Publishing frame {self.i}", throttle_duration_sec=5)

        self.i += 1


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
