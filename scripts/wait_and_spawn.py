#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
import rclpy
from rclpy.node import Node
from rosgraph_msgs.msg import Clock


class WaitForGazeboAndSpawn(Node):
    def __init__(self, entity, spawn_cmd):
        super().__init__('wait_for_gazebo_and_spawn')
        self.entity = entity
        self.spawn_cmd = spawn_cmd
        self.clock_received = False
        self.create_subscription(Clock, '/clock', self.clock_cb, 10)
        self.get_logger().info('Waiting for /clock from Gazebo...')

    def clock_cb(self, msg):
        # First clock message indicates Gazebo simulation started
        if not self.clock_received:
            self.clock_received = True
            self.get_logger().info('/clock received, spawning entity...')
            # call spawn_entity via ros2 run
            try:
                subprocess.run(self.spawn_cmd, check=False)
            except Exception as e:
                self.get_logger().error(f'Failed to run spawn command: {e}')
            finally:
                # shutdown after attempting spawn
                rclpy.shutdown()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--entity')
    parser.add_argument('-file')
    args = parser.parse_args()

    # Build the ros2 run command to spawn the entity (uses gazebo_ros package script)
    spawn_cmd = [
    'ros2', 'run', 'gazebo_ros', 'spawn_entity.py', 
    '-entity', args.entity,
    '-file', args.file,
    ]

    rclpy.init()
    node = WaitForGazeboAndSpawn(args.entity, spawn_cmd)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
