# CMAKE
cmake -S /workspace/project -B /workspace/build
cmake --build /workspace/build
/workspace/build/my_project

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
