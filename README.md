# Rain
Data files and scripts related to my Beat Saber map, Rain.

You can download the level here: *link still coming lmao*

See a video of the level here: *link still coming lmao*

[Rain](https://www.youtube.com/watch?v=yWh9l8RSkPk) is a song by Martin O'Donnell and Michael Salvatori for the game *Halo 3: ODST*. I've created a Beat Saber map for this song for the Noodle Games Volume 2 map pack, using mods such as [Noodle Extensions](https://github.com/Aeroluna/NoodleExtensions) and [Chroma](https://github.com/Aeroluna/Chroma/) to put a heavy emphasis on the atmosphere, achieving a feeling of walking the streets of New Mombasa.

The scripts and files used to create the Beat Saber map for Rain are publicly released under the MIT License for educational purposes regarding modchart creation, and the use of Noodle Extensions in Beat Saber levels. The Beat Saber map itself, however, is not.

## Downloading
To download these files, click the green `Code` button near the top of the page, then click `Download Zip`. Extract its contents to a folder of your choice, and you are ready to examine the code.

## Files

### `EasyStandard.bw`
This is a BeatWalls file (See "Tools Used") which defines the interfaces and wall structures for the map's rain and cloud effects.

### `SaneMapMerge.exe`
See "Tools Used" for a description on what this does. It's harmless, I promise.

### `generate_geometry.py`
This is a modified version of [Nyri0's mapping scripts for his song Wait](https://github.com/Nyrio/beat-saber-mapping-scripts), also released under the MIT License. This modified version also contains code copied (with permission) from Reaxt, and is commented throughout.

### `track.dae`
This is an exported COLLADA file from Blender, which contains New Mombasa: The road, light posts, and buildings throughout.

## Tools Used

### [BeatWalls](https://github.com/spookyGh0st/beatwalls)
BeatWalls was used to compile the `EasyStandard.bw` file into walls that represent the map's clouds and rain droplets.

### [Blender](blender.org)
Blender was used to model the road, light posts, and buildings of New Mombasa.

### [ChroMapper](https://github.com/Caeden117/ChroMapper) (Closed Beta)
ChroMapper was used to map the notes and lights for Rain, as well as for quick visualization with its 3D editor, and to make last-minute changes before combining the difficulties together.

ChroMapper is currently in Closed Beta, see more details in its repository.

### Sane Map Merge (Included in Repository)
`SaneMapMerge.exe` is a basic command-line tool which, as the name suggests, sanely merges two map difficulty files together.

This is because, during the creation of Rain, I used 3 difficulties: One for notes and BeatWalls, one for Blender walls, and one for the lightshow. `SaneMapMerge.exe` was used to combine everything into one single difficulty.

Source code can be released upon request, however I can safely assure everyone that it does not do anything harmful to your machine.
