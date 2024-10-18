# Deep Convolutional Generative Adversarial Network

# DCGAN for Synthetic Image Generation

This project implements a Deep Convolutional Generative Adversarial Network (DCGAN) to generate synthetic images for variety of datasets. The model is trained on different datasets using PyTorch. This repository contains the training code with modified hyperparameters for improved results.

## Table of Contents
- [Overview](#overview)
- [Dataset](#dataset)
- [Model Architecture](#model-architecture)
- [Requirements](#requirements)
- [Training](#training)
- [Testing](#testing)
- [Results](#results)
- [References](#references)

## Overview
This project focuses on generating black-and-white geometrical shapes using a DCGAN model. The hyperparameters have been tuned for better results, and the repository includes:
- DCGAN training script
- Model checkpoints saving mechanism
- Image generation with pre-trained weights

## Dataset
The dataset used for this project contains black-and-white images of LEGO geometrical shapes. The images are preprocessed using the following transformations:
- Grayscale conversion
- Resizing to 128x128 pixels
- Normalization with mean and standard deviation of 0.5

### Dataset Path
- Training data: `r"C:\Users\ANNA MANI\Desktop\labels_sakshi\lego_ALL_results\LEGO_data"`
- Test data: `r"C:\Users\ANNA MANI\LEGOshape\New folder\Black&White_LEGO\train"`

## Model Architecture
The architecture follows the standard DCGAN framework:
- **Generator**: Takes a random noise vector as input and generates an image.
- **Discriminator**: Classifies images as real or fake.

The generator and discriminator weights are initialized using a normal distribution for convolutional layers and batch normalization layers.

### Generator
- Linear layer followed by convolutional blocks with upsampling.
- Final layer outputs an image using the `Tanh` activation.

### Discriminator
- Convolutional layers with Leaky ReLU activations and dropout.
- Final layer outputs the probability of the image being real using a `Sigmoid` activation.

## Requirements
- Python 3.x
- PyTorch
- torchvision
- numpy
- tqdm
- PIL
- pytorch_fid

You can install the required libraries using the following command:
```bash
pip install -r requirements.txt
