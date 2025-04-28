# play_go1_keyboard.py

from etils import epath
import mujoco
import mujoco.viewer as viewer
import glfw
import numpy as np
import onnxruntime as rt
import time

from mujoco_playground._src.locomotion.go1 import go1_constants
from mujoco_playground._src.locomotion.go1.base import get_assets

# —— 全局 GLFW 窗口指针 —— 
_glfw_window = None

def on_key(key: int):
    """MuJoCo 被动 Viewer 回调：首次捕获 GLFW window"""
    global _glfw_window
    # 在 UI 线程中，这将返回有效的 GLFWwindow* 
    if _glfw_window is None:
        _glfw_window = glfw.get_current_context()

class KeyboardJoystick:
    """
    直接轮询 GLFW：
      - Edge (raw==PRESS && prev_raw==False): 短按 -> 小步移动
      - Level (raw==PRESS): 长按 -> 持续移动
    """
    def __init__(self, vx_scale=1.5, wz_scale=2*np.pi, ctrl_dt=0.02):
        self.vx_scale = vx_scale
        self.wz_scale = wz_scale
        self.ctrl_dt  = ctrl_dt
        # 初始化上一帧原始状态
        self.prev_raw = {
            glfw.KEY_UP:    False,
            glfw.KEY_DOWN:  False,
            glfw.KEY_LEFT:  False,
            glfw.KEY_RIGHT: False,
        }

    def get_command(self) -> np.ndarray:
        # 如果还没捕获到 window，默认为未按下
        window = _glfw_window
        def raw_state(key):
            return (glfw.get_key(window, key) == glfw.PRESS) if window else False

        # 边沿检测：第一次按下
        cmd_fx = 0.0
        up_raw   = raw_state(glfw.KEY_UP)
        down_raw = raw_state(glfw.KEY_DOWN)
        # Edge detection
        up_edge   = up_raw   and not self.prev_raw[glfw.KEY_UP]
        down_edge = down_raw and not self.prev_raw[glfw.KEY_DOWN]
        # 更新 prev_raw
        self.prev_raw[glfw.KEY_UP]   = up_raw
        self.prev_raw[glfw.KEY_DOWN] = down_raw

        # 前后速度：短按 -> vx_scale * dt, 长按 -> vx_scale
        if up_edge:
            cmd_fx =  self.vx_scale * self.ctrl_dt
        elif up_raw:
            cmd_fx =  self.vx_scale
        elif down_edge:
            cmd_fx = -self.vx_scale * self.ctrl_dt
        elif down_raw:
            cmd_fx = -self.vx_scale

        # 原地转向
        cmd_frot = 0.0
        right_raw = raw_state(glfw.KEY_RIGHT)
        left_raw  = raw_state(glfw.KEY_LEFT)
        right_edge = right_raw and not self.prev_raw[glfw.KEY_RIGHT]
        left_edge  = left_raw  and not self.prev_raw[glfw.KEY_LEFT]
        self.prev_raw[glfw.KEY_RIGHT] = right_raw
        self.prev_raw[glfw.KEY_LEFT]  = left_raw

        if left_edge:
            cmd_frot =  self.wz_scale * self.ctrl_dt
        elif left_raw:
            cmd_frot =  self.wz_scale
        elif right_edge:
            cmd_frot = -self.wz_scale * self.ctrl_dt
        elif right_raw:
            cmd_frot = -self.wz_scale

        # 不做侧移
        return np.array([cmd_fx, 0.0, cmd_frot], dtype=np.float32)

class OnnxController:
    def __init__(
        self,
        policy_path: str,
        default_angles: np.ndarray,
        n_substeps: int,
        action_scale: float = 0.5,
        vx_scale: float = 1.5,
        wz_scale: float = 2*np.pi,
        ctrl_dt: float = 0.02,
    ):
        self._policy        = rt.InferenceSession(policy_path, providers=["CPUExecutionProvider"])
        self._output_names  = ["continuous_actions"]
        self._action_scale  = action_scale
        self._default_angles= default_angles
        self._last_action   = np.zeros_like(default_angles, dtype=np.float32)
        self._n_substeps    = n_substeps
        self._counter       = 0
        # 直接轮询的摇杆
        self._joystick      = KeyboardJoystick(vx_scale, wz_scale, ctrl_dt)

    def get_obs(self, model, data) -> np.ndarray:
        linvel   = data.sensor("local_linvel").data
        gyro     = data.sensor("gyro").data
        imu_xmat = data.site_xmat[model.site("imu").id].reshape(3,3)
        gravity  = imu_xmat.T @ np.array([0,0,-1])
        jpos     = data.qpos[7:] - self._default_angles
        jvel     = data.qvel[6:]
        cmd      = self._joystick.get_command()
        obs = np.hstack([linvel, gyro, gravity, jpos, jvel, self._last_action, cmd])
        return obs.astype(np.float32)

    def get_control(self, model: mujoco.MjModel, data: mujoco.MjData):
        self._counter += 1
        if self._counter % self._n_substeps == 0:
            obs = self.get_obs(model, data).reshape(1, -1)
            act = self._policy.run(self._output_names, {"obs": obs})[0][0]
            self._last_action = act.copy()
            data.ctrl[:] = act * self._action_scale + self._default_angles

def main():
    # 加载模型 & 数据
    model = mujoco.MjModel.from_xml_path(
        go1_constants.FEET_ONLY_ROUGH_TERRAIN_XML.as_posix(),
        assets=get_assets(),
    )
    data = mujoco.MjData(model)
    mujoco.mj_resetDataKeyframe(model, data, 0)

    # 时步设置
    ctrl_dt    = 0.02
    sim_dt     = 0.004
    model.opt.timestep = sim_dt
    n_substeps = int(round(ctrl_dt / sim_dt))

    # 启动被动 Viewer，注册 on_key 仅用来捕获 window
    handle = viewer.launch_passive(
        model, data,
        key_callback=on_key,
        show_left_ui=True,
        show_right_ui=True,
    )

    # 控制器初始化
    policy_path = epath.Path(__file__).parent / "onnx/go1_policy.onnx"
    controller = OnnxController(
        policy_path=policy_path.as_posix(),
        default_angles=np.array(model.keyframe("home").qpos[7:]),
        n_substeps=n_substeps,
        ctrl_dt=ctrl_dt,
    )
    mujoco.set_mjcb_control(controller.get_control)

    # 主循环
    while handle.is_running():
        mujoco.mj_step(model, data)
        handle.sync()
        time.sleep(model.opt.timestep)

    glfw.terminate()

if __name__ == "__main__":
    main()
