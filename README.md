# Readme

This project is the final pipeline of car license plate detection and recognition of car license plate text.
Image or video can be detected.  

## Input Arguments 


Before installation of the project, it is impotant to understand the inputs given to run the program. The program accepts three arguments via argparser. 

1. mode :  can be 1 or 2 of integer type. 1 denotes "IMAGE" type and 2 denotes "VIEO" type

2. input_dir : path to image/images/video

3. output_dir : output path to store results

---
**NOTE**

~~~
If mode is 1, the input path should be the path of a single image or a directory of images.

If mode is 2, the input path should be the directory to a single video.
~~~
---

### Download Source Code
```shell
$ git clone https://github.com/kht-gw/Final_Pipeline.git
$ cd Final_Pipeline
```


## Install With Docker
If the system has docker installed, docker can be utilized to run the project. 

### Run docker with Makefile
```shell
$ make docker-build
$ make docker-run
```

### Run Docker manually
#### Build Docker
```shell
# $ docker build -t {docker_image} -f Docker/Dockerfile .
$ docker build -t car_license_app -f Docker/Dockerfile .

```
#### Run Docker

```shell
# docker run -it --rm -v {project_path}:/car_license_app/ --gpus all --network=host {docker_image} {mode} "{image_path }" "{output_path}"

$ docker run -it --rm -v ./:/car_license_app/ --gpus all --network=host car_license_app  1 "assets/images" "assets/sample_run"
```

### Run Docker for Video Detection
Replace the variables in the following command with the actual values. 

* {project_path} : path to project (Final_Pipeline)

* {docker_image} : *car_license_app* according to the above build command

* {video_path} : path to video 

* {output_path} : path to generate output video result

```shell
 $ docker run -it --rm -v {project_path}:/car_license_app/ --gpus all --network=host {docker_image} 2 "{video_path }" "{output_path}"
```



## Install with Venv
If you don't want to install with docker, you can install on local machine via virtualenv. 

``` shell
$ python3 -m virtualenv venv
$ source venv/bin/activate
$ pip install -U pip
$ pip install -e .
```

### Run App

#### Image Detection
The following command detects and generate ocr text of images. You can replace {mode} {input_image_dir} {output_dir} with respective values.
```shell
# $ python3 src/license_plate/main.py {mode=1} {input_image_dir} {output_dir}
$ python3 src/license_plate/main.py 1 "assets/images" "assets/sample_run"
```

#### Video Detection
Replace the variables inside {} with actual values. Please reference [Input Arguments](#Input-Arguments)

```shell
$ python3 src/license_plate/main.py {mode} {video_dir} {output_dir}
```




## Output of Image Mode

After doing detection and ocr, the following outputs will be genereted in sample_run foder automatically. 'crops' directory contains cropped car license plate images. 'bbox_images' contains the images with detected car license plates and ocr text. 
'results.json' is the json file containing all the information of the process. 

* assets
    + sample_run
        + crops
        + bbox_imgaes
        + results.json 


## Outputs of Video Mode


* assets
    + sample_run
        + video_name.mp4


