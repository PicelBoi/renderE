# renderE - The Open Source IntelliStar 1 Renderer

renderE is intended as a replacement for a VM emulating the IntelliStar 1, a system previously used by The Weather Channel to render Local on the 8s.

## renderE is far from finished! Expect bugs, issues, and crashes!

## Usage

1. Clone repository
2. Install Python dependencies
3. Run setup.py. This will guide you through setup, and allow you to change options
4. Place your background music in a folder called "bgm"
5. Run main.py

### Commands

- Run `load.py local flavor`, replacing flavor with the i1 flavor, to load a presentation.
- Run `run.py local` to run the loaded presentation
- Run `toggleNationalLDL.py` with the next argument as either 1 or 0 to enable or disable the national LDL respectively.

### encodE

encodE is a data encoder bundled with RenderE. To use it, follow these instructions:

1. Set up renderE (including configuration)
2. While renderE is running, run encodE.py.
3. Run a local forecast using the commands

## Environment Variables

RenderE uses the following environment variables for replacements to various paths used by the i1:

- RENDEREROOT: The folder renderE is in. This will probably be removed in the future.
- RENDERERSRC: The rsrc folder to be used. On the i1, this is located at /usr/local/twc/rsrc
- RENDEREMEDIA: The media folder. this is located at /media
- RENDEREDOMESTIC: The domestic data folder. On the i1, this is located at /usr/twc/domestic
- TWCCLIDIR: Used by the the original i1, located at /usr/twc. There is no equivalent for renderE.
- TWCPERSDIR: Used by the original i1. renderE's version is in the `domesticpy` folder.
- TWCDIR: Used by the original i1, although it's the same as TWCCLIDIR for some reason.

I suggest making a shell script to set your environment variables if you'd like to use them.
