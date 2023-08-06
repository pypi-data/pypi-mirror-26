#!/usr/bin/env bash

context_dir="./context"
dockerfile="conda_pyenv.docker"
tag="conda_pyenv:pinned_v0.1"

echo "#### Build basic pyenv docker image"
sudo docker rmi ${tag}
sudo docker build -f ${context_dir}/${dockerfile} -m 20G -t ${tag} ${context_dir}
