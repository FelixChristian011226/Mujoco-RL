import argparse

def generate_pit_xml(num_steps=6, min_radius=0.2, step_height=0.1, horizontal_shift=0.2):
    xml_content = "<worldbody>\n"
    xml_content += f'    <body name="pit" pos="0 0 {round(step_height / 2, 4)}">\n'
    
    boarder=0.1

    # 方向1
    xml_content += '        <body name="pit1" pos="0 0 0" euler="0 0 0">\n'
    xml_content += f'            <geom type="box" size="{round(min_radius+boarder, 4)} {round(min_radius+boarder, 4)} {round(step_height / 2, 4)}" pos="0 0 0" material="mat_pit"/>\n'
    for i in range(1, num_steps):
        z = i * step_height
        x = i * horizontal_shift + (horizontal_shift+boarder) / 2
        l = i * horizontal_shift + (horizontal_shift+boarder)
        xml_content += f'            <geom type="box" size="{round((horizontal_shift+boarder) / 2, 4)} {round(l, 4)} {round(step_height / 2, 4)}" pos="{round(x, 4)} 0 {round(z, 4)}" material="mat_pit"/>\n'
    xml_content += '        </body>\n'

    # 方向2
    xml_content += '        <body name="pit2" pos="0 0 0" euler="0 0 90">\n'
    xml_content += f'            <geom type="box" size="{round(min_radius+boarder, 4)} {round(min_radius+boarder, 4)} {round(step_height / 2, 4)}" pos="0 0 0" material="mat_pit"/>\n'
    for i in range(1, num_steps):
        z = i * step_height
        x = i * horizontal_shift + (horizontal_shift+boarder) / 2
        l = i * horizontal_shift
        xml_content += f'            <geom type="box" size="{round((horizontal_shift+boarder) / 2, 4)} {round(l, 4)} {round(step_height / 2, 4)}" pos="{round(x, 4)} 0 {round(z, 4)}" material="mat_pit"/>\n'
    xml_content += '        </body>\n'

    # 方向3
    xml_content += '        <body name="pit3" pos="0 0 0" euler="0 0 180">\n'
    xml_content += f'            <geom type="box" size="{round(min_radius+boarder, 4)} {round(min_radius+boarder, 4)} {round(step_height / 2, 4)}" pos="0 0 0" material="mat_pit"/>\n'
    for i in range(1, num_steps):
        z = i * step_height
        x = i * horizontal_shift + (horizontal_shift+boarder) / 2
        l = i * horizontal_shift + (horizontal_shift+boarder)
        xml_content += f'            <geom type="box" size="{round((horizontal_shift+boarder) / 2, 4)} {round(l, 4)} {round(step_height / 2, 4)}" pos="{round(x, 4)} 0 {round(z, 4)}" material="mat_pit"/>\n'
    xml_content += '        </body>\n'    

    # 方向4
    xml_content += '        <body name="pit4" pos="0 0 0" euler="0 0 270">\n'
    xml_content += f'            <geom type="box" size="{round(min_radius+boarder, 4)} {round(min_radius+boarder, 4)} {round(step_height / 2, 4)}" pos="0 0 0" material="mat_pit"/>\n'
    for i in range(1, num_steps):
        z = i * step_height
        x = i * horizontal_shift + (horizontal_shift+boarder) / 2
        l = i * horizontal_shift
        xml_content += f'            <geom type="box" size="{round((horizontal_shift+boarder) / 2, 4)} {round(l, 4)} {round(step_height / 2, 4)}" pos="{round(x, 4)} 0 {round(z, 4)}" material="mat_pit"/>\n'
    xml_content += '        </body>\n'

    xml_content += '    </body>\n'
    xml_content += "</worldbody>\n"
    return xml_content


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate MuJoCo XML for pit.")
    parser.add_argument("num_steps", type=int, default=6, help="Number of steps")
    parser.add_argument("min_radius", type=float, default=0.2, help="Width of each step")
    parser.add_argument("step_height", type=float, default=0.1, help="Height of each step")
    parser.add_argument("horizontal_shift", type=float, default=0.2, help="Horizontal shift between steps")

    args = parser.parse_args()

    terrain_xml = generate_pit_xml(args.num_steps, args.min_radius, args.step_height, args.horizontal_shift)
    with open("component/pit.xml", "w") as f:
        f.write(terrain_xml)