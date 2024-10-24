#!/bin/bash
# A script to alternative gcc version
ls /usr/bin/gcc*
ls /usr/local/bin/gcc*
gcc --version
sudo update-alternatives --list gcc
sudo update-alternatives --list g++

sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-12 1220
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-12 1220


sudo update-alternatives --install /usr/bin/gcc gcc /usr/local/gcc-9.4.0/bin/gcc 940
sudo update-alternatives --install /usr/bin/g++ g++ /usr/local/gcc-9.4.0/bin/g++ 940

sudo update-alternatives --config gcc
sudo update-alternatives --config g++
