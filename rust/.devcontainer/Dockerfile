FROM rust:latest

# Create a non-root user (recommended)
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN apt-get update \
    && apt-get install -y curl pkg-config libssl-dev build-essential \
    && rustup component add rustfmt clippy \
    && groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get clean

USER $USERNAME
WORKDIR /home/$USERNAME/app
