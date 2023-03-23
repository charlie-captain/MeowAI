# 使用官方 Python 镜像作为基础镜像
FROM python:3.8-buster

# 将当前目录下的文件都复制到 Docker 镜像的 /app 目录下
COPY . /app

# 切换到 /app 目录
WORKDIR /app

# 安装所需依赖
RUN apt-get update --fix-missing \
    && apt-get install ffmpeg libsm6 libxext6 -y \
    && pip install --upgrade pip \
    && pip install torch==1.13.0 torchvision==0.14.0 \
    && pip install -r requirements.txt \
    && pip install -r yolov5/requirements.txt \
#    && apt-get install -y libgl1-mesa-glx \
    # 删除缓存文件
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf ~/.cache/pip

# 设置环境变量
ENV PYTHONPATH "${PYTHONPATH}:/app/"

# 运行 Python 程序
CMD ["python", "main.py"]
