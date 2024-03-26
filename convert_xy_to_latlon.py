import xml.etree.ElementTree as ET
import re
import os
from xml.dom.minidom import parseString

def read_file(file_path):
    """Reads the entire content of a file."""
    with open(file_path, 'r') as file:
        return file.read()

def convert_xy_to_latlon(x, y):
    """
    Convert x, y coordinates to lat, lon.
    This function is a placeholder. Replace it with actual conversion logic.
    """
    lat = float(x) / 10000000
    lon = float(y) / 10000000
    return lat, lon

def process_points_to_osm(input_text, output_file_path):
    osm_root = ET.Element("osm")
    node_id = -1  # Starting node ID; this script decrements ID for each point

    points_pattern = re.compile(r"point\s*\{\s*x:\s*([-\d.]+)\s*y:\s*([-\d.]+)\s*\}")

    for match in points_pattern.finditer(input_text):
        x, y = match.groups()
        lat, lon = convert_xy_to_latlon(x, y)

        node_attribs = {
            "id": str(node_id),
            "visible": "true",
            "lat": f"{lat:.8f}",
            "lon": f"{lon:.8f}"
        }
        ET.SubElement(osm_root, "node", node_attribs)
        node_id -= 1  # Ensure each node ID is unique

    # Convert the ElementTree to an XML string
    rough_string = ET.tostring(osm_root, 'utf-8')
    reparsed = parseString(rough_string)

    # Pretty print to the specified output file with newlines after each node
    with open(output_file_path, "w") as output_file:
        output_file.write(reparsed.toprettyxml(indent="  "))

# Specify the paths to your input and output files
current_directory = os.path.dirname(os.path.abspath(__file__))
input_file_path = os.path.join(current_directory, "base_map.txt")
output_file_path = os.path.join(current_directory, "output.osm")

# Process the input file to generate the OSM output
input_text = read_file(input_file_path)
process_points_to_osm(input_text, output_file_path)

print(f"Generated OSM file saved to: {output_file_path}")

