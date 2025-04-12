conan profile detect --force
conan install . --output-folder=build --build=missing
cd build
# Enable specific environment:  source conanbuild.sh
cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release
cmake --build .
# Disable specific environment: source deactivate_conanbuild.sh