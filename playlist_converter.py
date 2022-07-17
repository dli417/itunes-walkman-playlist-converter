#!/usr/bin/env python

"""
Converts iTunes playlists to Walkman format and vice versa. Place iTunes playlists in ./itunes_playlists and Walkman playlists in ./walkman_playlists and run script.

Usage: playlist_converter.py [i2w | w2i]

i2w: iTunes to Walkman
w2i: Walkman to iTunes

"""

import sys
import os
from unicodedata import normalize, is_normalized


class m_colours:
    CLEAR = '\033[0m'
    GREEN = '\033[0;32m'
    ORANGE = '\033[0;33m'
    RED = '\033[031m'


def check_directories_files_exist(dir_name):
    for folder in ('itunes_playlists', 'walkman_playlists'):
        if not os.path.isdir(f"{cwd}/{folder}"):
            print(f"'{folder}' doesn't exist, creating folder")
            os.mkdir(os.path.join(cwd, folder))
    files_to_convert = []
    for file in os.listdir(f"{cwd}/{dir_name}"):
        if file.endswith('.m3u8'):
            files_to_convert.append(file)
    if len(files_to_convert) == 0:
        sys.exit(f"{m_colours.RED}Error: no '.m3u8' files detected in '{dir_name}'{m_colours.CLEAR}")
    return files_to_convert


def error_checks(read_format, write_format, file_in, file_out, extinf_counter, song_path_counter, extm3u_counter, unknown_line_format):
    conversion_errors_status = 0
    file_in.seek(0)
    file_out.seek(0)
    file_in_lines = len(file_in.readlines())
    file_out_lines = len(file_out.readlines())

    if extinf_counter != song_path_counter:
        print(f"{m_colours.RED}Error:{m_colours.CLEAR} processed EXTINF lines ({extinf_counter}) does not match processed song path lines ({song_path_counter})")
        conversion_errors_status = 1
    if extm3u_counter != 1:
        print(f"{m_colours.RED}Error:{m_colours.CLEAR} EXTM3U header count ({extm3u_counter}) is not 1")
        conversion_errors_status = 1
    if unknown_line_format != 0:
        print(f"{m_colours.RED}Error:{m_colours.CLEAR} unknown line format occured {unknown_line_format} times")
        conversion_errors_status = 1
    if (file_in_lines % 2) == 0:
        print(f"{m_colours.RED}Error:{m_colours.CLEAR} {read_format} playlist file has even number of lines")
        conversion_errors_status = 1
    file_in_songs = (file_in_lines - 1) // 2
    if (file_out_lines % 2) == 0:
        print(f"{m_colours.RED}Error:{m_colours.CLEAR} {write_format} playlist file has even number of lines")
        conversion_errors_status = 1
    file_out_songs = (file_out_lines - 1) // 2

    if file_in_songs == file_out_songs:
        result_message_colour = m_colours.ORANGE
    else:
        result_message_colour = m_colours.RED
        conversion_errors_status = 1
    return result_message_colour, file_in_songs, file_out_songs, conversion_errors_status


def converter(file, read_format, write_format):
    if read_format == "itunes":
        # song_path_length calculated from length of "/Users/danielli/Music/Music/Media.localized/"
        song_path_length = 44
    extinf_counter = 0
    song_path_counter = 0
    extm3u_counter = 0
    unknown_line_format = 0
    with open(f"{cwd}/{read_format}_playlists/{file}", 'r') as file_in, open(f"{cwd}/{write_format}_playlists/{file}", 'w+') as file_out:
        for line in file_in:
            if line.startswith("#EXTINF:"):
                file_out.write("#EXTINF:,\n")
                extinf_counter += 1
            elif read_format == "itunes" and line.startswith("/Users/danielli/Music/Music/Media.localized/"):
                # # normalise all song lines
                # walkman.write(normalize('NFC', line[song_path_length:]))
                # check and normalise lines that need to be normalised only
                trimmed_line = line[song_path_length:]
                if not is_normalized('NFC', trimmed_line):
                    print(f"Normalising to Unicode NFC: '{trimmed_line[:len(trimmed_line)-1]}'")
                    trimmed_line = normalize('NFC', trimmed_line)
                file_out.write(trimmed_line)
                song_path_counter += 1
            elif read_format == "walkman" and "/" in line:
                file_out.write("/Users/danielli/Music/Music/Media.localized/{0}".format(line))
                song_path_counter += 1
            elif line == "#EXTM3U\n":
                file_out.write(line)
                extm3u_counter += 1
            else:
                print(f"{m_colours.RED}Error:{m_colours.CLEAR} unknown line format: '{line[:len(line)-1]}'")
                unknown_line_format += 1

        # final error checking
        result_message_colour, file_in_songs, file_out_songs, conversion_errors_status = error_checks(read_format, write_format, file_in, file_out, extinf_counter, song_path_counter, extm3u_counter, unknown_line_format)
        print(f"{result_message_colour}{file_out_songs}/{file_in_songs} songs converted from '{file}'{m_colours.CLEAR}")
        return conversion_errors_status


cwd = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
    # check arguments
    if len(sys.argv) != 2:
        sys.exit(f"{m_colours.RED}Error: script takes one argument - try 'i2w' or 'w2i'{m_colours.CLEAR}")
    if sys.argv[1] == "i2w":
        read_format = "itunes"
        write_format = "walkman"
    elif sys.argv[1] == "w2i":
        read_format = "walkman"
        write_format = "itunes"
    else:
        sys.exit(f"{m_colours.RED}Unknown argument: try 'i2w' or 'w2i'{m_colours.CLEAR}")

    # check files and folders exist
    files_to_convert = check_directories_files_exist(f"{read_format}_playlists")

    files_to_convert_count = len(files_to_convert)
    conversion_errors_count = 0

    for file in files_to_convert:
        conversion_errors_status = converter(file, read_format, write_format)
        if conversion_errors_status == 1:
            conversion_errors_count += 1

    successful_conversions_count = files_to_convert_count - conversion_errors_count

    if conversion_errors_count == 0:
        summary_message_colour = m_colours.GREEN
    else:
        summary_message_colour = m_colours.RED
    print(f"{summary_message_colour}{successful_conversions_count}/{files_to_convert_count} files successfully converted without errors{m_colours.CLEAR}")
