# play_go1_keyboard.py

from etils import epath
import mujoco
import mujoco.viewer as viewer
import glfw                  # use PyGLFW for key constants
import numpy as np
import onnxruntime as rt
import time

from mujoco_playground._src.locomotion.go1 import go1_constants
from mujoco_playground._src.locomotion.go1.base import get_assets

# — Global toggle state dict —
_key_state = {}

# play_go1_keyboard.py （只展示改动部分）

import glfw   # PyGLFW

# —— 全局键位状态 —— 
_key_state = {}

def on_key(keycode: int):
    """Passive viewer callback: toggle那几把键"""
    if keycode in (
        glfw.KEY_UP,    # 前
        glfw.KEY_DOWN,  # 后
        glfw.KEY_LEFT,  # 左平移
        glfw.KEY_RIGHT, # 右平移
        glfw.KEY_Q,     # 左转
        glfw.KEY_E,     # 右转
    ):
        _key_state[keycode] = not _key_state.get(keycode, False)

class KeyboardJoystick:
    """用↑↓←→做速度，用 Q/E 做转向"""
    def __init__(self, vx_scale=1.5, vy_scale=0.8, wz_scale=2*np.pi):
        self.vx_scale  = vx_scale
        self.vy_scale  = vy_scale
        self.wz_scale  = wz_scale

    def get_command(self) -> np.ndarray:
        # ↑↓ 前后
        fx   = (_key_state.get(glfw.KEY_UP, False)
               - _key_state.get(glfw.KEY_DOWN, False)) * self.vx_scale
        # ←→ 侧移
        fy   = (_key_state.get(glfw.KEY_RIGHT, False)
               - _key_state.get(glfw.KEY_LEFT, False)) * self.vy_scale
        # Q/E 左右转
        frot = (_key_state.get(glfw.KEY_E, False)
               - _key_state.get(glfw.KEY_Q, False)) * self.wz_scale
        return np.array([fx, fy, frot], dtype=np.float32)

class OnnxController:
    """Inject keyboard command into GO-1 policy observation."""
    def __init__(
        self,
        policy_path: str,
        default_angles: np.ndarray,
        n_substeps: int,
        action_scale: float = 0.5,
        vx_scale: float = 1.5,
        vy_scale: float = 0.8,
        wz_scale: float = 2*np.pi,
    ):
        self._policy = rt.InferenceSession(policy_path, providers=["CPUExecutionProvider"])
        self._output_names = ["continuous_actions"]
        self._action_scale = action_scale
        self._default_angles = default_angles
        self._last_action = np.zeros_like(default_angles, dtype=np.float32)
        self._n_substeps = n_substeps
        self._counter = 0
        self._joystick = KeyboardJoystick(vx_scale, vy_scale, wz_scale)

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
    # — Load MJCF & data —
    model = mujoco.MjModel.from_xml_path(
        go1_constants.FEET_ONLY_ROUGH_TERRAIN_XML.as_posix(),
        assets=get_assets(),
    )
    data = mujoco.MjData(model)
    mujoco.mj_resetDataKeyframe(model, data, 0)

    # — Timestep setup —
    ctrl_dt = 0.02
    sim_dt  = 0.004
    model.opt.timestep = sim_dt
    n_substeps = int(round(ctrl_dt / sim_dt))

    # — Controller init —
    policy_path = epath.Path(__file__).parent / "onnx/go1_policy.onnx"
    controller = OnnxController(
        policy_path=policy_path.as_posix(),
        default_angles=np.array(model.keyframe("home").qpos[7:]),
        n_substeps=n_substeps,
    )
    mujoco.set_mjcb_control(controller.get_control)

    # — Launch passive viewer with our on_key callback —
    handle = viewer.launch_passive(
        model, data,
        key_callback=on_key,        # only passes keycode:int :contentReference[oaicite:4]{index=4}
        show_left_ui=True,
        show_right_ui=True,
    )

    # — Main loop: step physics & sync display —
    while handle.is_running():
        mujoco.mj_step(model, data)
        handle.sync()
        time.sleep(model.opt.timestep)

    glfw.terminate()

if __name__ == "__main__":
    main()
