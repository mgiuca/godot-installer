# Godot Installer

This is a simple Python script that fetches a specific version of Godot and
installs it, setting up symlinks.

Currently only works on Linux.

Basic usage:

    ./godot_installer.py -s godot -s godot4.5 4.5-beta4

(By default, installs in root and asks for sudo permission.)

Symlinks are optional and can be multiple; I like to set `godotx.y` for the
latest build of every minor release, and `godot` for the latest stable.

For full help:

    ./godot_installer.py --help
