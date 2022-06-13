#!/usr/bin/env bash

# usage:
# playlist_converter.sh itunes-to-walkman
# playlist_converter.sh walkman-to-itunes

scriptpath="$( cd -- "$(dirname "$0")" &> /dev/null; pwd -P )"

green='\033[0;32m'
orange='\033[0;33m'
nc='\033[0m'
bold=$(tput bold)

if [ ! -d "${scriptpath}/itunes_playlists" ]; then
    echo "'itunes_playlists' folder not detected. Making folder in script directory."
    mkdir -p "${scriptpath}/itunes_playlists"
fi
if [ ! -d "${scriptpath}/walkman_playlists" ]; then
    echo "'walkman_playlists' folder not detected. Making folder in script directory."
    mkdir -p "${scriptpath}/walkman_playlists"
fi

processed_file_counter=0
if [ $1 == "itunes-to-walkman" ]; then
    if [ ! -f "${scriptpath}/itunes_to_walkman_playlist.py" ]; then
        echo -e "${orange}'itunes_to_walkman_playlist.py' script missing${nc}"
        exit 1
    fi
    if [ -z "$(ls -A "${scriptpath}/itunes_playlists")" ]; then
        echo -e "${orange}No files detected in '${scriptpath}/itunes_playlists'${nc}"
        exit 1
    fi
    for playlist in ${scriptpath}/itunes_playlists/*; do
        python3 ${scriptpath}/itunes_to_walkman_playlist.py "${playlist#"${scriptpath}/itunes_playlists/"}"
        echo -e "${orange}'${playlist#"${scriptpath}/itunes_playlists/"}' processed${nc}"
        ((processed_file_counter+=1))
    done
elif [ $1 == "walkman-to-itunes" ]; then
    if [ ! -f "${scriptpath}/walkman_to_itunes_playlist.py" ]; then
        echo -e "${orange}'walkman_to_itunes_playlist.py' script missing${nc}"
        exit 1
    fi
    if [ -z "$(ls -A "${scriptpath}/walkman_playlists")" ]; then
        echo -e "${orange}No files detected in '${scriptpath}/walkman_playlists'${nc}"
        exit 1
    fi
    for playlist in ${scriptpath}/walkman_playlists/*; do
        python3 ${scriptpath}/walkman_to_itunes_playlist.py "${playlist#"${scriptpath}/walkman_playlists/"}"
        echo -e "${orange}'${playlist#"${scriptpath}/walkman_playlists/"}' processed${nc}"
        ((processed_file_counter+=1))
    done
else
    echo -e "${orange}Command requires one argument (itunes-to-walkman, walkman-to-itunes)${nc}"
    unset green orange nc bold processed_file_counter
    exit 1
fi

echo -e "${green}${bold}Processed $processed_file_counter files${nc}"
unset green orange nc bold processed_file_counter
