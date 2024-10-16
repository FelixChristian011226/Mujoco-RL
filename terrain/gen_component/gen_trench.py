import argparse

def generate_trench_xml(length=5, unit_length=0.5, x_scale=1.0, y_scale=1.0, z_scale=1.0):
    xml_content = "<worldbody>\n"
    xml_content += f'    <body name="trench" pos="0 0 0">\n'
    
    x_unit = unit_length * x_scale
    y_unit = unit_length * y_scale
    z_unit = unit_length * z_scale
    
    xml_content += f'    <geom type="box" size="{round(x_scale * length / 2, 4)} {round(y_unit, 4)} {round(z_unit / 2, 4)}" pos="0 0 {round(z_unit/2, 4)}" material="mat_trench"/>\n'
    xml_content += f'    <geom type="box" size="{round(x_scale * length / 2, 4)} {round(y_unit / 2, 4)} {round(z_unit, 4)}" pos="0 {round(y_unit*3/2, 4)} {round(z_unit, 4)}" material="mat_trench"/>\n'
    xml_content += f'    <geom type="box" size="{round(x_scale * length / 2, 4)} {round(y_unit / 2, 4)} {round(z_unit, 4)}" pos="0 {round(-y_unit*3/2, 4)} {round(z_unit, 4)}" material="mat_trench"/>\n'
    xml_content += f'    <geom type="box" size="{round(x_scale * length / 2, 4)} {round(y_unit / 2, 4)} {round(z_unit*3/2, 4)}" pos="0 {round(y_unit*5/2, 4)} {round(z_unit*5/2, 4)}" material="mat_trench"/>\n'
    xml_content += f'    <geom type="box" size="{round(x_scale * length / 2, 4)} {round(y_unit / 2, 4)} {round(z_unit*3/2, 4)}" pos="0 {round(-y_unit*5/2, 4)} {round(z_unit*5/2, 4)}" material="mat_trench"/>\n'
    xml_content += f'    <geom type="box" size="{round(x_scale * length / 2, 4)} {round(y_unit / 2, 4)} {round(z_unit*2, 4)}" pos="0 {round(y_unit*7/2, 4)} {round(z_unit*5, 4)}" material="mat_trench"/>\n'
    xml_content += f'    <geom type="box" size="{round(x_scale * length / 2, 4)} {round(y_unit / 2, 4)} {round(z_unit*2, 4)}" pos="0 {round(-y_unit*7/2, 4)} {round(z_unit*5, 4)}" material="mat_trench"/>\n'

    xml_content += f'    <geom type="box" size="{round(x_unit / 2, 4)} {round(y_unit * 2, 4)} {round(z_unit / 2, 4)}" pos="{round(x_scale * length / 2 + x_unit / 2, 4)} 0 {round(z_unit/2, 4)}" material="mat_trench"/>\n'
    xml_content += f'    <geom type="box" size="{round(x_unit / 2, 4)} {round(y_unit * 2, 4)} {round(z_unit / 2, 4)}" pos="{round(-x_scale * length / 2 - x_unit / 2, 4)} 0 {round(z_unit/2, 4)}" material="mat_trench"/>\n'    
    xml_content += f'    <geom type="box" size="{round(x_unit / 2, 4)} {round(y_unit * 3, 4)} {round(z_unit, 4)}" pos="{round(x_scale * length / 2 + x_unit / 2, 4)} 0 {round(z_unit*2, 4)}" material="mat_trench"/>\n'
    xml_content += f'    <geom type="box" size="{round(x_unit / 2, 4)} {round(y_unit * 3, 4)} {round(z_unit, 4)}" pos="{round(-x_scale * length / 2 - x_unit / 2, 4)} 0 {round(z_unit*2, 4)}" material="mat_trench"/>\n'
    xml_content += f'    <geom type="box" size="{round(x_unit / 2, 4)} {round(y_unit * 4, 4)} {round(z_unit*2, 4)}" pos="{round(x_scale * length / 2 + x_unit / 2, 4)} 0 {round(z_unit*5, 4)}" material="mat_trench"/>\n'
    xml_content += f'    <geom type="box" size="{round(x_unit / 2, 4)} {round(y_unit * 4, 4)} {round(z_unit*2, 4)}" pos="{round(-x_scale * length / 2 - x_unit / 2, 4)} 0 {round(z_unit*5, 4)}" material="mat_trench"/>\n'


    xml_content += '    </body>\n'
    xml_content += "</worldbody>\n"
    return xml_content


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate MuJoCo XML for trench.")
    parser.add_argument("length", type=int, default=6, help="Length on the x-axis")
    parser.add_argument("unit_length", type=float, default=2.0, help="Length of a unit")
    parser.add_argument("y_scale", type=float, default=0.5, help="Scale on the y-axis")
    parser.add_argument("z_scale", type=float, default=4.0, help="Scale on the z-axis")

    args = parser.parse_args()

    terrain_xml = generate_trench_xml(args.length, args.unit_length, args.y_scale, args.z_scale)
    with open("component/trench.xml", "w") as f:
        f.write(terrain_xml)