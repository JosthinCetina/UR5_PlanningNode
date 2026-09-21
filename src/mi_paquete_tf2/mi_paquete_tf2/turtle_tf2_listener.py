import math
import rclpy
from rclpy.node import Node
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from geometry_msgs.msg import Twist

class FrameListener(Node):
    def __init__(self):
        super().__init__('turtle_tf2_frame_listener')

        self.target_frame = self.declare_parameter('target_frame', 'carrot1').get_parameter_value().string_value
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.publisher = self.create_publisher(Twist, 'turtle2/cmd_vel', 1)
        self.timer = self.create_timer(0.1, self.on_timer)

    def on_timer(self):
        from_frame_rel = self.target_frame
        to_frame_rel = 'turtle2'

        try:
            t = self.tf_buffer.lookup_transform(
                to_frame_rel,
                from_frame_rel,
                rclpy.time.Time())
        except TransformException as ex:
            self.get_logger().info(f'Esperando transformacion de {from_frame_rel} a {to_frame_rel}: {ex}')
            return

        msg = Twist()
        scale_rotation_rate = 1.0
        msg.angular.z = scale_rotation_rate * math.atan2(
            t.transform.translation.y,
            t.transform.translation.x)

        scale_forward_speed = 0.5
        msg.linear.x = scale_forward_speed * math.sqrt(
            t.transform.translation.x ** 2 +
            t.transform.translation.y ** 2)

        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = FrameListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
