# HydroLearn - AI-Powered Hydroponics Monitoring and Alert System

**HydroLearn** is an AI-powered, real-time monitoring and alert system designed to optimize and improve the sustainability of hydroponic farming. It gathers real-time sensor data (temperature, humidity, pH) from a hydroponic setup, uses machine learning to predict future conditions, and sends alerts when critical thresholds are exceeded. The project leverages data analytics, machine learning, and Firebase integration to create a system that helps improve plant growth efficiency while reducing resource consumption.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [How It Works](#how-it-works)
- [Machine Learning Model](#machine-learning-model)
- [Alert System](#alert-system)
- [Real-Time Visualization](#real-time-visualization)
- [Future Enhancements](#future-enhancements)
- [Contributors](#contributors)

## Introduction
**HydroLearn** aims to provide a smart solution for hydroponic farming by enabling:
- **Real-time sensor monitoring** to ensure optimal growing conditions.
- **Data-driven learning and predictions** using machine learning to forecast environmental trends.
- **Automated alerts** via email or mobile notification systems to notify users of conditions that could harm plants.

By continuously monitoring temperature, humidity, and pH levels, the system helps growers fine-tune their hydroponic system, ultimately leading to **better crop yields** and **efficient resource management**.

## Features
- **Real-Time Monitoring**: Continuously collects data from sensors monitoring temperature, humidity, and pH levels.
- **Machine Learning Predictions**: Uses historical sensor data to predict future conditions and prevent harmful changes.
- **Alert System**: Sends email alerts using SendGrid if environmental conditions exceed safe limits.
- **Data Visualization**: Displays real-time sensor data and predictions on a dynamic graph with thresholds.
- **Firebase Integration**: Stores and retrieves sensor data and predictions from a Firebase Realtime Database.

## Architecture
HydroLearn is composed of three main components:
1. **Data Collection**: Sensor data is collected and pushed to Firebase in real-time.
2. **Machine Learning Predictions**: A machine learning model is trained to predict future conditions based on past sensor data.
3. **Alerts & Visualization**: Real-time alerts are sent, and sensor data is visualized through a Python-based graph with custom thresholds for temperature, humidity, and pH.

### Key Technologies:
- **Python** for data processing, machine learning, and Firebase interaction.
- **Firebase** Realtime Database for storing and retrieving sensor and prediction data.
- **Matplotlib** for real-time data visualization.
- **SendGrid** for email notifications.
- **scikit-learn** for machine learning predictions.

## Prerequisites
- **Python 3.7+**
- **Firebase Project** (set up a Realtime Database)
- **SendGrid API Key** (for email notifications)
- Basic understanding of **hydroponics** and environmental variables (temperature, humidity, pH).

### Python Libraries:
- `firebase-admin`
- `sendgrid`
- `matplotlib`
- `scikit-learn`
- `requests`

Install all dependencies using:
```bash
pip install firebase-admin sendgrid matplotlib scikit-learn requests
```