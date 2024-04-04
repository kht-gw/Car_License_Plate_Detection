FROM nvidia/cuda:11.7.1-runtime-ubuntu22.04

RUN apt-get clean

RUN apt-get update --fix-missing

RUN apt-get install -y python3 python3-pip 

RUN apt-get install -y \
    zlib1g-dev \
    libjpeg-dev \
    gcc \
    libtiff5-dev \
    ffmpeg \ 
    libsm6 \
    libxext6

RUN apt-get install libgl1-mesa-glx -y

RUN mkdir /car_license_app

COPY .. /car_license_app/

WORKDIR /car_license_app

# RUN pip install --no-cache-dir -r requirements.txt
# RUN . license-plate/bin/activate

RUN pip install -U pip

RUN pip install -e .



ENTRYPOINT ["python3", "src/license_plate/main.py"]
