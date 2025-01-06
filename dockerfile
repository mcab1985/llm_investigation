FROM nvidia/cuda:12.1.1-devel-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Update the package list, install sudo.
RUN apt update && \
    apt install -y sudo software-properties-common

RUN add-apt-repository ppa:deadsnakes/ppa -y

# Install base packages.
RUN apt install -y ffmpeg libgl1 libsm6 libxext6 python3.11 python3.11-dev python3.11-venv python3.11-distutils git vim bc curl

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# Set working directory 
WORKDIR /classifier_app

# Create virtual environment in the container.
RUN python3.11 -m venv .venv

# Acvivate the virtual environment.
ENV Path="/classifier_app/.venv/bin:$PATH"

# Copy dependencies 
COPY requirements.txt . 
COPY classifier_app.py .
COPY finetune.py . 
COPY dataset_handler.py .
COPY text_classifier.py .

# Install python dependencies
RUN python3.11 -m pip install -r requirements.txt

# Copy application
COPY . . 

#  Use Port 6001
EXPOSE 6001

CMD ["python3.11", "classifier_app.py"]
