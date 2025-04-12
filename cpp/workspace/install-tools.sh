#!/bin/bash
set -e

echo "C/C++ tools..."


# Valgrind
sudo apt update && sudo apt install -y valgrind

# Bazel keys (falls nötig, hier Beispiel für optionalen erweiterten Support)
curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor > bazel-archive-keyring.gpg
sudo mv bazel-archive-keyring.gpg /usr/share/keyrings/
echo "deb [signed-by=/usr/share/keyrings/bazel-archive-keyring.gpg] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
sudo apt update && sudo apt install -y bazel

# Conan
sudo apt install -y pip
sudo apt install -y pipx
pipx ensurepath
pipx install conan

echo "Tools installed."
