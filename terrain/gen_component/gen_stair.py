def generate_stairs_xml(num_steps=5, step_width=1, step_height=0.2, step_length=1, horizontal_shift=0.5):
    xml_content = "<worldbody>\n"
    xml_content += '    <body name="stairs" pos="0 0 0">\n'
    
    for i in range(num_steps):
        z = i * step_height
        x = i * horizontal_shift
        xml_content += f'        <geom type="box" size="{step_length / 2} {step_width / 2} {step_height / 2}" pos="{x} 0 {z}" material="mat_stairs"/>\n'
    
    xml_content += '    </body>\n'
    xml_content += "</worldbody>\n"
    return xml_content

terrain_xml = generate_stairs_xml()
with open("component/stair.xml", "w") as f:
    f.write(terrain_xml)
