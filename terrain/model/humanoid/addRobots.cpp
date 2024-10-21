// addRobots.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//
#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <fstream>
#include <string>
#include <random>
#include <cmath>
#include <vector>

using namespace std;

const int N = 3;
const int M = 3;
float scale = 4.0;

void addHead(const char* filename) {
	FILE* file = fopen(filename, "rt");
	char line[1024];

	while (fgets(line, 1024, file)) {
		printf("%s", line);
	}

	fclose(file);
}

void setFileToFile(const char* inputfile, const char* outputfile) {
	FILE* file = fopen(inputfile, "rt");
	char line[1024];
	fstream f;
	f.open(outputfile, ios::out);

	while (fgets(line, 1024, file)) {
		f << line;
	}
	f.close();
	fclose(file);
}

void addFileToFile(const char* inputfile, const char* outputfile) {
	FILE* file = fopen(inputfile, "rt");
	char line[1024];
	fstream f;
	f.open(outputfile, ios::out|ios::app);

	while (fgets(line, 1024, file)) {
		f << line;
	}
	f.close();
	fclose(file);
}

void addActuator(const char* filename, int idx) {
	FILE* file = fopen(filename, "rt");
	char line[1024];
	std::string from("2a_");
	std::string to = std::to_string(idx)+"_";

	while (fgets(line, 1024, file)) {
		std::string str(line);
		size_t start_pos = str.find(from);

		if (start_pos != std::string::npos) {
			str.replace(start_pos, from.length(), to);
		}
		printf("%s", str.c_str());
	}

	fclose(file);
}

void addActuatorToFile(const char* inputfile, const char* outputfile, int idx) {
	FILE* file = fopen(inputfile, "rt");
	char line[1024];
	fstream f;
	f.open(outputfile, ios::out|ios::app);
	std::string from("2a_");
	std::string to = std::to_string(idx)+"_";

	while (fgets(line, 1024, file)) {
		std::string str(line);
		size_t start_pos = str.find(from);

		if (start_pos != std::string::npos) {
			str.replace(start_pos, from.length(), to);
		}
		f << str;
	}

	f.close();
	fclose(file);
}

void addRobot(const char* filename, int i, int j, double tx, double ty, double angle, int idx)
{
	FILE* file = fopen(filename, "rt");
	char line[1024];
	std::string from("2a_");
	std::string to = std::to_string(idx)+"_";

	int no = 0;
	while (fgets(line, 1024, file)) {
		if (no == 0) {
			printf("    <body name=\"%s_torso\" pos=\"%lf %lf 1.5\" childclass=\"body\"  euler=\"0 0 %lf\">\n", to.c_str(), i*scale+tx, j*scale+ty, angle);
			no++;
			continue;
		}

		std::string str(line);
		size_t start_pos = str.find(from);

		if (start_pos != std::string::npos) {
			str.replace(start_pos, from.length(), to);
		}
		printf("%s", str.c_str());
	}

	fclose(file);
}

void addRobotToFile(const char* inputfile, const char* outputfile, int i, int j, double tx, double ty, double angle, int idx)
{
	FILE* file = fopen(inputfile, "rt");
	char line[1024];
	fstream f;
	f.open(outputfile, ios::out|ios::app);
	std::string from("2a_");
	std::string to = std::to_string(idx)+"_";

	int no = 0;
	while (fgets(line, 1024, file)) {
		if (no == 0) {
			f << "    <body name=\"" << to << "_torso\" pos=\"" << i*scale+tx << " " << j*scale+ty << " 1.5\" childclass=\"body\"  euler=\"0 0 " << angle << "\">\n";
			no++;
			continue;
		}

		std::string str(line);
		size_t start_pos = str.find(from);

		if (start_pos != std::string::npos) {
			str.replace(start_pos, from.length(), to);
		}
		f << str;
	}

	f.close();
	fclose(file);
}

void addRect(double x, double y, double z, double a, double b, double c, double dx, double dy, double dz)
{
	printf("    <geom type=\"box\" pos=\"%lf %lf %lf\" size=\"%lf %lf %lf\" rgba=\"0.5 0.5 0.5 1\" />\n",
		x+dx, y+dy, z+dz, a, b, c);
}

void addRectToFile(const char* outputfile, double x, double y, double z, double a, double b, double c, double dx, double dy, double dz)
{
	fstream f;
	f.open(outputfile, ios::out|ios::app);
	f << "    <geom type=\"box\" pos=\"" << x+dx << " " << y+dy << " " << z+dz << "\" size=\"" << a << " " << b << " " << c << "\" rgba=\"0.5 0.5 0.5 1\" />\n";
	f.close();
}

bool addRectRing(double w, double h, double a, double z, double dx, double dy, double dz)
{
	if ((h - 2 * a) <= 0.0001) {
		addRect(0, 0, z * 0.5, w, h, z, dx, dy, dz);
		return false;
	}

	addRect(0, (h-a), z*0.5, w, a, z, dx, dy, dz);
	addRect(0, (a-h), z*0.5, w, a, z, dx, dy, dz);
	addRect((w-a), 0, z * 0.5, a, h-2*a, z, dx, dy, dz);
	addRect((a-w), 0, z * 0.5, a, h-2*a, z, dx, dy, dz);
	return true;
}

bool addRectRingToFile(const char* outputfile, double w, double h, double a, double z, double dx, double dy, double dz)
{
	if ((h - 2 * a) <= 0.0001) {
		addRectToFile(outputfile, 0, 0, z * 0.5, w, h, z, dx, dy, dz);
		return false;
	}

	addRectToFile(outputfile, 0, (h-a), z*0.5, w, a, z, dx, dy, dz);
	addRectToFile(outputfile, 0, (a-h), z*0.5, w, a, z, dx, dy, dz);
	addRectToFile(outputfile, (w-a), 0, z * 0.5, a, h-2*a, z, dx, dy, dz);
	addRectToFile(outputfile, (a-w), 0, z * 0.5, a, h-2*a, z, dx, dy, dz);
	return true;
}

int mainTestStand()
{
	double dx = 0.2;
	double dy = -0.2;
	double dz = -1.5;

	double w = 2.0;
	double h = 2.0;
	double a = 0.2;
	double z = 0.1;

	addRectRing(w, h, a, z, dx, dy, dz);
	do {
		w -= 2 * a;
		if (w <= 0)
			break;

		h -= 2 * a;
		if (h <= 0)
			break;

		dz -= 2 * z;
		if (false == addRectRing(w, h, a, z, dx, dy, dz))
			break;

	} while (1);

	return 0;
}

void
buildGutter(
	double offsetx, double offsety, double offsetz,
	double head, double tail, double extent, double thick,
	double depth, double wid1, double wid2,
	int num)
{
	double x = 0;
	double y = 0;
	double z = 0;

	addRect(x, y, z, head, extent, thick, offsetx, offsety, offsetz);
	x+= head - thick;

	//for (int i = 0; i < num; i++)
	for (int i = 0; i <4; i++)
	{
		addRect(x, y, z-depth-thick, thick, extent, depth, offsetx, offsety, offsetz);
		x += -thick+wid1;
		addRect(x, y, z-depth*2-thick*2, wid1, extent, thick, offsetx, offsety, offsetz);
		x += -thick+wid1;
		addRect(x, y, z-depth-thick, thick, extent, depth, offsetx, offsety, offsetz);
		x += -thick*3+wid1;
		addRect(x, y, z, wid2, extent, thick, offsetx, offsety, offsetz);
		x += -thick*3 + wid1;
	}

	x += tail+thick;
	addRect(x, 0, 0, tail, extent, thick, offsetx, offsety, offsetz);
}

void
buildStair(double offsetx, double offsety, double offsetz,
	double length, double width, double height, 
	double deltaH, int num)
{
	double x = 0;
	double y = 0;
	double z = 0;

	for (int i = 0; i < num; i++) {
		addRect(x, y, z, length, width, height, offsetx, offsety, offsetz);
		z += deltaH;
		x += length*2.1;
	}
}

/**
 * 生成一个沟
 * @param outputfile 输出文件名
 */
void addGutterToFile(const char* outputfile, double offsetx, double offsety, double offsetz,
	double head, double tail, double extent, double thick,
	double depth, int rotate,
	int num)
{
	if(scale-head-tail < 0)
	{
		cout << "沟添加错误，请保持头尾长度小于总长度" << endl;
	}
	double x, y, z, wid1, wid2;
	switch (rotate)
	{
	case 0:
		x = -scale/2+head/2;
		y = 0;
		z = 0;
		wid1 = wid2 = ((scale-head-tail)/num + 2*thick)/2;

		addRectToFile(outputfile, x, y, z, head/2, extent/2, thick/2, offsetx, offsety, offsetz);
		x += head/2 - thick/2;

		for (int i = 0; i < num; i++)
		{
			addRectToFile(outputfile, x, y, z-depth/2-thick/2, thick/2, extent/2, depth/2, offsetx, offsety, offsetz);
			x += -thick/2+wid1/2;
			addRectToFile(outputfile, x, y, z-depth-thick, wid1/2, extent/2, thick/2, offsetx, offsety, offsetz);
			x += -thick/2+wid1/2;
			addRectToFile(outputfile, x, y, z-depth/2-thick/2, thick/2, extent/2, depth/2, offsetx, offsety, offsetz);
			x += -thick/2+wid2/2;
			addRectToFile(outputfile, x, y, z, wid2/2, extent/2, thick/2, offsetx, offsety, offsetz);
			x += -thick/2+wid2/2;
		}
		x += tail/2+thick/2;
		// 总长度: head + num*(wid1+wid2-2*thick) +tail = scale
		addRectToFile(outputfile, x, y, z, tail/2, extent/2, thick/2, offsetx, offsety, offsetz);
		break;
	
	case 1:
		x = 0;
		y = -scale/2+head/2;
		z = 0;
		wid1 = wid2 = ((scale-head-tail)/num + 2*thick)/2;

		addRectToFile(outputfile, x, y, z, extent/2, head/2, thick/2, offsetx, offsety, offsetz);
		y += head/2 - thick/2;

		for (int i = 0; i < num; i++)
		{
			addRectToFile(outputfile, x, y, z-depth/2-thick/2, extent/2, thick/2, depth/2, offsetx, offsety, offsetz);
			y += -thick/2+wid1/2;
			addRectToFile(outputfile, x, y, z-depth-thick, extent/2, wid1/2, thick/2, offsetx, offsety, offsetz);
			y += -thick/2+wid1/2;
			addRectToFile(outputfile, x, y, z-depth/2-thick/2, extent/2, thick/2, depth/2, offsetx, offsety, offsetz);
			y += -thick/2+wid2/2;
			addRectToFile(outputfile, x, y, z, extent/2, wid2/2, thick/2, offsetx, offsety, offsetz);
			y += -thick/2+wid2/2;
		}
		y += tail/2+thick/2;
		// 总长度: head + num*(wid1+wid2-2*thick) +tail = scale
		addRectToFile(outputfile, x, y, z, extent/2, tail/2, thick/2, offsetx, offsety, offsetz);
		break;
	}

}

/**
 * 生成一个楼梯
 * @param outputfile 输出文件名
 * @param offsetx x方向偏移
 * @param offsety y方向偏移
 * @param offsetz z方向偏移
 * @param rotate 旋转方向
 * @param base_z 基础高度
 * @param deltaH 楼梯级高
 * @param num 楼梯的级数
 */
void addStairToFile(const char* outputfile, double offsetx, double offsety, double offsetz,
	int rotate, double base_z, double deltaH, int num)
{
	double a, b, c, x, y, z;

	fstream f;
	f.open(outputfile, ios::out|ios::app);

	switch(rotate) {
		case 0:
			a = scale/num/2;
			b = scale/2;
			c = base_z/2;
			x = -scale/2+a;
			y = 0;
			z = 0;
			for (int i = 0; i < num; i++) {
				addRectToFile(outputfile, x, y, z, a, b, c, offsetx, offsety, offsetz);
				z += deltaH/2;
				c += deltaH/2;
				x += a*2;
			}
			break;
		case 1:
			a = scale/2;
			b = scale/num/2;
			c = base_z/2;
			x = 0;
			y = -scale/2+b;
			z = 0;
			for (int i = 0; i < num; i++) {
			addRectToFile(outputfile, x, y, z, a, b, c, offsetx, offsety, offsetz);
				z += deltaH/2;
				c += deltaH/2;
				y += b*2;
			}
			break;
		case 2:
			a = scale/num/2;
			b = scale/2;
			c = base_z/2;
			x = scale/2-a;
			y = 0;
			z = 0;
			for (int i = 0; i < num; i++) {
				addRectToFile(outputfile, x, y, z, a, b, c, offsetx, offsety, offsetz);
				z += deltaH/2;
				c += deltaH/2;
				x -= a*2;
			}
			break;
		case 3:
			a = scale/2;
			b = scale/num/2;
			c = base_z/2;
			x = 0;
			y = scale/2-b;
			z = 0;
			for (int i = 0; i < num; i++) {
				addRectToFile(outputfile, x, y, z, a, b, c, offsetx, offsety, offsetz);
				z += deltaH/2;
				c += deltaH/2;
				y -= b*2;
			}
			break;
	}


	f.close();
}

int addStand(int i, int j, bool flag, double iz, double idz)
{
	double dx = i*scale;
	double dy = j*scale;
	double dz = iz;

	double w = scale*0.5;
	double h = scale*0.5;
	double a = scale*0.04;
	double z = idz;

	addRectRing(w, h, a, z, dx, dy, dz);
	do {
		w -= 2 * a;
		if (w <= 0)
			break;

		h -= 2 * a;
		if (h <= 0)
			break;

		if (flag)
			dz -= 2 * z;
		else
			dz += 2*z;

		if (false == addRectRing(w, h, a, z, dx, dy, dz))
			break;

	} while (1);

	return 0;
}

int addStandToFile(const char* outputfile, int i, int j, bool flag, double iz, double idz)
{
	double dx = i*scale;
	double dy = j*scale;
	double dz = iz;

	double w = scale*0.5;
	double h = scale*0.5;
	double a = scale*0.04;
	double z = idz;

	addRectRingToFile(outputfile, w, h, a, z, dx, dy, dz);
	do {
		w -= 2 * a;
		if (w <= 0)
			break;

		h -= 2 * a;
		if (h <= 0)
			break;

		if (flag)
			dz -= 2 * z;
		else
			dz += 2*z;

		if (false == addRectRingToFile(outputfile, w, h, a, z, dx, dy, dz))
			break;

	} while (1);

	return 0;
}

void addContentToFile(const char* outputfile, string content)
{
	fstream f;
	f.open(outputfile, ios::out|ios::app);
	f << content;
	f.close();
}

void genHeightField(const char* filename, int rows, int cols) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::normal_distribution<float> dist(0.0f, 1.0f);

    std::ofstream file(filename);
    if (!file.is_open()) {
        std::cerr << "无法打开文件: " << filename << std::endl;
        return;
    }

    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            float height = dist(gen);
            file << height << " ";
        }
        file << "\n";
    }

    file.close();
    std::cout << "高场数据已生成并保存到: " << filename << std::endl;
}

/**
 * 生成一个二维高度场数据，符合正态分布
 * @param filename 保存的文件名
 * @param radius 高度场的半径细分程度
 * @param stddevX X方向的标准差
 * @param stddevY Y方向的标准差
 * @param meanX X方向的均值
 * @param meanY Y方向的均值
 */

void genNDHeightField(string filename, int radius, float stddevX, float stddevY, float meanX=0, float meanY=0)
{
	std::ofstream file(filename, std::ios::binary);
	if (!file.is_open()) {
		std::cerr << "无法打开文件: " << filename << std::endl;
		return;
	}
    int rows = 2 * radius + 1;
    int cols = 2 * radius + 1;
    file.write(reinterpret_cast<const char*>(&rows), sizeof(rows));
    file.write(reinterpret_cast<const char*>(&cols), sizeof(cols));
	std::vector<float> height_data;
	for(int i=-radius; i<=radius; i++) {
		for(int j=-radius; j<=radius; j++) {
			float height = 1.0/2/stddevX/stddevY/M_PI * std::exp(-1.0/2*((i-meanX)*(i-meanX)/stddevX/stddevX+(j-meanY)*(j-meanY)/stddevY/stddevY));
			height_data.push_back(height);
		}
	}
	file.write(reinterpret_cast<const char*>(height_data.data()), height_data.size() * sizeof(float));

	file.close();
	std::cout << "高度场数据已生成并保存到: " << filename << std::endl;
}

void addHfieldAssetToFile(string filename, string hfieldname,int index, double radius_x, double radius_y, double elevation_z, double base_z)
{
	fstream f;
	f.open(filename, ios::out|ios::app);
	f << "    <hfield file=\"" << hfieldname << "\" name=\"heightfield_" << index << "\"  size=\"" << radius_x << " " << radius_y << " " << elevation_z << " " << base_z << "\"/>\n";
}

void addHeightFieldToFile(string filename, int i, int j, string hfieldname, int index)
{
	// <geom hfield="heightfield" pos="0 0 0" rgba="0.8 0.9 0.8 1" type="hfield"/>
	fstream f;
	f.open(filename, ios::out|ios::app);
	f << "    <geom hfield=\"heightfield_" << index << "\" pos=\"" << i*scale << " " << j*scale << " -1.475\" type=\"hfield\"/>\n";
}

int main2()
{
	addStand(0, 0, -1, -1.5, 0.05);
	return 0;
}


int main1()
{
	//buildStair(0, 0, 0, 0.5, 5, 0.1, -0.25, 20);
	buildGutter(0, 0, 0, 4, 2, 5, 0.05, 0.1, 0.5, 0.3, 4);
	return 0;
}


int main()
{
	// 创建一个随机数生成器
	std::random_device rd;
	std::mt19937 gen(rd());

	// 定义一个范围在0到360之间的均匀分布
	std::uniform_real_distribution<> dis(0, 360);
	int idx = 0;

	// 地形种类
	vector<int> type;	//0: stand, 1: stair, 2: gutter, 3: pebble, 4: heightfield
	int cnt_hfield = 0;
	int cnt = 0;
	string hfield_name ="";

	for (int i = -N; i <= N; i++) {
		for (int j = -M; j <= M; j++) {
			type.push_back(rand() % 5);
		}
	}
	
	double height;
	setFileToFile("head1.txt", "testout.xml");
	for (auto t : type) {
		if (t == 4) {
			hfield_name = "./hfield/heightfield_"+to_string(cnt_hfield)+".bin";
			//随机生成1.0~2.0之间的高度
			height = 1.0 + (rand() % 101) * 0.01;
			addHfieldAssetToFile("testout.xml", hfield_name, cnt_hfield, scale/2, scale/2, height, 0.1f);
			genNDHeightField(hfield_name, 100, 50.0f, 50.0f, 0.0f, 0.0f);
			cnt_hfield++;
		}
	}
	addFileToFile("head2.txt", "testout.xml");

	cnt_hfield = 0;
	double angle;
	int stair_rotate, stair_num, gutter_rotate, gutter_num;
	double stair_deltaH, gutter_head, gutter_tail, gutter_depth;
	// addHead("head.txt");
#if 1
	for (int i = -N; i <= N; i++) {
		for (int j = -M; j <= M; j++) {
			switch (type[cnt]) {
				case 0:	//stand
					// 生成一个随机角度
					if(i == 0 && j == 0)
						continue;
					angle =dis(gen);
					cout << "angle: " << angle << endl;
					// addStand(i, j, angle > 180, -1.5, 0.05);
					// printf("\n");
					addStandToFile("testout.xml", i, j, angle > 180, -1.5, 0.05);
					addContentToFile("testout.xml", "\n");
					break;
				case 1:	//stair
					// 生成随机数，方向0~3，层高0.03~0.06，级数10~20
					stair_rotate = rand() % 4;
					stair_deltaH = 0.03 + (rand() % 4) * 0.01;
					stair_num = 10 + rand() % 11;
					addStairToFile("testout.xml", i*scale, j*scale, -1.475, stair_rotate, 0.04, stair_deltaH, stair_num);
					addContentToFile("testout.xml", "\n");
					break;
				case 2:	//gutter
					// 生成随机数，方向0~1，头尾0.1~0.5，深度0.1~0.2，数量6~12
					gutter_head = 0.1 + (rand() % 4) * 0.1;
					gutter_tail = 0.1 + (rand() % 4) * 0.1;
					gutter_num = 6 + rand() % 7;
					gutter_depth = 0.1 + (rand() % 2) * 0.1;
					gutter_rotate = rand() % 2;
					addGutterToFile("testout.xml", i*scale, j*scale, -1.475, gutter_head, gutter_tail, scale, 0.02, gutter_depth, gutter_rotate, 8);
					break;
				case 3:	//pebble
					break;
				case 4:	//heightfield
					addHeightFieldToFile("testout.xml", i, j, hfield_name, cnt_hfield);
					addContentToFile("testout.xml", "\n");
					cnt_hfield++;
					break;

			}
			cnt++;
		}
	}
#endif

	idx = 0;
	for (int i = -N; i <= N; i++) {
		for (int j = -M; j <= M; j++) {
			// 生成一个随机角度
			double angle = dis(gen);
			double tx = (dis(gen)- 180)/180.0*scale*0.1;
			double ty = (dis(gen) - 180) / 180.0 * scale * 0.1;
			// addRobot("robot.txt", i, j, tx, ty, angle, idx++);
			// printf("\n");
			addRobotToFile("robot.txt", "testout.xml", i, j, tx, ty, angle, idx++);
			addContentToFile("testout.xml", "\n");

		}
	}

	// printf("  </worldbody>\n");
	addContentToFile("testout.xml", "  </worldbody>\n");

	idx=0;
	for (int i = -N; i <= N; i++) {
		for (int j = -M; j <= M; j++) {
			// addActuator("actuator.txt", idx++);
			addActuatorToFile("actuator.txt", "testout.xml", idx++);
		}
	}

	// printf("</mujoco>\n\n");
	addContentToFile("testout.xml", "</mujoco>\n\n");
	return 0;
}
