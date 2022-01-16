#!/usr/bin/env python3

import csv
import rospy

from datetime import datetime
from geometry_msgs.msg import PoseStamped


class MsgWriter():
    def __init__(self):
        rospy.init_node('msg_writer', anonymous=True)

        time_at_init = datetime.now().strftime("%H-%M-%S")
        filename = 'data_' + time_at_init + '.csv'

        # Launch file params
        topic_to_write = rospy.get_param("~topic_to_write")
        msg_type = rospy.get_param("~msg_type")
        output_dir = rospy.get_param("~output_dir")

        # Class variables
        self.filepath = output_dir + '/' + filename
        self.sub = None

        if msg_type == "PoseStamped":
            self.write_header(pose_msg_header())
            self.sub = rospy.Subscriber(topic_to_write, PoseStamped, self.iterable_cb)


    def iterable_cb(self, msg):
        print(dict(msg))

        for thing in msg:
            print("This is a THING:")
            print(thing)

    def writer_cb(self, msg):
        row = pose_msg_to_row(msg)
        self.write_msg_row(row)

    def write_header(self, header: tuple):
        # Write header of data###.csv file
        with open(self.filepath, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(header)
        csv_file.close()

    def write_msg_row(self, row):
        # Append row to data.csv file
        with open(self.filepath, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(row)
        csv_file.close()


def pose_msg_header():
    return ["hdr_seq", "hdr_stmp_sec", "hdr_stmp_nsec", "hdr_frm_id",
            "pos_x", "pos_y", "pos_z",
            "rot_x", "rot_y", "rot_z", "rot_w"]


def pose_msg_to_row(msg):
    hdr_seq = msg.header.seq
    hdr_stmp_sec = msg.header.stamp.secs
    hdr_stmp_nsec = msg.header.stamp.nsecs
    hdr_frm_id = msg.header.frame_id

    pos_x = msg.pose.position.x
    pos_y = msg.pose.position.y
    pos_z = msg.pose.position.z

    rot_x = msg.pose.orientation.x
    rot_y = msg.pose.orientation.y
    rot_z = msg.pose.orientation.z
    rot_w = msg.pose.orientation.w

    return [str(hdr_seq), str(hdr_stmp_sec), str(hdr_stmp_nsec), str(hdr_frm_id),
            str(pos_x), str(pos_y), str(pos_z),
            str(rot_x), str(rot_y), str(rot_z), str(rot_w)]


if __name__ == "__main__":
    node = MsgWriter()

    try:
        rospy.spin()
    except KeyboardInterrupt:  # Press Ctrl+c on keyboard to exit.
        print("Shutting down...")
