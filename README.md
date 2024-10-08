# Drowsy Detection
This repo is a PoC for using Jetson Nano and camera to detect drowsiness. It follow the guideline https://github.com/dusty-nv/jetson-inference

# Prerequisites
- Hardware: Jetson Orin NX module, camera
- Software: Jetpack 5.1.3, python 3.8.10, torch 2.1 ([link](https://developer.download.nvidia.com/compute/redist/jp/v512/pytorch/torch-2.1.0a0+41361538.nv23.06-cp38-cp38-linux_aarch64.whl)), torchvision 0.16 ([link](https://download.pytorch.org/whl/torchvision-0.16.0-cp38-cp38-linux_aarch64.whl))
# Dataset
- Labeling and annotating on Roboflow https://roboflow.com/
- Export to VOC format (refer dataset.zip)
# Prepare
- Clone the repo at : https://github.com/dusty-nv/jetson-inference
- Build project, refer guideline https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo.md
- Add dataset folder to data folder
# Training
- ```cd jetson-inference/python/training/detection/ssd```
- Run: ```python train_ssd.py --dataset-type=voc```
  ![training_process_image](https://github.com/user-attachments/assets/9e6a4c63-1a4d-4e5d-af75-643dcc63e29c)
After completing the traning process, the model will be stored at models
- Export onnx: ```python onnx_export.py --model-dir=models --labels=models/labels.txt```

# Inference with live cam
- Copy ```ssd_inference.py``` to ```jetson-inference/python/training/detection/ssd```
- ```cd jetson-inference/python/training/detection/ssd```
- I'm using usb camera, so URI of the input stream is ```/dev/video0```
- Inference with live camera: ```python ssd_inference.py /dev/video0```
  ![inference_image](https://github.com/user-attachments/assets/cea6774d-7c7b-48a0-9bc9-f8eff76bb50d)

