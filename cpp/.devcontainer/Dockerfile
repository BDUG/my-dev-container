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

RUN curl -fsSL https://build2.org/bootstrap.sh | sh

COPY install-tools.sh /usr/local/bin/install-tools.sh
COPY scripts/create_project_structure.sh /usr/local/bin/create_project_structure.sh
RUN chmod +x /usr/local/bin/install-tools.sh /usr/local/bin/create_project_structure.sh
