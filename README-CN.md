# MeowAI

使用Yolov5离线检测图片并在Synology Photos上对图片添加标签，支持识别80种场景

## 原理

通过Synology API获取图片缩略图，使用离线yolov5模型识别并对图片添加标签

## 使用方法


### Docker (推荐)

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

### Synology DSM

运行在Synology上会占用大量CPU，请谨慎使用

1. 下载镜像, 一般选latest(x86-64)
   ![picture 1](images/1679625127031.png)

2. 启动容器
   ![picture 2](images/1679625615970.png)

   ![picture 3](images/1679625687135.png)

### Shell

1. git clone repository
2. install requirements.txt
    ```
   pip3 install requirements.txt
   pip3 install yolov5/requirements.txt
   pip3 install torch==1.13.0 torchvision==0.14.0
   ```
3. run py
   ```
    user="xxx" pwd="xxx" mode="xxx" detect_class="[\"cat\",\"all\"]" python3 main.py
    ```

### 参数说明

| 参数         | 说明                                              | 例子                | 必选                          |
| ------------ | ------------------------------------------------- | ------------------- | ----------------------------- |
| user         | 登录用户名                                        | -                   | true                          |
| pwd          | 登录密码                                          | -                   | true                          |
| ip           | Nas的地址:端口                                    | 0.0.0.0:5000        | false(default 127.0.0.1:5000) |
| mode         | 个人文件夹还是共享文件夹                          | "person" or"share"  | false(default person)         |
| detect_class | 识别的场景(67种), 具体看src/detect/detect_dict.py | ['cat','dog','all'] | false(default ['all'])        |
| model        | 模型数据集                                        | yolov5l             | false(default yolov5l)        |

model 准确率: yolov5s<yolov5m<yolov5l

model 速度: yolov5s>yolov5m>yolov5l

test on mac m1: yolov5s(0.2s), yolov5m(0.3s), yolov5l(0.4s)

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

## 捐献

>感谢您的支持

TRC20(USDT): TKRJkxUWYnnjLXVjN5Nutk6cvZ3Nz3S9pv

<img src="images/1679625687777.JPG" width="50%" />

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