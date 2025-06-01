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
        git clone https://github.com/AsithaKanchana1/performanceMonitor.git
        cd performanceMonitor
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
```

- docker build Command to build an image from a Dockerfile.
- -t system-monitor-app Tags the image with the name system-monitor-app. You can choose a different name.
- This command might take a few moments the first time as Docker downloads the base Python image.

## Running the Container
After the image is built successfully, you can run the performance monitor as a Docker container:

### For Linux/macOS (bash/zsh)

```bash
docker run -d --name performance-logger \
  -v "$(pwd)/my_host_logs:/app/performance_logs" \
  system-monitor-app
```

### For Windows (PowerShell):

```powershell
docker run -d --name performance-logger `
  -v "${PWD}/my_host_logs:/app/performance_logs" `
  system-monitor-app
```

## Explanation of docker run options

- `-d` Runs the container in detached mode (in the background). If you want to see the live console output of the script, omit this flag.
- `--name` `performance-logger` Assigns a memorable name to your running container. This makes it easier to manage (e.g., stop or view logs).
- `-v "$(pwd)/my_host_logs/app/performance_logs"` (Linux/macOS) or `-v "${PWD}/my_host_logs/app/performance_logs"` (Windows PowerShell) This is a volume mount.
- It maps a directory on your host PC to a directory inside the container.
- `$(pwd)/my_host_logs` or `${PWD}/my_host_logs` creates a directory named `my_host_logs` in your current working directory on the host. This is where the CSV log files will be accessible from your host machine.
- `/app/performance_logs` is the path inside the container where the Python script (as configured by the *LOG_DIRECTORY* environment variable) will write the log files.
- This is crucial for persisting your log data even if the container is *stopped* or *removed*, and for easily accessing the logs.
- `system-monitor-app` The name of the Docker image you built in the previous step.


### Container's Standard Output (stdout)
The Python script prints a summary of each log entry to the console. You can view these logs (even if running in detached mode) using

```bash
docker logs performance-logger
To follow the logs in real-time:
```

```bash
docker logs -f performance-logger

```

### CSV Log File on Your Host Machine

The actual CSV log data (e.g., system_performance.csv) will be saved in the host directory you specified in the volume mount (e.g., my_host_logs in your project directory). *You can open this CSV file with any spreadsheet program or text editor.*

## Stopping and Removing the Container
### Stop the Container:

To stop the *performance-logger* container from running
```bash
docker stop performance-logger
```

### Remove the Container:
Once stopped, you can remove the container if you no longer need it. This *does not remove the image or your log files* (if you used a volume mount).
```Bash
docker rm performance-logger
```

## Customization

in this document i haven't tuch how to custermize the script ill be updating it in futerue

*Updated Date :2025-6-1*
*@Asitha Kanchana Palliyaguru*
