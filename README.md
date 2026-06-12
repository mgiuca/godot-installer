# Godot Installer

This is a simple Python script that fetches a specific version of Godot and
installs it, setting up symlinks.

Currently only works on Linux and Windows (see caveats below).

Basic usage:

    ./godot_installer.py -s godot -s godot4.6 4.6-stable

(By default, installs in root and asks for sudo permission.)

This will download and create three new files on your system:

- `/usr/local/bin/Godot_v4.6-stable_linux.x86_64`
- `/usr/local/bin/godot4.6` -> `Godot_v4.6-stable_linux.x86_64`
- `/usr/local/bin/godot` -> `Godot_v4.6-stable_linux.x86_64`

Symlinks are optional and can be multiple; I like to set `godotx.y` for the
latest build of every minor release, and `godot` for the latest stable. As it
never deletes old versions, over time you will accumulate all the versions (with
their full name), symlinks to each minor release, and the main `godot` symlink
pointing to the latest stable release. You can manually clean these up
periodically but I like to keep them all for testing purposes.

Useful for:

- Installing pre-release versions and testing them out, without overwriting your
  main `godot` install.
- Maintaining a library of old versions for easily loading old projects without
  upgrading them, or testing regressions across past versions.

For full help:

    ./godot_installer.py --help

## Windows

On Windows, it installs to C:\Program Files\Godot by default (which is probably
not in your path), and has some caveats:

- It needs a Bash-like environment (such as MinGW).
- The "symlinks" will just be copies.
- It automatically adds `.exe` to the end of the symlink path, and also copies
  the `_console.exe` file.
- It assumes your user is an administrator, and does not try to use sudo by
  default. If you use `--user` to install as a different user, it will try to
  use the system `sudo`, which is disabled by default.

## Details

The specific operations that this script does is:

1. Downloads the Godot binary ZIP file for the specified version to `/tmp`
   (using the system `curl` command, forcing SSL certificate checks). It is
   hard-coded to get it from the official Godot releases on GitHub
   ([https://github.com/godotengine](https://github.com/godotengine)), the same
   place that the download button on the website gets it from.
2. Unzips the ZIP file using the system `unzip` command.
3. Asks for `sudo` permission, if the specified user is not the current user (by
   default, asks for `sudo` as `root`).
4. As the specified user: sets the ownership of the Godot binary to that user
   (by default, `root`) using the system `chown` command.
5. As the specified user: moves the Godot binary into the specified directory
   (by default, `/usr/local/bin`).
6. As the specified user: creates symlinks as requested, in the specified
   directory, to the newly unpacked binary. Overwrites existing symlinks without
   asking.
7. Cleans up the downloaded and unzipped files in `/tmp`.

## Disclaimer

This program does stuff to your system which may break things, including running
commands as `root` by default. It also downloads software from the Internet and
installs it onto your computer. I can't be held responsible for any damage to
your system as a result of using this.

I have made every effort to ensure it is safe, as detailed above (for example,
checking SSL on the download, and only running the necessary commands as root).
Also, by default it installs into `/usr/local/bin` which is the normal place for
software installed outside of the system package manager, so it should not
interfere with system packages.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
