# MeowAI
![GitHub release (release name instead of tag name)](https://img.shields.io/github/v/release/charlie-captain/MeowAI?include_prereleases)
![GitHub last commit](https://img.shields.io/github/last-commit/charlie-captain/MeowAI)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/charlie-captain/MeowAI)
![Docker Stars](https://img.shields.io/docker/stars/charliecaptain/meowai-image)
![GitHub Repo stars](https://img.shields.io/github/stars/charlie-captain/MeowAI)
![GitHub](https://img.shields.io/github/license/charlie-captain/MeowAI)


Use Yolov5 to perform offline detection on images and add tags to the images in Synology Photos, supporting the
recognition of 80 scenes.

#### [中文文档](./README-CN.md)

## How

Extract thumbnail images using Synology API and add labels to images using offline yolov5 model.

## Usage

### Shell  (Recommend)

1. git clone repository
2. install requirements.txt
    ```
   pip3 install -r requirements.txt
   pip3 install -r yolov5/requirements.txt
   pip3 install torch torchvision
   ```
3. run py
   ```
    user="xxx" \
    pwd="xxx" \
    mode="xxx" \
    exclude_class="[\"cat\"]" \
    ip="192.168.5.1:5000" \
    python3 main.py
    ```

### Docker shell

Docker will run longer than the shell command above because it will forever monitor for new photos.

1. pull docker image
    ```
    //arm64 [600MB]
    docker pull charliecaptain/meowai-image:latest-arm-linux

    //x86-64 [2G]
    docker pull charliecaptain/meowai-image:latest
    ```

2. run docker container

    ```shell
    docker run -it 
            --name meowai \
            -e user="xxx" \
            -e pwd="xxx" \
            -e mode="person" \
            -e exclude_class="[\"cat\",\"dog\"]" \
            -e model='yolov5m6' \
            --network host \
            meowai_image
    ```

### Synology DSM

This will consume your CPU resources.

1. download docker image
   ![picture 1](images/1679625127031.png)

2. run docker
   ![picture 2](images/1679625615970.png)

   ![picture 3](images/1679625687135.png)

### Arguments

| Argument      | Description                                          | Demo               | Require                       |
| ------------- | ---------------------------------------------------- | ------------------ | ----------------------------- |
| user          | login user                                           | -                  | true                          |
| pwd           | login password                                       | -                  | true                          |
| ip            | nas ip                                               | 0.0.0.0:5000       | false(default 127.0.0.1:5000) |
| mode          | person dir or share dir                              | "person" or"share" | false(default person)         |
| exclude_class | exclude detect scenes, see src/detect/detect_dict.py | ['cat','dog']      | false(default [])             |
| model         | yolov5 model pt file name                            | yolov5m6           | false(default yolov5m6)       |
| lang          | tag language                                         | zh/en              | false(default en)             |

### Model

Pretrained models for YOLOv5 can be selected and will be automatically downloaded to the environment.

Running the Python file directly allows for the use of larger models with the participation of the GPU, resulting in significantly faster processing speeds compared to running within a Docker container. 

Docker is best suited for running yolov5s6, which has an average recognition speed of about 2 seconds.

## Dev

Currently using the yolov5m6.pt dataset, which can be changed to a larger dataset, more can be viewed on the
website [Yolov5-Github](https://github.com/ultralytics/yolov5).

### Build Docker

1. install docker
2. git clone project
3. build docker image
    ```
    chmod 777 ./build.sh
    ./build.sh
    ```
4. run docker

## Q&A

### How to remove all tags

```shell
user="xxx" pwd="xxx" mode="xxx" exclude_class="[\"dog\"]" python3 src/util/util.py
```

## Thanks

https://github.com/zeichensatz/SynologyPhotosAPI

## Donate

TRC20(USDT): TKRJkxUWYnnjLXVjN5Nutk6cvZ3Nz3S9pv

[爱发电支持我](https://afdian.net/a/richardmike)

[![Ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/charliecaptain)


## License

```
MIT License

Copyright (c) 2023 Charlie

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```