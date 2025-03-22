#!/bin/bash
set -e

create_standard() {
    mkdir -p src include build
    touch src/main.cpp include/main.h
    echo "Standard-Projektstruktur erstellt."
}

create_cmake() {
    create_standard
    cat <<EOF > CMakeLists.txt
cmake_minimum_required(VERSION 3.10)
project(MyProject)

set(CMAKE_CXX_STANDARD 17)

add_executable(my_project src/main.cpp)
EOF
    echo "CMake-Projektstruktur erstellt."
}

create_meson() {
    create_standard
    mkdir -p build
    cat <<EOF > meson.build
project('MyProject', 'cpp')

executable('my_project', 'src/main.cpp')
EOF
    echo "Meson-Projektstruktur erstellt."
}

create_bazel() {
    create_standard
    cat <<EOF > BUILD
cc_binary(
    name = "my_project",
    srcs = ["src/main.cpp"],
    hdrs = ["include/main.h"]
)
EOF
    touch WORKSPACE
    echo "Bazel-Projektstruktur erstellt."
}

create_scons() {
    create_standard
    cat <<EOF > SConstruct
env = Environment()
env.Program(target='my_project', source=['src/main.cpp'])
EOF
    echo "SCons-Projektstruktur erstellt."
}

case "$1" in
    "standard") create_standard ;;
    "cmake") create_cmake ;;
    "meson") create_meson ;;
    "bazel") create_bazel ;;
    "scons") create_scons ;;
    *) echo "Ungültige Option. Verfügbar: standard, cmake, meson, bazel, scons" ;;
esac
