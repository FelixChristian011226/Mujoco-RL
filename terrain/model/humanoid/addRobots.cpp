// addRobots.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//
#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <string>
#include <random>

const int N = 5;
const int M = 5;
float scale = 4.0;

void addHead(const char* filename) {
	FILE* file = fopen(filename, "rt");
	char line[1024];

	while (fgets(line, 1024, file)) {
		printf("%s", line);
	}

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

void addRect(double x, double y, double z, double a, double b, double c, double dx, double dy, double dz)
{
	printf("    <geom type=\"box\" pos=\"%lf %lf %lf\" size=\"%lf %lf %lf\" rgba=\"0.5 0.5 0.5 1\" />\n",
		x+dx, y+dy, z+dz, a, b, c);
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

int main()
{
	// 创建一个随机数生成器
	std::random_device rd;
	std::mt19937 gen(rd());

	// 定义一个范围在0到360之间的均匀分布
	std::uniform_real_distribution<> dis(0, 360);
	int idx = 0;

	addHead("head.txt");
#if 1
	for (int i = -N; i <= N; i++) {
		for (int j = -M; j <= M; j++) {
			// 生成一个随机角度
			double angle =dis(gen);
			addStand(i, j, angle > 180, -1.5, 0.05);
			printf("\n");
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
			addRobot("robot.txt", i, j, tx, ty, angle, idx++);
			printf("\n");

		}
	}

	printf("  </worldbody>\n");

	idx=0;
	for (int i = -N; i <= N; i++) {
		for (int j = -M; j <= M; j++) {
			addActuator("actuator.txt", idx++);
		}
	}

	printf("</mujoco>\n\n");
	return 0;
}
