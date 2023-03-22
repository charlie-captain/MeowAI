# MeowAI

Detect cat and tag image on synology photos by yolov5

[中文文档](./README-CN.md)

## Usage

### Synology DSM

1. open docker
2. 

### Docker shell

1. install docker
2. clone project
3. build docker image

    ```
    chmod 777 ./build.sh
    ./build.sh
    ```

4. run docker container

    ```shell
    docker run -it --name meowai --env cookie="xxx" --env token="xxx" --network host meowai_image
    ```

   cookie-> Cookie: __SSID...

   token-> X-SYNO-TOKEN: xxxxx

## Dev

Currently using the yolov5s.pt dataset, which can be changed to a larger dataset, more can be viewed on the
website [Yolov5-Github](https://github.com/ultralytics/yolov5).


