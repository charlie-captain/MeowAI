# MeowAI

使用Yolov5检测猫并在Synology Photos上对图片添加标签

## 使用方法

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
   docker run -it --name meow --network host -e cookie=xxx -e token=xxx meowai_image
   ```
   cookie-> Cookie: __SSID...

   token-> X-SYNO-TOKEN: xxxxx