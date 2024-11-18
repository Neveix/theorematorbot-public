#!/bin/bash
if [ ! -d "build" ]; then
  mkdir build
fi

if [ ! -d "pdf" ]; then
  mkdir pdf
fi

cd build

cmake ..

cmake --build .