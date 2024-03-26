import xml.etree.ElementTree as ET
import re
from xml.dom.minidom import parseString

def read_file(file_path):
    """Reads the entire content of a file."""
    with open(file_path, 'r') as file:
        return file.read()

def convert_xy_to_latlon(x, y):
    """
    Convert x, y coordinates to lat, lon.
    Placeholder function - replace with actual conversion logic.
    """
    lat = float(x) / 10000000
    lon = float(y) / 10000000
    return lat, lon

def process_roads_to_osm(input_text, output_file_path):
    osm_root = ET.Element("osm")
    nodes = []  # To store node elements temporarily
    ways = []  # To store way elements temporarily
    
    node_id_start = 1  # Initialize node ID start value
    way_id_start = -123324  # Initialize way ID start value

    road_sections = re.findall(r'road\s*{.*?}(?=\s*road\s*{|$)', input_text, re.DOTALL)

    for section in road_sections:
        way_element = ET.Element("way", id=str(way_id_start), visible="true")
        points = re.findall(r'point\s*{\s*x:\s*([-\d.]+)\s*y:\s*([-\d.]+)\s*}', section)
        
        for x, y in points:
            lat, lon = convert_xy_to_latlon(x, y)
            node_attribs = {"id": str(node_id_start), "visible": "true", "lat": f"{lat:.8f}", "lon": f"{lon:.8f}"}
            node_element = ET.Element("node", node_attribs)
            nodes.append(node_element)  # Store the node for later addition to the root
            
            ET.SubElement(way_element, "nd", ref=str(node_id_start))
            node_id_start += 1
        
        ET.SubElement(way_element, "tag", k="type", v="virtual")
        ways.append(way_element)  # Store the way for later addition to the root
        
        way_id_start -= 1

    # Add nodes and ways to the root element in order
    for node in nodes:
        osm_root.append(node)
    for way in ways:
        osm_root.append(way)

    # Convert to string using minidom for pretty printing
    rough_string = ET.tostring(osm_root, 'utf-8')
    reparsed = parseString(rough_string)
    pretty_xml_as_string = reparsed.toprettyxml(indent="  ")

    with open(output_file_path, "w") as output_file:
        output_file.write(pretty_xml_as_string)

input_file_path = "base_map.txt"  # Adjust to your input file's path
output_file_path = "outputroad2way.osm"

input_text = read_file(input_file_path)
process_roads_to_osm(input_text, output_file_path)

print(f"Generated OSM file saved to: {output_file_path}")

