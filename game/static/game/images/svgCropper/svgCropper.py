import os
import xml.etree.ElementTree as ET
from svgpathtools import Path, svg2paths
from pathlib import Path


def get_bounding_box(svg_file):
    # Parse the SVG and extract paths
    paths, _ = svg2paths(svg_file)

    # Get the bounding box for each path in the SVG
    min_x, min_y, max_x, max_y = (
        float("inf"),
        float("inf"),
        -float("inf"),
        -float("inf"),
    )
    for path in paths:
        for segment in path:
            # Get the bounds of the segment (this is approximate)
            bbox = segment.bbox()
            min_x = min(min_x, bbox[0])
            min_y = min(min_y, bbox[1])
            max_x = max(max_x, bbox[2])
            max_y = max(max_y, bbox[3])

    return (min_x, min_y, max_x, max_y)


def crop_svg(svg_file, bounding_box):
    # Parse the SVG file
    tree = ET.parse(svg_file)
    root = tree.getroot()

    # Set the viewBox attribute to the bounding box
    root.set(
        "viewBox",
        f"{bounding_box[0]} {bounding_box[1]} {bounding_box[2] - bounding_box[0]} {bounding_box[3] - bounding_box[1]}",
    )

    # Save the cropped SVG to a new file
    new_svg_file = svg_file.replace(".svg", "_cropped.svg")
    tree.write(new_svg_file)
    print(f"Cropped SVG saved as {new_svg_file}")


def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".svg"):
            svg_file = os.path.join(directory, filename)
            print(f"Processing {svg_file}...")

            bounding_box = get_bounding_box(svg_file)
            crop_svg(svg_file, bounding_box)


# Set the directory to your SVG files
directory = "../black-cards"
process_directory(Path(directory))
