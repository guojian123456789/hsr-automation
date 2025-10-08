# HSR Automation - Android构建环境
FROM ubuntu:22.04

# 设置非交互式安装
ENV DEBIAN_FRONTEND=noninteractive

# 设置时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    # 基础工具
    git \
    zip \
    unzip \
    wget \
    curl \
    # Java环境
    openjdk-17-jdk \
    # Python和pip
    python3 \
    python3-pip \
    python3-dev \
    # 构建工具
    build-essential \
    autoconf \
    libtool \
    pkg-config \
    # 依赖库
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    # 清理缓存
    && rm -rf /var/lib/apt/lists/*

# 设置Java环境变量
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# 升级pip并安装Python构建工具
RUN pip3 install --upgrade pip && \
    pip3 install --upgrade setuptools wheel && \
    pip3 install buildozer cython==0.29.33

# 设置工作目录
WORKDIR /app

# 设置默认命令
CMD ["/bin/bash"]

# 标签信息
LABEL maintainer="HSR Automation Team"
LABEL description="HSR Automation Android Build Environment"
LABEL version="1.0"




