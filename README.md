# MeowAI

Detect cat and tag image on synology photos by yolov5

[中文文档](./README-CN.md)

## Usage

### Synology DSM

1. download docker image
    ![picture 1](images/1679625127031.png)  
    
2. run docker
    ![picture 2](images/1679625615970.png)  

    ![picture 3](images/1679625687135.png)  



### Docker shell

1. pull docker image
    ```
    //arm64 [600MB]
    docker pull charliecaptain/meowai-image:latest-arm-linux

    //x86-64 [2G]
    docker pull charliecaptain/meowai-image:latest
    ```

2. run docker container

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

### Build Docker 

1. install docker
2. git clone project
3. build docker image
    ```
    chmod 777 ./build.sh
    ./build.sh
    ```
4. run docker

