# Generative Adversarial Networks (GANs) Collection

This repository contains implementations of various GAN models applied to diverse datasets, including RGB, thermal, and infrared images. Each GAN is designed to handle different data types, providing flexibility for synthetic image generation tasks across multiple domains.

## Table of Contents
- [Overview](#overview)
- [Datasets](#datasets)
- [GAN Models](#gan-models)
- [Requirements](#requirements)
- [Training](#training)
- [Testing](#testing)
- [Results](#results)
- [References](#references)

## Overview
This project showcases a collection of GAN architectures trained on different datasets for synthetic image generation. Each file corresponds to a unique GAN model tailored to a specific type of data, such as RGB, thermal, or infrared images. The repository includes:
- Multiple GAN implementations (DCGAN, WGAN, CycleGAN, WGAN-Divergence, WGAN with Gradient Penalty, MixNMatch, SRGAN etc)
- Training scripts for different GANs
- Model checkpoints for each GAN

## Datasets
The GANs are implemented on various datasets with specific preprocessing steps suited to the data type:
- **RGB**: High-resolution color images with detailed textures.
- **Thermal**: Images representing heat signatures.
- **Infrared**: Lower spatial resolution, often used for night vision or non-visible spectrum tasks.
- **Results**: Here I have attached the drive link for the results of the datasets and GANs that I have used so far- https://docs.google.com/presentation/d/1PJ5nNBFok_bX-F9UvrEm7PTF3w4j3POz/edit?usp=sharing&ouid=111933379389103591948&rtpof=true&sd=true

### Dataset 
Each dataset used in this project is publicly available and can be downloaded from sources like Kaggle, depending on your needs. Be sure to adjust the dataset paths in the scripts to match your own directory structure for training your model.

## GAN Models
The repository includes a variety of GAN architectures:
- **DCGAN**: Standard model for synthetic image generation using convolutional layers.
- **WGAN**: Wasserstein GAN for more stable training.
- **CycleGAN**: Designed for image-to-image translation tasks.
- **Conditional GANs**: For generating images based on specific conditions or labels.
- **MixNMatch GAN**: A generative model designed to create diverse and realistic images by combining different features from multiple input images by disentangling features such as background, shape, texture and pose, enabling flexible and customizable image synthesis.

Each GAN architecture has been customized to the dataset it works on, and the generator/discriminator models are tailored to capture the characteristics of the input data.

### Key Model Features
- **Generator**: Creates synthetic images from random noise or conditional inputs.
- **Discriminator**: Evaluates the authenticity of generated images against real ones.
- **Loss Functions**: Tailored loss functions for stable training (e.g., Wasserstein loss, adversarial loss).

## Requirements
The project relies on common Python libraries and frameworks such as PyTorch. You can install the necessary versions of CUDA, CUDNN and Pytorch according to your requirements.


