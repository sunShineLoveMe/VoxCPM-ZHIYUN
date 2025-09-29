# Python + CUDA 12.1 + cuDNN8（Runpod 兼容）
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONUNBUFFERED=1 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    GRADIO_SERVER_PORT=7860

# 工作目录
WORKDIR /app

# 系统依赖（含 ffmpeg 和 libsndfile，音频必备）
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-dev git ffmpeg libsndfile1 ca-certificates curl && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install -U pip setuptools wheel

# 先复制 requirements 以利用缓存层
COPY requirements.txt /tmp/requirements.txt

# 安装与 CUDA 12.1 匹配的 PyTorch/torchaudio/torchvision（GPU 版）
RUN pip3 install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cu121 \
    torch==2.3.1+cu121 \
    torchaudio==2.3.1+cu121 \
    torchvision==0.18.1+cu121

# 安装其余 Python 依赖
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# 复制项目代码
COPY . /app

# 暴露端口
EXPOSE 7860

# 健康检查（可选）
HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=10 \
  CMD curl -fsS http://localhost:7860/config || exit 1

# 启动
CMD ["python3", "app.py", "--host", "0.0.0.0", "--port", "7860"]
