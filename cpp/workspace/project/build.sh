# CMAKE
cmake -S . -B build
cmake --build build
./build/my_project

# MESON
#meson setup build
#meson compile -C build
#./build/my_project

# BAZEL
#bazel build //:my_project
#./bazel-bin/my_project

#SCons
#scons
#./my_project
