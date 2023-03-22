# MeowAI

Detect cat and tag image on synology photos by yolov5

## Usage

### Docker

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