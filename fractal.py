import bpy

from .lsystem.lsystem_parse import parse as lparse
import os
from .fractal_gen import FractalGen


def _create_fractal(self, context):
    x = None
    if self.grammar_path == "":
        return
    try:
        with open(self.grammar_path) as f:
            x = lparse(f.read())
    except FileNotFoundError:
        self.grammar_path = ""
        return

    max_count = x.approx_steps(level)
    bpy.context.window_manager.progress_begin(0, 99)
    tick_count = max(max_count // 100, 1)
    ticks = 0
    count = 0
    print("Expected ticks: " + str(max_count))

    FractalGen(x).draw_vertices(self.iteration)

    count += 1
    if count > tick_count:
        ticks += count // tick_count
        count = count % tick_count
        bpy.context.window_manager.progress_update(ticks)

    bpy.context.window_manager.progress_end()
    print("Needed ticks: " + str(ticks * tick_count + count))
    with Timer("Node apply", True):
        profile_mesh = bpy.data.meshes.new("FractalMesh")
        profile_mesh.from_pydata(self.verts, self.edges, [])
        profile_mesh.update()

        profile_object = bpy.data.objects.new("Fractal", profile_mesh)
        profile_object.data = profile_mesh

        scene = bpy.context.scene
        scene.objects.link(profile_object)
        profile_object.select = True

    CommandTimer.get_timings()


class Fractal_add_object(bpy.types.Operator):
    """Create a new Fractal"""
    bl_idname = "mesh.add_fractal"
    bl_label = "Add Fracal"
    bl_options = {'REGISTER', 'UNDO'}

    iteration = bpy.props.IntProperty(
        name="Iteration Count",
        default=2,
        min=1,
        soft_min=1,
        soft_max=7,
        subtype='UNSIGNED',
        description="Number of iterations of the fractal")

    def reset_iteration(self, context):
        self.iteration = 2
    grammar_path = bpy.props.StringProperty(
        name="Grammar path",
        default=os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             "examples", "sierpinski.txt"),
        description="The grammar for the fractal you want to draw",
        subtype='FILE_PATH',
        update=reset_iteration
    )

    def execute(self, context):

        _create_fractal(self, context)

        return {'FINISHED'}
