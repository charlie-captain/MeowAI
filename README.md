# MeowAI

Detect cat and tag image on synology photos by yolov5

[中文文档](./README-CN.md)

## Usage

### Synology DSM

Making image smaller now, will be updated.

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
    docker run -it --name meowai -e cookie="xxx" -e token="xxx" -e mode="person" --network host meowai_image
    ```

    | Argument | Description              | Demo               | Require        |
    | -------- | ------------------------ | ------------------ | -------------- |
    | cookie   | Dsm request headerCookie | __SSID...          | true           |
    | token    | X-SYNO-TOKEN:            | Nxxxx.xxxxxÏ       | true           |
    | mode     | person dir or share dir  | "person" or"share" | default person |
   

## Dev

Currently using the yolov5s.pt dataset, which can be changed to a larger dataset, more can be viewed on the
website [Yolov5-Github](https://github.com/ultralytics/yolov5).


