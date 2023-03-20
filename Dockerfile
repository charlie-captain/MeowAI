# 使用官方 Python 镜像作为基础镜像
FROM python:3.8-alpine

# 将当前目录下的文件都复制到 Docker 镜像的 /app 目录下
COPY . /app

# 切换到 /app 目录
WORKDIR /app

# 安装所需依赖
RUN pip install -r requirements.txt

# 设置环境变量
ENV PYTHONPATH "${PYTHONPATH}:/app/"

# 运行 Python 程序
CMD ["python", "main.py"]
