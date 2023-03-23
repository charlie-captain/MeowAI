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
    docker run -it --name meowai -e user="xxx" -e pwd="xxx" -e mode="person" --network host meowai_image
    ```

    | Argument | Description             | Demo               | Require                       |
    | -------- | ----------------------- | ------------------ | ----------------------------- |
    | user     | login user              | -                  | true                          |
    | pwd      | login password          | -                  | true                          |
    | ip       | nas ip                  | 0.0.0.0:5000       | false(default 127.0.0.1:5000) |
    | mode     | person dir or share dir | "person" or"share" | false(default person)         |
   

## Dev

Currently using the yolov5s.pt dataset, which can be changed to a larger dataset, more can be viewed on the
website [Yolov5-Github](https://github.com/ultralytics/yolov5).


