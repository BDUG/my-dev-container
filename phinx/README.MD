To run the Docker container build type: 

```
docker build -t sphinx-dev .
docker run -it --rm -v "$(pwd)/docs:/docs" sphinx-dev
```

Within the container tyoe: 

```
sphinx-build -b html source build
exit
```

Afterwars type the following on MAC-OS

```
open docs/build/index.html
```

To use [VSCode Dev Container](https://code.visualstudio.com/docs/devcontainers/containers) install the  
[extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) and press in the upper left coner the icon "><".


