'''
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

bl_info = {
    "name": "Set UV Layer On All Selected Objects",
    "author": "tryptech, brockmann",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Object Data > UV Maps",
    "description": "Set UV Layer On All Selected Objects",
    "category": "Object",
    }

import bpy

__bl_classes = []

class OBJECT_OT_set_active_uv(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.set_active_uv_selection"
    bl_label = "Set UV Layer On All Selected Objects"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'MESH' and obj.data.uv_layers.active

    def execute(self, context):
        target_uv = context.active_object.data.uv_layers.active
        for obj in context.selected_objects:
            if obj.type == 'MESH' and obj != context.active_object:
                if target_uv.name in obj.data.uv_layers.keys():
                    # Active UV Layer = Target Layer
                    obj.data.uv_layers.active = obj.data.uv_layers[target_uv.name]
                else:
                    uv_list_size = len(obj.data.uv_layers.keys())
                    if uv_list_size < 8:
                        new_uv = obj.data.uv_layers.new(
                            name=target_uv.name, do_init=True)
                        obj.data.uv_layers.active = obj.data.uv_layers[target_uv.name]

        return {'FINISHED'}


def draw_set_active_uv(self, context):
    layout = self.layout
    layout.operator(OBJECT_OT_set_active_uv.bl_idname)


def register():
    bpy.utils.register_class(OBJECT_OT_set_active_uv)
    
    bpy.types.DATA_PT_uv_texture.append(draw_set_active_uv)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_set_active_uv)

    bpy.types.DATA_PT_uv_texture.remove(draw_set_active_uv)


if __name__ == "__main__":
    register()
