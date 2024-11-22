# Hybrid Image Playground

![Typing SVG](https://readme-typing-svg.demolab.com?font=Jetbrains+Mono&pause=1000&width=435&lines=Play+with+hybrid+images;Create+your+own+one;Tweak+the+parameters;Understand+the+concept)

![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/ptrlx/hybrid-image-playground)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub Pipenv locked Python version dash](https://img.shields.io/github/pipenv/locked/python-version/ptrlx/hybrid-image-playground/dash)
![Github Action Status](https://img.shields.io/github/actions/workflow/status/ptrlx/hybrid-image-playground/build.yml)
[![Docker Image Size](https://img.shields.io/docker/image-size/ptrlx/hybrid-image-playground?label=Image%20Size&logo=docker)](https://hub.docker.com/r/ptrlx/hybrid-image-playground)
[![Docker Pulls](https://img.shields.io/docker/pulls/ptrlx/hybrid-image-playground?label=Pulls&logo=docker)](https://hub.docker.com/r/ptrlx/hybrid-image-playground)

![](assets/2024-11-22-00-40-54.png)

## Setup

###### Requirements

* Python 3.12
* Pipenv

###### Install and run the project

```bash
pipenv install
pipenv run python src/main.py
```

* Open your browser and go to <http://localhost:8300>

###### Run the docker image

```bash
docker pull ptrlx/hybrid-image-playground
docker run -it --rm -p 8080:80 ptrlx/hybrid-image-playground
```

* Open your browser and go to <http://localhost:8080>

## Preprocessing - resizing and alignment

* The two images should be aligned e. g. using [GIMP](https://www.gimp.org/) (add both images as layers; reduce the opacity of the top layer; move the top layer to align with the bottom layer)
* Resize both images to the same size (and a quadratic shape)

## Resources

* <http://olivalab.mit.edu/publications/OlivaTorralb_Hybrid_Siggraph06.pdf>
* <https://github.com/rhthomas/hybrid-images>
* <https://www.geeksforgeeks.org/creating-hybrid-images-using-opencv-library-python/>
* <https://www.jeremykun.com/2014/09/29/hybrid-images/>
