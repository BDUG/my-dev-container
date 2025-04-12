FROM mcr.microsoft.com/devcontainers/cpp:debian

RUN apt-get update && apt-get install -y \
    ninja-build \
    meson \
    bazel \
    scons \
    clangd \
    valgrind \
    python3-pip \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*
