.DEFAULT_GOAL := build_addon
VER := $(shell grep -E '^version = ' ./src/blender_manifest.toml | cut -d '"' -f 2)

build_addon:
	@echo "Building blender addon..."
	mkdir zi_cx_tools
	cp ./src/MapTools.py zi_cx_tools
	cp ./src/__init__.py zi_cx_tools
	cp ./src/blender_manifest.toml zi_cx_tools
	zip carx_map_tools_v$(VER).zip ./zi_cx_tools/*
	echo "Build finished. Cleaning..."
	rm -r zi_cx_tools
	echo "Done"

clean:
	rm carx_map_tools_v*.zip
