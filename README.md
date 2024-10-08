# Drowsy Detection
This repo is a PoC for using Jetson Nano and camera to detect drowsiness. It follow the guideline https://github.com/dusty-nv/jetson-inference

# Prerequisites
- Hardware: Jetson Orin NX module, camera
- Software: Jetpack 5.1.3, python 3.8.10, torch 2.1, torchvision 0.16
# Dataset
- Labeling and annotating on Roboflow https://roboflow.com/
- Export to VOC format (refer dataset.rar)
# Training
- Clone the repo at : https://github.com/dusty-nv/jetson-inference
- ```cd jetson-inference/python/training/detection/ssd```
- Add dataset folder to data folder
- Run: ```python train_ssd.py --dataset-type=voc```
After completing the traning process, the model will be stored at models
- Export onnx: ```python onnx_export.py --model-dir=models --labels=models/labels.txt```
- Inference with live camera: ```python ssd_inference.py /dev/video0```
# Training process
image

# Inference with live cam
image
