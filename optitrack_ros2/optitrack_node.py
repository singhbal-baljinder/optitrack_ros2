
import numpy as np

from NatNetSDKPython.NatNetClient import *
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose, Quaternion, PoseArray
import threading  

class OptitrackNode(Node):
    def __init__(self, server_address ="", client_address="", use_multicast=False, topic_name=""):
        super().__init__('OptitrackPublisher')

        self.server_address = server_address
        self.client_address = client_address
        self.use_multicast = use_multicast
        self.positions = {}
        self.quaternions = {}    
        self._lock = threading.Lock() # Protects the dictionaries
        # NatNet runs a client that populates the positions and quaternions variables
        self.streaming_client = NatNetClient()
        self.streaming_client.set_client_address(self.client_address)
        self.streaming_client.set_server_address(self.server_address)
        self.streaming_client.set_use_multicast(self.use_multicast)
        self.streaming_client.run()
        self.streaming_client.rigid_body_listener = self.receive_rigid_body_frame

        # A ROS publisher that exposes the optitrack frames as an array of Pose msgs
        self.publisher_ = self.create_publisher(PoseArray, 'optitrack_frames', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def receive_rigid_body_frame(self, new_id, position, rotation):
        """Called by the background NatNet thread."""
        with self._lock:  # Ensure we aren't writing while ROS is reading
            self.positions[new_id] = position
            self.quaternions[new_id] = rotation

            print(self.positions)

    def timer_callback(self):
        """Called by the main ROS thread."""
        # Use a lock to take a quick "snapshot" of the data
        with self._lock:
            if not self.positions:
                return
            # Create copies to iterate over safely
            current_positions = dict(self.positions)
            current_quaternions = dict(self.quaternions)

        msg = PoseArray()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "optitrack"
        
        poses_list = []
        for rb_id in current_positions.keys():
            p = Pose()
            pos = current_positions[rb_id]
            rot = current_quaternions[rb_id]

            p.position.x = float(pos[0])
            p.position.y = float(pos[1])
            p.position.z = float(pos[2])

            p.orientation.x = float(rot[0])
            p.orientation.y = float(rot[1])
            p.orientation.z = float(rot[2])
            p.orientation.w = float(rot[3])
            
            poses_list.append(p)
            
        msg.poses = poses_list

        # Publish message
        self.publisher_.publish(msg)

    def shutdown_client(self):
            self.get_logger().info('Shutting down NatNet Client...')
            # Most NatNetSDK implementations have a shutdown or stop method
            self.streaming_client.shutdown()

def main(args=None):
    rclpy.init(args=args)
    
    # Initialize your node
    node = OptitrackNode(server_address="169.254.164.223", client_address="169.254.164.224")
    
    try:
        # Keep the node alive and processing callbacks
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Stop the external NatNet thread BEFORE touching ROS node
        # This is the most likely cause of the "hang"
        if hasattr(node, 'streaming_client'):
            print("Shutting down NatNet Client...") # Use print instead of get_logger
            node.streaming_client.shutdown() 
        
        # Now safely destroy the node
        node.destroy_node()
        
        # Finally shutdown ROS
        if rclpy.ok():
            rclpy.shutdown()
        print("ROS 2 Shutdown complete.")
if __name__ == '__main__':
    main()
