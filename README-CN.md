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
    docker run -it --name meowai -e user="xxx" -e pwd="xxx" --network host meowai_image
    ```

    | 参数 | 说明                     | 例子               | 必选                          |
    | ---- | ------------------------ | ------------------ | ----------------------------- |
    | user | 登录用户名               | -                  | true                          |
    | pwd  | 登录密码                 | -                  | true                          |
    | ip   | Nas的地址:端口ƒ          | 0.0.0.0:5000       | false(default 127.0.0.1:5000) |
    | mode | 个人文件夹还是共享文件夹 | "person" or"share" | false(default person)         |
   


## Dev

目前使用的是Yolov5s.pt数据模型，可以更换更大的数据模型，更多详情请看[Yolov5-Github](https://github.com/ultralytics/yolov5).


