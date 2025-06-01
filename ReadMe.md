# System Performance Monitor (Dockerized)

## Overview
Hay ,
This project provides a Python script to monitor system CPU and memory usage over time. The script logs this data to a CSV file. The entire application is containerized using Docker, making it easy to run on any PC with Docker installed, regardless of the underlying operating system.

## **Key Technologies:**
* **Python:** For the monitoring script.
* **`psutil` library:** To fetch system performance metrics.
* **Docker:** For containerizing the application, ensuring portability and consistent execution.

## How it Works

The project consists of three main files:

1.  **`performance_monitor.py`**:
    * This Python script uses the `psutil` library to gather current CPU usage percentage and virtual memory usage percentage.
    * It logs these metrics along with a timestamp to a CSV file (`system_performance.csv` by default, or as configured).
    * The logging interval and output file/directory can be configured using environment variables.

2.  **`Dockerfile`**:
    * This file contains instructions for Docker to build an image of the application.
    * It starts from a Python base image (`python:3.9-slim`).
    * Sets up a working directory (`/app`) within the container.
    * Copies `requirements.txt` and installs the `psutil` dependency.
    * Copies the `performance_monitor.py` script into the image.
    * Sets default environment variables for the script's configuration.
    * Specifies the command to run the Python script when a container starts from this image.

3.  **`requirements.txt`**:
    * A simple text file listing the Python dependencies required by the script. In this case, it only contains:
        ```txt
        psutil
        ```

## Prerequisites

To run this project on any other PC, you **must** have Docker installed:

* **Windows/macOS:** Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
* **Linux:** Install [Docker Engine](https://docs.docker.com/engine/install/).

Ensure the Docker daemon/service is running after installation.

## Getting Started / Setup

1.  **Obtain the Project Files:**
    * If this project is in a Git repository, clone it:
        ```bash
        git clone <repository_url>
        cd <repository_directory_name>
        ```
    * Alternatively, download or copy the following files into a single directory on your PC:
        * `performance_monitor.py`
        * `Dockerfile`
        * `requirements.txt`

2.  **Navigate to the Project Directory:**
    Open a terminal or command prompt and change your current directory to where you placed the project files.
    ```bash
    cd path/to/your/project-directory
    ```

## Building the Docker Image

Once you are in the project directory, build the Docker image using the following command:

```bash
docker build -t system-monitor-app .