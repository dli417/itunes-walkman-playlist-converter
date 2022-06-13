#!/usr/bin/env python

import sys
import os
from os import path

cwd = os.path.dirname(os.path.realpath(__file__))

# check files and folders exist
if not path.exists(f"{cwd}/itunes_playlists"):
    print(f"Error: directory missing: '{cwd}/itunes_playlists'")
    sys.exit()
if not path.exists(f"{cwd}/walkman_playlists"):
    print(f"Error: directory missing: '{cwd}/walkman_playlists'")
    sys.exit()
if not path.exists(f"{cwd}/walkman_playlists/{sys.argv[1]}"):
    print(f"Error: specified playlist file not found: '{cwd}/walkman_playlists/{sys.argv[1]}'")
    sys.exit()

extinf_counter = 0
song_path_counter = 0
extm3u_counter = 0
unknown_line_format = 0
with open(f"{cwd}/walkman_playlists/{sys.argv[1]}", 'r') as walkman, open(f"{cwd}/itunes_playlists/{sys.argv[1]}", 'w+') as itunes:
    for line in walkman:
        if line.startswith("#EXTINF:"):
            itunes.write("#EXTINF:,\n")
            extinf_counter += 1
        elif "/" in line:
            itunes.write("/Users/danielli/Music/Music/Media.localized/{0}".format(line))
            song_path_counter += 1
        elif line == "#EXTM3U\n":
            itunes.write(line)
            extm3u_counter += 1
        else:
            print(f"Error: unknown line format: '{line[:len(line)-1]}'")
            unknown_line_format += 1

    print(f"{extinf_counter} songs converted to iTunes format")

    # final error checking
    itunes.seek(0)
    walkman.seek(0)
    itunes_lines = len(itunes.readlines())
    walkman_lines = len(walkman.readlines())

    if itunes_lines != walkman_lines:
        print(f"Error: iTunes playlist line count ({itunes_lines}) does not match Walkman playlist line count ({walkman_lines})")
    if extinf_counter != song_path_counter:
        print(f"Error: processed EXTINF lines ({extinf_counter}) does not match processed song path lines ({song_path_counter})")
    if extm3u_counter != 1:
        print(f"Error: EXTM3U header count ({extm3u_counter}) is not 1")
    if unknown_line_format != 0:
        print(f"Error: unknown line format ocurred {unknown_line_format} times")
