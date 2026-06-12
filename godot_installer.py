#!/usr/bin/env python3

import argparse
import getpass
import os.path
import shlex
import shutil
import subprocess
import sys
import tempfile

# TODO: Doing Windows will require some work related to filename and symlinks.
OS = 'linux.x86_64'

def run_cmd(cmd, sudo_as=None):
  """Logs and runs a command."""
  if sudo_as:
    cmd = get_sudo_prefix(sudo_as) + cmd
  print(shlex.join(cmd), file=sys.stderr)
  subprocess.run(cmd)

def get_sudo_prefix(user):
  # Get the 'sudo' command prefix, based on the requested user. May return
  # empty, if the user is self.
  if user == getpass.getuser():
    return []

  if user == 'root':
    return ['sudo']

  return ['sudo', '-u', user]

def download_to_tmp(url):
  basename = os.path.basename(url)
  dest_path = os.path.join(tempfile.gettempdir(), basename)
  # Use curl instead of urllib to show a progress bar.
  run_cmd(['curl', '--ssl-reqd', '-L', url, '-o', dest_path])
  return dest_path

def install(zip_file_path, version, symlinks, user, dir):
  # Needed, as we'll be changing directory.
  binary = f'Godot_v{version}_{OS}'
  dir = os.path.abspath(dir)
  # Extract and move into the given directory.
  with tempfile.TemporaryDirectory() as temp_dir:
    print(f'cd {shlex.quote(temp_dir)}', file=sys.stderr)
    os.chdir(temp_dir)
    run_cmd(['unzip', zip_file_path])

    files = os.listdir('.')
    if not files:
      print('Error: No files extracted.', file=sys.stderr)
      return 1

    if user != getpass.getuser():
      run_cmd(['chown', f'{user}:{user}'] + files, sudo_as=user)

    run_cmd(['mv'] + files + [dir], sudo_as=user)

  # Now set up symlinks.
  if symlinks:
    os.chdir(dir)
    for symlink in symlinks:
      run_cmd(['ln', '-fs', binary, symlink], sudo_as=user)

def download_and_install(version, symlinks, user, dir):
  print(f'{version}, {symlinks}, {user}, {dir}')

  if not os.path.isdir(dir):
    print(f'{dir} is not an existing directory', file=sys.stderr)
    return 1

  url = f'https://github.com/godotengine/godot-builds/releases/download/{version}/Godot_v{version}_{OS}.zip'
  zip_file_path = download_to_tmp(url)

  try:
    install(zip_file_path, version, symlinks, user, dir)
  finally:
    os.remove(zip_file_path)

def main(args=None):
  if args is None:
    args = sys.argv[1:]

  parser = argparse.ArgumentParser(
            prog='godot_installer',
            description='Downloads and installs Godot',
          )

  parser.add_argument('version',
                      help='Godot version (e.g. 4.5-beta4)')
  parser.add_argument('-s', metavar='SYMLINK', dest='symlinks', action='append',
                      help='Symbolic links to alias (e.g. -s godot -s godot4.5)')
  parser.add_argument('--user', default='root',
                      help='User to own binary and symlinks (default: root)')
  parser.add_argument('--dir', default='/usr/local/bin',
                      help='Directory to store binary and symlinks in (default: /usr/local/bin)')

  args = parser.parse_args(args)

  return download_and_install(args.version, args.symlinks, args.user, args.dir)

if __name__ == '__main__':
  sys.exit(main())
