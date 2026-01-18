# itunes-walkman-playlist-converter

Convert playlists (.m3u8 format) between iTunes and Walkman formats

## System requirements

Scripts have been successfully run on the following system:

- macOS Monterey 12.4 (21F79)
- GNU bash, version 5.1.16(1)-release (x86_64-apple-darwin21.1.0)
- Python 3.10.0
- Clone this repository to `$HOME/Projects/itunes-walkman-playlist-converter/`
- \[Optional\] Download `itunesexport` binary file to user's $HOME/.local/bin folder
  - <https://github.com/ericdaugherty/itunesexport-go/releases>
- \[Optional\] Copy `playlist-converter` script file to user's $HOME/.local/bin folder

## Usage

### Convert all iTunes playlists to Walkman format

Export iTunes library file from iTunes (required by `itunesexport`):

1. Open iTunes/Music.app
2. File -> Library -> Export Library...
3. Save `Library.xml` to `$HOME/Projects/itunes-walkman-playlist-converter/itunes_library_xml/Library.xml`

Run `playlist_converter` command

### Manual playlist conversion

Run `playlist_converter.py` once or manually create `itunes_playlists` and `walkman_playlists` folders

To convert iTunes playlists to Walkman format:

- Place iTunes playlists in `itunes_playlists` folder
- Run `playlist_converter.py i2w`
- Find Walkman formatted playlists in `walkman_playlists` folder

To convert Walkman playlists to iTunes format:

- Place Walkman playlists in `walkman_playlists` folder
- Run `playlist_converter.py w2i`
- Find iTunes formatted playlists in `itunes_playlists` folder
