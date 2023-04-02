# 使用官方 Python 镜像作为基础镜像
FROM python:3.8-buster

# 将当前目录下的文件都复制到 Docker 镜像的 /app 目录下
COPY . /app

# 切换到 /app 目录
WORKDIR /app

# 安装所需依赖
RUN pip install --upgrade pip \
    && pip install -r requirements.txt  \
    && pip install torch==1.13.0 torchvision==0.14.0 --index-url https://download.pytorch.org/whl/cpu  \
    && rm -rf ~/.cache/pip/* \
    && apt-get update --fix-missing  \
    && apt-get install -y --no-install-recommends libgl1-mesa-glx \
    && pip install -r yolov5/requirements.txt  \
    && rm -rf ~/.cache/pip/* \
    && rm -rf /var/lib/apt/lists/*

# 设置环境变量
ENV PYTHONPATH "${PYTHONPATH}:/app/"

# 运行 Python 程序
CMD ["python", "main.py"]
