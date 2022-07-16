#!/usr/bin/env python

import sys
import os
from os import path
from unicodedata import normalize, is_normalized


class m_colours:
    CLEAR = '\033[0m'
    ORANGE = '\033[0;33m'
    RED = '\033[031m'


cwd = os.path.dirname(os.path.realpath(__file__))

# check files and folders exist
if not path.exists(f"{cwd}/itunes_playlists"):
    print(f"{m_colours.RED}Error:{m_colours.CLEAR} directory missing: '{cwd}/itunes_playlists'")
    sys.exit()
if not path.exists(f"{cwd}/walkman_playlists"):
    print(f"{m_colours.RED}Error:{m_colours.CLEAR} directory missing: '{cwd}/walkman_playlists'")
    sys.exit()
if not path.exists(f"{cwd}/itunes_playlists/{sys.argv[1]}"):
    print(f"{m_colours.RED}Error:{m_colours.CLEAR} specified playlist file not found: '{cwd}/itunes_playlists/{sys.argv[1]}'")
    sys.exit()

# song_path_length calculated from length of "/Users/danielli/Music/Music/Media.localized/"
song_path_length = 44
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
            print(f"{m_colours.RED}Error:{m_colours.CLEAR} unknown line format: '{line[:len(line)-1]}'")
            unknown_line_format += 1

    # print(f"{extinf_counter} songs converted to Walkman format")

    # final error checking
    itunes.seek(0)
    walkman.seek(0)
    itunes_lines = len(itunes.readlines())
    walkman_lines = len(walkman.readlines())

    if itunes_lines != walkman_lines:
        print(f"{m_colours.RED}Error:{m_colours.CLEAR} iTunes playlist line count ({itunes_lines}) does not match Walkman playlist line count ({walkman_lines})")
    if extinf_counter != song_path_counter:
        print(f"{m_colours.RED}Error:{m_colours.CLEAR} processed EXTINF lines ({extinf_counter}) does not match processed song path lines ({song_path_counter})")
    if extm3u_counter != 1:
        print(f"{m_colours.RED}Error:{m_colours.CLEAR} EXTM3U header count ({extm3u_counter}) is not 1")
    if unknown_line_format != 0:
        print(f"{m_colours.RED}Error:{m_colours.CLEAR} unknown line format occured {unknown_line_format} times")

    if (itunes_lines % 2) == 0:
        print(f"{m_colours.RED}Error:{m_colours.CLEAR} iTunes playlist file has even number of lines")
    itunes_songs = (itunes_lines - 1) // 2
    if (walkman_lines % 2) == 0:
        print(f"{m_colours.RED}Error:{m_colours.CLEAR} Walkman playlist file has even number of lines")
    walkman_songs = (walkman_lines - 1) // 2

    if itunes_songs == walkman_songs:
        # orange text
        result_message_colour = m_colours.ORANGE
    else:
        # red text
        result_message_colour = m_colours.RED

    print(f"{result_message_colour}{walkman_songs}/{itunes_songs} songs converted from '{sys.argv[1]}'{m_colours.CLEAR}")
