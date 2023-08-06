#!/bin/bash
set -xe

MINICONDA_DIR="$HOME/miniconda3"

if [ -d "$MINICONDA_DIR" ] && [ -e "$MINICONDA_DIR/bin/conda" ]
then
  echo "Miniconda install already present from cache: $MINICONDA_DIR"
  conda config --set always_yes yes --set changeps1 no
  conda update -q conda
else
  echo "Installing Miniconda"
  wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
  chmod +x miniconda.sh
  ./miniconda.sh -b -f -p "$MINICONDA_DIR"

  conda config --set always_yes yes --set changeps1 no
  conda update -q conda
  if [ "x$TRAVIS_PYTHON_VERSION" = "x3.4" ]; then
      conda install gcc
  else
      conda install gcc_linux-64
  fi
  conda create -n sksurv-test python=$TRAVIS_PYTHON_VERSION numpy=$NUMPY_VERSION pandas=$PANDAS_VERSION mkl=2017.0.* nose coverage cython
  echo "numpy $NUMPY_VERSION.*" > "$MINICONDA_DIR/envs/sksurv-test/conda-meta/pinned"
  echo "pandas $PANDAS_VERSION.*" >> "$MINICONDA_DIR/envs/sksurv-test/conda-meta/pinned"
fi

# The next couple lines fix a crash with multiprocessing on Travis and are not specific to using Miniconda
sudo rm -rf /dev/shm
sudo ln -s /run/shm /dev/shm
