# 使用 Python 3.11 的精简版镜像
FROM python:3.11-slim

# 可选：添加项目和维护者标签
LABEL maintainer="your-email@example.com"
LABEL project="TTS-VC-PTTS-Animate-Testing"

# 设置工作目录为 /app
WORKDIR /app

# 复制依赖文件并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 将整个项目代码复制到容器中（包含 TTS 文件夹）
COPY . .

# 默认启动 bash，以便 PyCharm 通过 Docker 远程解释器运行指定脚本
CMD [ "bash" ]
