import genesis as gs

gs.init(
    seed = None,
    backend = gs.gpu,
    debug = False,
    eps = 1e-12,

    )

scene = gs.Scene(
    sim_options=gs.options.SimOptions(
        dt=4e-3,
        # gravity=(0, 0, -10.0),
        substeps=10,
    ),
    show_viewer=True,
    # viewer_options=gs.options.ViewerOptions(
    #     camera_pos=(3.5, 0.0, 2.5),
    #     camera_lookat=(0.0, 0.0, 0.5),
    #     camera_fov=40,
    # ),
    mpm_options=gs.options.MPMOptions(
        lower_bound=(-1.0, -1.0, -0.01),
        upper_bound=(1.0, 1.0, 2.0),
        grid_density=64,
        enable_CPIC=True,
    ),
    vis_options=gs.options.VisOptions(
        visualize_mpm_boundary=True,
    ),
)

plane = scene.add_entity(
    material=gs.materials.Rigid(),
    morph=gs.morphs.URDF(file="urdf/plane/plane.urdf", fixed=True),
)

# box = scene.add_entity(
#     material=gs.materials.MPM.Elastic(sampler="pbs-64"),
#     morph=gs.morphs.Box(
#         size=(0.1, 0.1, 0.1),
#         pos=(0, 0, 0.1),
#     ),
# )

# mountain = scene.add_entity(
#     gs.morphs.Mesh(
#         file = './model/mesh/Monte_Cervino.stl',
#         scale = 0.02,
#         pos = (0, 0, 0),
#         convexify = False,
#         decompose_nonconvex = True,
#         visualization = True,
#         collision = True,
#         requires_jac_and_IK = True,
#         fixed = True,
#         merge_submeshes_for_collision = True,
        
#     )    
# )

mountain = scene.add_entity(
    material=gs.materials.Rigid(),
    morph=gs.morphs.Mesh(
        # file="./terrain/mesh/Monte_Cervino.stl",
        file="./terrain/mesh/Trench_90_Deg._Turn_V1.stl",
        scale=0.02,
        pos=(-0.6, 0.0, 0.1), 
        euler=(0, 0, 0),
        convexify = False,
        decompose_nonconvex = True,
        fixed = True,
        collision = True,
    ),
)

dragon = scene.add_entity(
    material=gs.materials.MPM.Elastic(sampler="pbs-64"),
    morph=gs.morphs.Mesh(
        file="meshes/dragon/dragon.obj",
        scale=0.007,
        euler=(0, 0, 90),
        pos=(0.3, -0.0, 1.7),
    ),
    surface=gs.surfaces.Rough(
        color=(0.6, 1.0, 0.8, 1.0),
        vis_mode="particle",
    ),
)

scene.build()

for i in range(10000):
    scene.step()