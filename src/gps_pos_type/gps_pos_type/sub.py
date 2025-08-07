import rclpy
from rclpy.node import Node
from enum import IntEnum

# TODO: download the sbg driver msg types

from sbg_driver.msg import SbgGpsPos, SbgGpsPosStatus

class GpsPosType(IntEnum):
    NO_SOLUTION     = 0  # No valid solution available.
    UNKNOWN_TYPE    = 1  # An unknown solution type has been computed.
    SINGLE          = 2  # Single point solution position.
    PSRDIFF         = 3  # Standard Pseudorange Differential Solution (DGPS).
    SBAS            = 4  # SBAS satellite used for differential corrections.
    OMNISTAR        = 5  # Omnistar VBS Position (L1 sub-meter).
    RTK_FLOAT       = 6  # Floating RTK ambiguity solution (20 cms RTK).
    RTK_INT         = 7  # Integer RTK ambiguity solution (2 cms RTK).
    PPP_FLOAT       = 8  # Precise Point Positioning with float ambiguities
    PPP_INT         = 9  # Precise Point Positioning with fixed ambiguities
    FIXED           = 10 # Fixed location solution position


class TypeChecker(Node):
    def __init__(self):
        super().__init__("gps_pos_type_node")
        self.sub = self.create_subscription(
            SbgGpsPos,
            "sbg/gps_pos",
            self.type_sub,
            10
        )
    
    def type_sub(self, msg: SbgGpsPos):
        currentStatus = GpsPosType(msg.status.type)

        # This should only run for the inital received message and at start up
        if (currentStatus == GpsPosType.NO_SOLUTION):
            self.get_logger().warn(f"GPS Status: {currentStatus.name}", throttle_duration_sec = 1)
        elif (currentStatus == GpsPosType.UNKNOWN_TYPE):
            self.get_logger().error(f"GPS Status: {currentStatus.name}", throttle_duration_sec = 1)
        else:
            self.get_logger().info(f"GPS Status: {currentStatus.name}", throttle_duration_sec = 5)
    

def main():
    rclpy.init()
    node = TypeChecker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        node.get_logger().fatal(f"Encountered fatal error: {e}")
    
    node.destroy_node()
    rclpy.shutdown()