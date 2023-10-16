from src.tile_api import TileApi
from src.bounding_volume import Sphere
from src.wgs84 import cartesian_from_degrees

import argparse
from pathlib import Path
import sys

from tqdm import tqdm


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--api-key",
                        help="your Google Maps 3d Tiles API key",
                        required=True)
    parser.add_argument("-c", "--coords",
                        help="longitude latitude [degrees]",
                        type=float,
                        nargs='+',
                        required=True)
    parser.add_argument("-r", "--radius",
                        help="radius around provided long/lat to fetch [m]",
                        type=float, required=True)
    parser.add_argument("-o", "--out",
                        help="output directory to place tiles in",
                        required=True)

    args = parser.parse_args()
    if len(args.coords) != 2:
        print("Must provide two coordinates: -c <longitude> <latitude>")
        sys.exit(-1)

    api = TileApi(key=args.api_key)
    print("Traversing tile hierarchy...")
    tiles = list(tqdm(api.get(Sphere(
        cartesian_from_degrees(*args.coords),
        args.radius
    ))))

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    print("Downloading tiles...")
    for i, t in tqdm(enumerate(tiles), total=len(tiles)):
        with open(outdir / Path(f"{t.basename}.glb"), "wb") as f:
            f.write(t.data)
