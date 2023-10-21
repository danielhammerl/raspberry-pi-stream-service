#!/bin/bash
libcamera-vid -t 0 --mode=1024:786:10 --framerate 20 --inline -o - | cvlc stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/stream}' :demux=h264