import argparse
import random
import numpy as np

def check_collision(new_pos, existing_positions, size):
    for pos in existing_positions:
        distance = np.linalg.norm(np.array(new_pos) - np.array(pos))
        if distance < size:  # 这里的size可以是椭球的半径和
            return True
    return False

def generate_pebble_path_xml(path_length=2, path_width=2, num_levels=7, level_height=0.4, density=10):
    xml_content = "<worldbody>\n"
    existing_positions = []

    for level in range(num_levels):
        for _ in range(density):
            # while True:
                # x = random.uniform(-path_length / 2, path_length / 2)
                # y = random.uniform(-path_width / 2, path_width / 2)
                # z = level * level_height
                
                # radius_x = random.uniform(0.07, 0.1)
                # radius_y = random.uniform(0.04, 0.07)
                # radius_z = random.uniform(0.03, 0.04)
                # size = radius_x + 0.1 
                
                # if not check_collision((x, y, z), existing_positions, size):
                #     existing_positions.append((x, y, z))
                #     z_rotation = random.uniform(0, 360)
                #     euler_str = f'euler="0 0 {round(z_rotation, 4)}"'
                    
                    

                #     # xml_content += '    <body>\n'
                #     # xml_content += '    <freejoint/>\n'
                #     # xml_content += f'        <geom type="ellipsoid" density="100000" conaffinity="1" condim="1" size="{round(radius_x, 4)} {round(radius_y, 4)} {round(radius_z, 4)}" pos="{round(x, 4)} {round(y, 4)} {round(z+0.06, 4)}" {euler_str} material="mat_pebble"/>\n'
                #     # xml_content += '    </body>\n'


                #     break  # 找到合适的位置后退出循环

            # 此段注释后，取消上文注释，可恢复碰撞检测，且石子会受重力影响及相互碰撞
            # 起
            x = random.uniform(-path_length / 2, path_length / 2)
            y = random.uniform(-path_width / 2, path_width / 2)
            z = level * level_height
            
            radius_x = random.uniform(0.07, 0.1)
            radius_y = random.uniform(0.04, 0.07)
            radius_z = random.uniform(0.03, 0.04)
            z_rotation = random.uniform(0, 360)
            euler_str = f'euler="0 0 {round(z_rotation, 4)}"'
            xml_content += f'    <geom type="ellipsoid" size="{round(radius_x, 4)} {round(radius_y, 4)} {round(radius_z, 4)}" pos="{round(x, 4)} {round(y, 4)} {round(z+radius_z/2, 4)}" {euler_str} material="mat_pebble"/>\n'
            # 终

    xml_content += "</worldbody>\n"
    return xml_content

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate MuJoCo XML for pebbles.")
    parser.add_argument("num_levels", type=int, default=7, help="Number of levels")
    parser.add_argument("path_length", type=float, default=2.0, help="Length of pebble road")
    parser.add_argument("path_width", type=float, default=2.0, help="Width of pebble road")
    parser.add_argument("level_height", type=float, default=0.4, help="Height between levels")
    parser.add_argument("density", type=int, default=50, help="Number of stones per level")

    args = parser.parse_args()

    terrain_xml = generate_pebble_path_xml(args.path_length, args.path_width, args.num_levels, args.level_height, args.density)
    with open("component/pebble.xml", "w") as f:
        f.write(terrain_xml)