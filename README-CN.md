# MeowAI

使用Yolov5检测猫并在Synology Photos上对图片添加标签

## 使用方法

### Synology DSM

目前还在精简镜像体积，请先使用下面方法

### Docker

1. 安装Docker
2. 克隆项目
3. 构建Docker镜像
    ```shell
    chmod 777 ./build.sh
    ./build.sh
    ```
   运行Docker容器

   ```shell 
   docker run -it --name meowai --network host -e cookie="xxx" -e token="xxx" meowai_image
   ```
   cookie-> Cookie: __SSID...

   token-> X-SYNO-TOKEN: xxxxx

## Dev

目前使用的是Yolov5s.pt数据模型，可以更换更大的数据模型，更多详情请看[Yolov5-Github](https://github.com/ultralytics/yolov5).


