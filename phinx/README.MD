To run the Docker container build type: 

```
docker build -t sphinx-dev .
docker run -it --rm -v "$(pwd)/docs:/docs" sphinx-dev
```

Within the container tyoe: 

```
sphinx-build -b html source build
```

Afterwars type the following on MAC-OS

```
open docs/build/index.html
```
