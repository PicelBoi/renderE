# renderE - The Open Source IntelliStar 1 Renderer

renderE is intended as a replacement for a VM emulating the IntelliStar 1, a system previously used by The Weather Channel to render Local on the 8s.

## renderE is far from finished! Expect bugs, issues, and crashes!

## Usage

1. Clone repository
2. Install Python dependencies
3. Run setup.py. This will guide you through setup, and allow you to change options
4. Place your background music in a folder called "bgm"
5. Run main.py.

### Arguments

The following arguments are supported by renderE:

* A positional argument will be treated as a URI for input. Set it to `wxs` for continuous music playback from the `bgm` folder.
* `-t` and `--trans` will give the window a transparent background (for overlaying).
* `-n` and `--noframe` will remove the window frame (useful for capture on mac).
* `-o` and `--offline` will disable fetching assets from the web.

### Commands

* Run `load.py local flavor`, replacing flavor with the i1 flavor, to load a presentation.
* Run `run.py local` to run the loaded presentation
* Run `toggleNationalLDL.py` with the next argument as either 1 or 0 to enable or disable the national LDL respectively. On Flat Rock, another argument (A or B) must be set to determine which LDL to cue.

### encodE

encodE is a data encoder bundled with RenderE. To use it, follow these instructions:

1. Set up renderE (including configuration)
2. While renderE is running, run encodE.py
3. Run a local forecast using the commands
