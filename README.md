# Overview

This project is the final pipeline of car license plate detection and recognition of car license plate text.
Image or video can be detected.  

![image](/assets/pipeline_architecture.png?raw=true)

## Models 
* Object Detection Model (YoloV8)
* OCR Model (Paddle OCR)


## Object Detection Model Evaluation Metrics on Validation Dataset

Inference Time | Precision | Recall | mAP@50 | mAP
--------------|-----------|--------|--------|------
2.8 ms | 0.87 | 0.867 | 0.917| 0.525

**FPS (based on above inference time) = 357**

## Input Arguments 


Before installation of the project, it is impotant to understand the inputs given to run the program. The program accepts three arguments via argparser. 

1. mode :  can be 1 or 2 of integer type. 1 denotes "IMAGE" type and 2 denotes "VIDEO" type

2. input_dir : path to image/images/video

3. output_dir : output path to store results

---
**NOTE**

~~~
If mode is 1, the input path should be the path of a single image or a directory of images.

If mode is 2, the input path should be the directory to a single video.
~~~
---

## System Requirements 

To install the project, you need Pyhton version 3.8 and above. In Linux, please install libGL to run paddleocr. 

```shell
$ sudo apt-get update && sudo apt-get install libgl1-mesa-glx

```

### Host System Specifications
The Host OS specifications are as follow:

* Ubuntu Linux: 22.04
* Cuda Version : 11.7
* Python Version : 3.10.12
* Docker Version : 25.0.3

### Required Libraries
* ultralytics
* opencv-python
* paddleocr
* paddlepaddle

Please reference requirements.txt file.


## Download Source Code
```shell
$ git clone https://github.com/kht-gw/Car_License_Plate_Detection.git
$ cd Car_License_Plate_Detection
```

# Inatallation

The installation setup can be of three types. You can follow one of the three methods to install. 

## 1. Install With Docker by Makefile


###  Build docker with Makefile
```shell
$ make docker-build
```
### Run docker with Makefile
This processes sample images from the  project. The images path is /assets/images. 

```shell
$ make docker-run-image
```

## 2. Install with Docker manually

If you want to handle more on docker commands, please follow this steps. 

### Build Docker
```shell
# $ docker build -t {docker_image} -f Docker/Dockerfile .
$ docker build -t car_license_app -f Docker/Dockerfile .
```


### Run Docker for Image Mode
```shell
# docker run -it --rm -v {project_path}:/car_license_app/ --gpus all --network=host {docker_image} {mode} "{image_path }" "{output_path}"

$ docker run -it --rm -v ./:/car_license_app/ --gpus all --network=host car_license_app  1 "assets/images" "assets/sample_run"
```

#### Run Docker for Video Mode
Replace the variables in the following command with the actual values. 

* {project_path} : path to project (Final_Pipeline)

* {docker_image} : *car_license_app* according to the above build command

* {video_path} : path to video 

* {output_path} : path to generate output video result

```shell
 $ docker run -it --rm -v {project_path}:/car_license_app/ --gpus all --network=host {docker_image} 2 "{video_path }" "{output_path}"
```



## 3. Install with Venv
If you don't want to install with docker, you can install on local machine via virtualenv. 

``` shell
$ python3 -m virtualenv venv
$ source venv/bin/activate
$ pip install -U pip
$ pip install -e .
```


### Run for Image Detection
The following command detects and generate ocr text of images. You can replace {mode} {input_image_dir} {output_dir} with respective values.
```shell
# $ python3 src/license_plate/main.py {mode=1} {input_image_dir} {output_dir}
$ python3 src/license_plate/main.py 1 "assets/images" "assets/sample_run"
```

### Run for Video Detection
Replace the variables inside {} with actual values. Please reference [Input Arguments](#Input-Arguments) for more.

```shell
$ python3 src/license_plate/main.py {mode} {video_dir} {output_dir}
```
## Model Weight file

The system will automatically download the model weight file once it started to run. 

However, you can download the weight file manually. 
The custom trained Yolov8 object detection model can be downloaded below. 


[Download license_plate_detector](https://drive.google.com/drive/u/0/folders/1GgT0VkIk08aEbFebe7ugkfxVfv4UFUBs)

Then go to the root of project directory and create 'weights' folder. You can put 'license_plate_detector.pt' weight file inside 'weights' directory so that the program skips to download the weight file again. 


*Car_License_Plate_Detection/weights /license_plate_detector.pt*

## Outputs of Image Mode

After doing detection and ocr, the following outputs will be genereted in sample_run folder automatically. 'crops' directory contains cropped car license plate images. 'bbox_images' contains the images with detected car license plates and ocr text. 
'results.json' is the json file containing all the information of the process. 

* assets
    + sample_run
        + crops
        + bbox_imgaes
        + results.json 

### Sample Results

#### bounding box image with text

![car image](/assets/sample_run/bbox_images/Cars297.png)


#### cropped license plate image

![carimage](/assets/sample_run/crops/Cars297_1.jpg?raw=true)



#### results.json

Json file output for detection results of above sample car image is as follows: 


```json

[
 
  {
    "file_name": "Cars297.png",
    "results": [
      {
        "bbox_coordinate": [
          157.355,
          148.991,
          245.429,
          170.645
        ],
        "detection_score": 0.794,
        "ocr_text": "IM4U555",
        "ocr_score": 0.992
      }
    ]
  }
  
]

```

## Outputs of Video Mode


* assets
    + sample_run
        + video_name.mp4

## Frame Per Second

The following describes fps of the pipeline based on sample images in assets folder.

* Average FPS of Object Detection Model: **31**
* Average FPS of OCR model: **15**
* Average FPS of Pipeline: **12**