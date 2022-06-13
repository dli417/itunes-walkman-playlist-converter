#!/usr/bin/env python

import sys
import os
from os import path
from unicodedata import normalize, is_normalized

cwd = os.getcwd()

# check files and folders exist
if not path.exists(f"{cwd}/itunes_playlists"):
    print(f"Error: directory missing: '{cwd}/itunes_playlists'")
    sys.exit()
if not path.exists(f"{cwd}/walkman_playlists"):
    print(f"Error: directory missing: '{cwd}/walkman_playlists'")
    sys.exit()
if not path.exists(f"{cwd}/itunes_playlists/{sys.argv[1]}"):
    print(f"Error: specified playlist file not found: '{cwd}/itunes_playlists/{sys.argv[1]}'")
    sys.exit()

song_path_length = len("/Users/danielli/Music/Music/Media.localized/")
extinf_counter = 0
song_path_counter = 0
extm3u_counter = 0
unknown_line_format = 0
with open(f"{cwd}/itunes_playlists/{sys.argv[1]}", 'r') as itunes, open(f"{cwd}/walkman_playlists/{sys.argv[1]}", 'w+') as walkman:
    for line in itunes:
        if line.startswith("#EXTINF:"):
            walkman.write("#EXTINF:,\n")
            extinf_counter += 1
        elif line.startswith("/Users/danielli/Music/Music/Media.localized/"):
            # normalise all song lines or check before normalising only those that need it
            # walkman.write(normalize('NFC', line[song_path_length:]))
            trimmed_line = line[song_path_length:]
            if not is_normalized('NFC', trimmed_line):
                print(f"Normalising to Unicode NFC: '{trimmed_line[:len(trimmed_line)-1]}'")
                trimmed_line = normalize('NFC', trimmed_line)
            walkman.write(trimmed_line)
            song_path_counter += 1
        elif line == "#EXTM3U\n":
            walkman.write(line)
            extm3u_counter += 1
        else:
            print(f"Error: unknown line format: '{line[:len(line)-1]}'")
            unknown_line_format += 1

    print(f"{extinf_counter} songs converted to Walkman format")

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
