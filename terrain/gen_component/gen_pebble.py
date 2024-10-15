import argparse
import random

def generate_pebble_path_xml(num_stones=100, path_length=5, path_width=1):
    xml_content = "<worldbody>\n"
    xml_content += '    <body name="pebble_path" pos="0 0 0">\n'
    
    for i in range(num_stones):
        x = random.uniform(-path_length / 2, path_length / 2)
        y = random.uniform(-path_width / 2, path_width / 2)
        z = 0 
        
        radius_x = random.uniform(0.05, 0.1)
        radius_y = random.uniform(0.04, 0.08)
        radius_z = random.uniform(0.02, 0.07)
        size_str = f"{radius_x} {radius_y} {radius_z}"
        
        z_rotation = random.uniform(0, 360)
        euler_str = f'euler="0 0 {z_rotation}"'

        xml_content += f'        <geom type="ellipsoid" size="{size_str}" pos="{x} {y} {z}" {euler_str} material="mat_pebble"/>\n'
    
    xml_content += '    </body>\n'
    xml_content += "</worldbody>\n"
    return xml_content

terrain_xml = generate_pebble_path_xml()
with open("component/pebble.xml", "w") as f:
    f.write(terrain_xml)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate MuJoCo XML for pebbles.")
    parser.add_argument("num_stones", type=int, default=100, help="Number of stones")
    parser.add_argument("path_length", type=float, default=5.0, help="Length of pebble road")
    parser.add_argument("path_width", type=float, default=0.5, help="Width of pebble road")

    args = parser.parse_args()

    terrain_xml = generate_pebble_path_xml(args.num_stones, args.path_length, args.path_width)
    with open("component/pebble.xml", "w") as f:
        f.write(terrain_xml)