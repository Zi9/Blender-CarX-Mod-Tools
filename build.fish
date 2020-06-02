#!/bin/fish
echo "Building Blender addon..."
mkdir zi_cx_tools
cp ./MapTools.py zi_cx_tools
cp ./__init__.py zi_cx_tools
zip carx_map_tools.zip ./zi_cx_tools/*
echo "Build finished. Cleaning..."
rm -r zi_cx_tools
echo "Done"
