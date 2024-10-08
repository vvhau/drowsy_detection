#!/usr/bin/env python3
#
# This inference reuses sample code published in Nvidia dusty-nv github repo 

import sys
import argparse

import time
import Jetson.GPIO as GPIO
# import cv2
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, Log

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, 
                                 epilog=detectNet.Usage() + videoSource.Usage() + videoOutput.Usage() + Log.Usage())
                                 
parser.add_argument("input", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 

try:
	args = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

# "/dev/video0"
input = videoSource(args.input, argv=sys.argv)

output = videoOutput(args.output, argv=sys.argv)
    

net = detectNet(model="models/ssd-mobilenet.onnx", labels="models/labels.txt", input_blob="input_0", output_cvg="scores", 
                    output_bbox="boxes", threshold=0.5)

# process frames until EOS or the user exits
# Led pin for plastic, metal
led_pin11 = 11

# Led pin for garbage

# Set up the GPIO channel
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(led_pin11, GPIO.OUT, initial=GPIO.LOW)

while True:
    

    # capture the next image
    img = input.Capture()

    if img is None: # timeout
        GPIO.output(led_pin11, GPIO.LOW)
        continue
        
    # detect objects in the image (with overlay)
    detections = net.Detect(img, overlay="box,labels,conf")

    # print the detections
    print("detected {:d} objects in image".format(len(detections)))
    
    is_drowsy = False
    for detection in detections:
        print(detection)
        classLabel = net.GetClassLabel(detection.ClassID)
        print(f'label: {classLabel}')
        if 'drowsy'.__eq__(classLabel):
          is_drowsy = True

    # render the image
    output.Render(img)
    # update the title bar
    output.SetStatus("{:s} | Network {:.0f} FPS".format("ssd-mobilenet-v2", net.GetNetworkFPS()))
    
    if is_drowsy == True:
        print("Drowsy detected")
        GPIO.output(led_pin11, GPIO.HIGH) 
        print("RED_LED is ON")
    else:
        print("RED_LED is OFF")
        GPIO.output(led_pin11, GPIO.LOW)

    # net.PrintProfilerTimes()

    # exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():
        break
