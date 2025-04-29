# S2A - Loss Visualization

Official implementation of S2A-Attention for Multimodal 3D Semantic Segmentation Using LiDAR and Cameras in Autonomous Driving, with integrated loss visualization tools.

## Project Overview

S2A is a multimodal 3D semantic segmentation method for autonomous driving scenarios that uses LiDAR and camera data. This project not only implements the S2A model but also provides loss visualization tools to help researchers better understand and analyze the training process.

![Model Architecture](https://github.com/user-attachments/assets/cf3ad712-6115-47e2-8bef-7bac44844cbd)

## Key Features

- **Multimodal 3D Semantic Segmentation**: LiDAR and camera fusion method based on S2A-Attention
- **Loss Visualization**: Tools for visualizing various loss changes during training
- **Multiple Loss Functions**: Support for Cross-Entropy Loss, Lovasz Loss, and more
- **Model Inference & Evaluation**: Pre-trained models and inference evaluation tools

## Installation Guide

1. Clone the repository:
```bash
git clone https://github.com/yourusername/S2A.git
cd S2A
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Setup environment:
```bash
bash setup.sh
```

## Running Guide

### Data Preparation

1. Download the dataset:
```bash
python tools/download_dataset.py --dataset waymo --output_dir data/
```

2. Data preprocessing:
```bash
python tools/preprocess_data.py --dataset_dir data/waymo --output_dir data/waymo_processed
```

### Model Training

1. Single GPU training:
```bash
python tools/train.py --config configs/s2a_waymo.yaml --work_dir work_dirs/s2a_waymo
```

2. Multi-GPU training:
```bash
bash scripts/dist_train.sh configs/s2a_waymo.yaml 8
```

### Model Testing and Evaluation

```bash
python tools/test.py --config configs/s2a_waymo.yaml --checkpoint work_dirs/s2a_waymo/latest.pth --eval mIoU
```

### Usage

Loss values are automatically recorded during training and can be visualized with the following command:
```bash
python tools/visualize_loss.py --logdir path/to/logs
```

## Model Evaluation & Inference

A simple inference example is provided:
```bash
python tools/simple_inference_waymo.py --config CONFIG_PATH --checkpoint CHECKPOINT_PATH --input_data_dir INPUT_DIR --output_dir OUTPUT_DIR --visual
```
