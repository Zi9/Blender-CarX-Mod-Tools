#!/bin/fish
echo "Building Blender addon..."
mkdir zi_cx_tools
cp ./MapTools.py zi_cx_tools
cp ./__init__.py zi_cx_tools
set VER (grep version __init__.py | cut -d '(' -f 2 | cut -d ')' -f 1 | sed 's/, /./g')
zip carx_map_tools_v$VER.zip ./zi_cx_tools/*
echo "Build finished. Cleaning..."
rm -r zi_cx_tools
echo "Done"
