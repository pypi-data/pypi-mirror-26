import os
from mujoco.sim import GeomType, ObjType
if os.environ.get('EGL'):
    from mujoco.simEgl import Sim
else:
    from mujoco.simGlfw import Sim


# Public API:
__all__ = ['Sim', 'GeomType', 'ObjType']
