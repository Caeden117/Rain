import argparse
import json
import numpy as np
import xml.etree.ElementTree as ET
from scipy.spatial.transform import Rotation

### Rain (from Halo 3: ODST) by Martin O'Donnell and Michael Salvatori
### Map by Caeden117
### Source is released under the MIT License.
### This code was built on top of Nyri0's script for "Wait", which is also released under the MIT License.

BLENDER_FILE = "track.dae" # Local location for the exported COLLADA file to build walls from
SCALE = 5  # Scaling factor for the x and y axes
NS = {"xmlns": "http://www.collada.org/2005/11/COLLADASchema"}
HYPER_DURATION = -10
COLOR_MULTIPLIER = 20 # Used to multiply colors from certain materials; see below.

def get_args():
    parser = argparse.ArgumentParser(
        description='Generate geometry of the map')
    parser.add_argument('-o', dest='out_file', default='EasyOneSaber.dat', # Define the output difficulty/file here.
                        help='Path to the output json file')
    return parser.parse_args()

# Loads a COLLADA file from disk and extracts important information about each object in it.
# A basic cube is exported from every transform in the file, which means that you cannot use shortcuts like array/mirror modifiers to speed up the Blender process.
# Collections are you best friend for making these kinds of maps. They are your BEST friend.
def load_model(filename):
    root = ET.parse(filename).getroot() # Load base file into memory
    nodes = (root.find("xmlns:library_visual_scenes", NS) # Dig into the tree a bit to find our list of transforms
             .find("xmlns:visual_scene", NS)
             .findall("xmlns:node", NS))
    model = []
    # Loop through all of them
    for node in nodes:
        name = node.get("name")
        transform = np.array(
            list(map(float, node.find("xmlns:matrix", NS).text.split())) # Get the Transform matrix, we'll use this for calculations later.
        ).reshape((4, 4))
        # The following code for obtaining the color from a material was copied with permission from Reaxt.
        color = False
        if(node.find("xmlns:instance_geometry", NS).find("xmlns:bind_material", NS)): # If our transform contains a material...
            matname = "-".join(node.find("xmlns:instance_geometry",NS) # Dig into the tree a bit further to find the name of our material
                          .find("xmlns:bind_material", NS)
                          .find("xmlns:technique_common", NS)
                          .find("xmlns:instance_material", NS)
                          .get("symbol", NS).split("-")[:-1])
            # Then we go to a completely other spot in the tree to find the Material properties
            effects = root.find("xmlns:library_effects",NS).findall("xmlns:effect",NS)
            for effect in effects:
                if(effect.get("id") == matname+"-effect"):
                    rawColorArray = list(map(float,
                        effect.find("xmlns:profile_COMMON",NS) # Go a bit farther to find the color of our material
                            .find("xmlns:technique", NS)
                            .find("xmlns:lambert", NS)
                            .find("xmlns:diffuse",NS)
                            .find("xmlns:color", NS).text.split()))
                    # I pulled a lazy and multiplied the color values if the material wasn't named.
                    # Feel free to change it to something more proper, like "Light"
                    if "Material" in matname:
                        rawColorArray[0] *= COLOR_MULTIPLIER
                        rawColorArray[1] *= COLOR_MULTIPLIER
                        rawColorArray[2] *= COLOR_MULTIPLIER
                    color=np.array(rawColorArray)
        model.append((transform, name, color)) # Append the Transform matrix, transform name, and extracted color (if any) into our list.
    return model

# Take our list of transforms and generate Beat Saber obstacles from it.
# The "offset" parameter goes unused in Rain. See the original script for "Wait" for usage.
def add_model(walls, model, offset):
    # Additional rotation applied to the object
    add_rotation = np.zeros((4, 4))
    add_rotation[:3, :3] = Rotation.from_euler(
        "xyz", offset[3:6], degrees=True).as_matrix()

    for tr_init, name, color in model: # This is the information we extracted from the load_model function
        transform = (
            np.matmul(add_rotation, tr_init) + np.array( # We add some position/rotation offsets to the Transform matrix.
                [[0, 0, 0, offset[0]],
                 [0, 0, 0, offset[1]],
                 [0, 0, 0, offset[2]],
                 [0, 0, 0, 0]]
            )
        )

        position = transform[:3, 3] # Extract the Position from the 4th column of each row.
        scale = np.array([np.linalg.norm(transform[:3, i]) for i in range(3)]) # Extract scale by normalizing the diagonal of the matrix
        rotation = transform[:3, :3] / scale # Obtain the Rotation matrix by dividing the entire transform by the scale 
        euler = Rotation.from_matrix(rotation).as_euler('xyz', degrees=True) # Convert this into euler angles

        pivot_diff = np.array([0, -1, 0]) * scale # Difference in wall position brought about by the difference of obstacle pivot
        correction = pivot_diff - np.matmul(rotation, pivot_diff) # Get the offset to correct this difference with matrix multiplication

        # Our new position is the sum of our original position, then the multiplication of the rotation matrix and a modified scale matrix,
        # then the correction calculated above. 
        new_position = position + \
            np.matmul(rotation, np.array([1, -1, -1]) * scale) + correction

        # Extract information to put into our Beat Saber wall.
        scale_x = scale[1] * SCALE
        scale_y = scale[2] * SCALE
        start_x = new_position[1] * SCALE
        start_y = new_position[2] * SCALE

        # I pulled customData into its own object for easy modification
        customData = {
            "_position": [start_x, start_y],
            "_scale": [2*scale_x, 2*scale_y],
            "_rotation": offset[6], # Global rotation defined as an offset object (goes unused by this script) 
            "_localRotation": [-euler[1], -euler[2], euler[0]], # Local rotation calculated using our euler angles from earlier
            "_noteJumpStartBeatOffset": 4, # This is to have all walls in the file spawn 6 beats from the player
            # We use _track to animate dissolve properties of walls. "New Mombasa" was a design choice given the name of the setting in Halo 3: ODST.
            "_track": "New Mombasa"
        }

        # Add color to customData if we extracted one from the material
        if (not isinstance(color, bool)):
            customData["_color"] = [color[0], color[1], color[2], color[3]]

        walls.append({
            "_time": -new_position[0], # Negative X in Blender is "forward" in time, in Beats
            "_lineIndex": 0, # We are using Noodle Extensions, not Mapping Extensions, so normalize these values
            "_type": 0,
            "_duration": HYPER_DURATION if name.lower().startswith("hyper") else 2 * scale[0], # Goes unused in Rain
            "_width": 0,
            "_customData": customData # Set our customData from earlier.
        })

def main():
    args = get_args()

    walls = []

    # Generate main geometry and export them to our "walls" array
    add_model(walls, load_model(BLENDER_FILE), (0, 0, 0, 0, 0, 0, 0))

    walls.sort(key=lambda x: x["_time"]) # Sort generated walls by time (important)

    with open(args.out_file, "r") as json_file: # Open our designated output file
        song_json = json.load(json_file)

    song_json["_obstacles"] = walls # Completely replace walls with what we have generated
    song_json["_customData"] = { # We use some Custom Events in Rain to further enhance the experience
        "_customEvents": [
            { # The first Custom Event assigns a dissolve fade-in animation to all walls in the Blender file.
                "_time": 0,
                "_type": "AssignPathAnimation",
                "_data": {
                    "_track": "New Mombasa", # "New Mombasa" is our exported walls from the Blender file
                    "_duration": 0,
                    "_dissolve": [
                        [0, 0],    # At 0% through our jump, make the wall 0% visible.
                        [1, 0.25]  # At 25% through our jump, make the wall 100% visible.
                    ]
                }
            },
            { 
                # This second Custom Event assigns a dissolve fade-out animation to all walls in the Blender file when the song is finished.
                # We make use of the fact that Path animations and Track animations are multiplied together for obstacle/note dissolve.
                "_time": 338.75,
                "_type": "AnimateTrack",
                "_data": {
                    "_track": "New Mombasa"
                    "_duration": 5, # Fade all walls out over 5 beats
                    "_dissolve": [ 
                        [1, 0], # At 0% through the animation, make the wall 100% visible.
                        [0, 1]  # At 100% through the animation, make the wall 0% visible.
                    ]
                }
            }
        ]
    }

    with open(args.out_file, "w") as json_file: # Write our modified file back onto disk.
        json.dump(song_json, json_file)


main()
