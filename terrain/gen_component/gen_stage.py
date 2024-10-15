import argparse

def generate_stage_xml(num_steps=6, min_radius=0.2, step_height=0.1, horizontal_shift=0.2):
    xml_content = "<worldbody>\n"
    xml_content += f'    <body name="stage" pos="0 0 {round(step_height / 2, 4)}">\n'
    
    for i in range(num_steps):
        z = (num_steps-i-1) * step_height
        l = i * horizontal_shift + min_radius
        xml_content += f'        <geom type="box" size="{round(l, 4)} {round(l, 4)} {round(step_height / 2, 4)}" pos="0 0 {round(z, 4)}" material="mat_stage"/>\n'
    
    xml_content += '    </body>\n'
    xml_content += "</worldbody>\n"
    return xml_content


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate MuJoCo XML for stage.")
    parser.add_argument("num_steps", type=int, default=6, help="Number of steps")
    parser.add_argument("min_radius", type=float, default=0.2, help="Width of each step")
    parser.add_argument("step_height", type=float, default=0.1, help="Height of each step")
    parser.add_argument("horizontal_shift", type=float, default=0.2, help="Horizontal shift between steps")

    args = parser.parse_args()

    terrain_xml = generate_stage_xml(args.num_steps, args.min_radius, args.step_height, args.horizontal_shift)
    with open("component/stage.xml", "w") as f:
        f.write(terrain_xml)