# MeowAI

使用Yolov5检测猫并在Synology Photos上对图片添加标签，也支持识别其他67种场景

## 原理

通过Synology API获取图片缩略图，使用离线yolov5模型识别并对图片添加标签



## 使用方法

### Synology DSM

1. 下载镜像, 一般选latest(x86-64)
    ![picture 1](images/1679625127031.png)  
    
2. 启动容器
    ![picture 2](images/1679625615970.png)  

    ![picture 3](images/1679625687135.png)  


### Docker

1. 拉取镜像
    ```
    //arm64 [600MB]
    docker pull charliecaptain/meowai-image:latest-arm-linux

    //x86-64 [2G]
    docker pull charliecaptain/meowai-image:latest
    ```

2. 运行Docker容器

   ```shell
    docker run -it --name meowai -e user="xxx" -e pwd="xxx" --network host meowai_image
    ```

    | 参数         | 说明                                              | 例子                | 必选                          |
    | ------------ | ------------------------------------------------- | ------------------- | ----------------------------- |
    | user         | 登录用户名                                        | -                   | true                          |
    | pwd          | 登录密码                                          | -                   | true                          |
    | ip           | Nas的地址:端口                                    | 0.0.0.0:5000        | false(default 127.0.0.1:5000) |
    | mode         | 个人文件夹还是共享文件夹                          | "person" or"share"  | false(default person)         |
    | detect_class | 识别的场景(67种), 具体看src/detect/detect_dict.py | ['cat','dog','all'] | false(default ['cat'])        |
    


## 开发

目前使用的是Yolov5s.pt数据模型，可以更换更大的数据模型，更多详情请看[Yolov5-Github](https://github.com/ultralytics/yolov5).

### 构建Docker镜像
1. 安装Docker
2. 克隆项目
3. 构建Docker镜像
    ```shell
    chmod 777 ./build.sh
    ./build.sh
    ```


## Thanks

https://github.com/zeichensatz/SynologyPhotosAPI