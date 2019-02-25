bl_info = {
	"name": "Discord Rich Presence",
	"description": "Adds Rich Presence support to Blender",
	"author": "@AlexApps#9295, @lvxejay#9771, @Ryan()#5875",
	"version": (1, 0),
	"blender": (2, 79, 0),
	"location": "",
	"wiki_url": "https://github.com/AlexApps99/blender-rich-presence/wiki",
	"tracker_url": "https://github.com/AlexApps99/blender-rich-presence/issues",
	"support": "COMMUNITY",
	"category": "System"
	}
import rpc
import time
import bpy
import threading

client_id = '434079082339106827'
rpc_obj = rpc.DiscordIpcClient.for_platform(client_id)
time.sleep(5)
start_time = time.time()
version_no = bpy.app.version_string.split(' (sub 0)')[0]

class presencePanel(bpy.types.Panel):
	"""Creates a Panel in the Object properties window"""
	bl_label = "Discord Rich Presence"
	bl_idname = "OBJECT_PT_hello"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.operator("wm.update_presence")

class presenceOperator(bpy.types.Operator):
	bl_idname = "wm.update_presence"
	bl_label = "Update Discord Presence"
	def execute(self, context):
		print(bpy.path.basename(bpy.context.blend_data.filepath))
		print(bpy.path.basename(bpy.context.blend_data.filepath).split(' (sub 0)'))
		activity = {
			"details": "Using Blender " + version_no,
			"state": bpy.path.basename(bpy.context.blend_data.filepath) + " | Poly Count: " + str(getPolyCount()),

			"timestamps": {
				"start": start_time
			},
			"assets": {
				"small_text": "Blender",
				"small_image": "blender_logo",
				"large_text": version_no,
				"large_image": "blender_logo"
			}
		}
		rpc_obj.set_activity(activity)
		return {'FINISHED'}

def getPolyCount():
	polyCount = 0
	for obj in bpy.context.scene.objects:
		if obj.type == 'MESH':
			mesh = obj.data
			polyCount += len(mesh.polygons)
	return polyCount

bpy.utils.register_class(presenceOperator)
bpy.utils.register_class(presencePanel)

def register():
	bpy.utils.register_module(__name__)
