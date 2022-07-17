# itunes-walkman-playlist-converter

Convert playlists (.m3u8 format) between iTunes and Walkman formats

## System requirements

Scripts have been successfully run on the following system:

- macOS Monterey 12.4 (21F79)
- GNU bash, version 5.1.16(1)-release (x86_64-apple-darwin21.1.0)
- Python 3.10.0

## Usage

Run $ `playlist_converter.py` once or manually create `itunes_playlists` and `walkman_playlists` folders

To convert iTunes playlists to Walkman format:

- Place iTunes playlists in `itunes_playlists` folder
- $ `playlist_converter.py i2w`
- Find Walkman formatted playlists in `walkman_playlists` folder

To convert Walkman playlists to iTunes format:

- Place Walkman playlists in `walkman_playlists` folder
- $ `playlist_converter.py w2i`
- Find iTunes formatted playlists in `itunes_playlists` folder
