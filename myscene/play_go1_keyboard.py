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

_glfw_window = None
speed = 0.4

def on_key(key: int):
    """MuJoCo 被动 Viewer 回调：首次捕获 GLFW window"""
    global _glfw_window
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
            glfw.KEY_KP_1:     False,
            glfw.KEY_KP_3:     False,
        }

    def get_command(self) -> np.ndarray:
        # 如果还没捕获到 window，默认为未按下
        window = _glfw_window
        def raw_state(key):
            return (glfw.get_key(window, key) == glfw.PRESS) if window else False

        cmd_fx = 0.0
        up_raw   = raw_state(glfw.KEY_UP)
        down_raw = raw_state(glfw.KEY_DOWN)

        if up_raw:
            cmd_fx =  self.vx_scale
        elif down_raw:
            cmd_fx = -self.vx_scale


        cmd_fy = 0.0
        key1_raw = raw_state(glfw.KEY_KP_1)
        key3_raw = raw_state(glfw.KEY_KP_3)

        if key1_raw:
            cmd_fy =  self.vx_scale
        elif key3_raw:
            cmd_fy = -self.vx_scale

        cmd_frot = 0.0
        left_raw  = raw_state(glfw.KEY_LEFT)
        right_raw = raw_state(glfw.KEY_RIGHT)

        if left_raw:
            cmd_frot =  self.wz_scale
        elif right_raw:
            cmd_frot = -self.wz_scale

        return np.array([cmd_fx, cmd_fy, cmd_frot], dtype=np.float32)

class OnnxController:
    def __init__(
        self,
        policy_path: str,
        default_angles: np.ndarray,
        n_substeps: int,
        action_scale: float = 0.5,
        vx_scale: float = 1.5 * speed,
        wz_scale: float = 2*np.pi * speed,
        ctrl_dt: float = 0.02,
    ):
        self._policy        = rt.InferenceSession(policy_path, providers=["CPUExecutionProvider"])
        self._output_names  = ["continuous_actions"]
        self._action_scale  = action_scale
        self._default_angles= default_angles
        self._last_action   = np.zeros_like(default_angles, dtype=np.float32)
        self._n_substeps    = n_substeps
        self._counter       = 0
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
    # model = mujoco.MjModel.from_xml_path(
    #     go1_constants.FEET_ONLY_ROUGH_TERRAIN_XML.as_posix(),
    #     assets=get_assets(),
    # )
    scene_path = epath.Path(__file__).parent / "room" / "room.xml"
    model = mujoco.MjModel.from_xml_path(
        scene_path.as_posix(),
        # assets=get_assets(),
    )
    
    data = mujoco.MjData(model)
    mujoco.mj_resetDataKeyframe(model, data, 0)

    ctrl_dt    = 0.02
    sim_dt     = 0.004
    model.opt.timestep = sim_dt
    n_substeps = int(round(ctrl_dt / sim_dt))

    handle = viewer.launch_passive(
        model, data,
        key_callback=on_key,
        show_left_ui=True,
        show_right_ui=True,
    )

    policy_path = epath.Path(__file__).parent / "onnx/go1_policy.onnx"
    controller = OnnxController(
        policy_path=policy_path.as_posix(),
        default_angles=np.array(model.keyframe("home").qpos[7:]),
        n_substeps=n_substeps,
        ctrl_dt=ctrl_dt,
    )
    mujoco.set_mjcb_control(controller.get_control)

    while handle.is_running():
        mujoco.mj_step(model, data)
        handle.sync()
        time.sleep(model.opt.timestep)

    glfw.terminate()

if __name__ == "__main__":
    main()
