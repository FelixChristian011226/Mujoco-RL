import argparse

def generate_stairs_xml(num_steps=5, step_width=1, step_height=0.2, step_length=1, horizontal_shift=0.5):
    xml_content = "<worldbody>\n"
    xml_content += f'    <body name="stairs" pos="0 0 {step_height / 2}">\n'
    
    for i in range(num_steps):
        z = i * step_height
        x = i * horizontal_shift
        xml_content += f'        <geom type="box" size="{step_width / 2} {step_length / 2} {step_height / 2}" pos="{x} 0 {z}" material="mat_stairs"/>\n'
    
    xml_content += '    </body>\n'
    xml_content += "</worldbody>\n"
    return xml_content


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate MuJoCo XML for stairs.")
    parser.add_argument("num_steps", type=int, default=6, help="Number of steps")
    parser.add_argument("step_width", type=float, default=2.0, help="Width of each step")
    parser.add_argument("step_height", type=float, default=0.5, help="Height of each step")
    parser.add_argument("step_length", type=float, default=4.0, help="Length of each step")
    parser.add_argument("horizontal_shift", type=float, default=1.0, help="Horizontal shift between steps")

    args = parser.parse_args()

    terrain_xml = generate_stairs_xml(args.num_steps, args.step_width, args.step_height, args.step_length, args.horizontal_shift)
    with open("component/stair.xml", "w") as f:
        f.write(terrain_xml)