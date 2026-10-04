import unreal as u
import os
import json

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
actor_subsystem = u.get_editor_subsystem(u.EditorActorSubsystem)
world = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
u.EditorLevelLibrary.set_level_viewport_camera_info(u.Vector(6200,-9600,4800),u.Rotator(pitch=-19,yaw=120,roll=0))
report = {'world':world.get_name(), 'checks':{}}
for name in ['BP_ThirdPersonCharacter','BP_ThirdPersonGameMode','BP_ThirdPersonPlayerController']:
    bp=u.load_asset('/Game/ThirdPerson/Blueprints/'+name)
    if bp:
        u.BlueprintEditorLibrary.compile_blueprint(bp)
    report['checks'][name] = bool(bp)
dragon=u.load_asset('/Game/Jangan/Meshes/SM_GoldenDragon')
report['checks']['dragon_mesh']=bool(dragon)
report['dragon_bounds']=str(dragon.get_bounds()) if dragon else ''
if dragon:
    bounds=dragon.get_bounds()
    report['checks']['dragon_upright']=bounds.box_extent.z>700 and bounds.origin.z>700
roof=u.load_asset('/Game/Jangan/Meshes/SM_CurvedHipRoof')
if roof:
    bounds=roof.get_bounds()
    report['checks']['roof_upright']=bounds.origin.z>=0 and bounds.box_extent.z<30
report['actors']=len(actor_subsystem.get_all_level_actors())
report['landmarks']={}
for actor in actor_subsystem.get_all_level_actors():
    if isinstance(actor,u.SkyLight): actor.light_component.recapture_sky()
    if actor.get_actor_label() in ['City_ground','GOLDEN_DRAGON','PlayerStart_SouthGate','DAMING_MAIN_HALL_foundation']:
        p=actor.get_actor_location()
        report['landmarks'][actor.get_actor_label()]={'x':p.x,'y':p.y,'z':p.z}
with open(os.path.join(root,'validation_report.json'),'w') as f:
    json.dump(report,f,indent=2)
u.log('JANGAN_INSPECT '+str(report))
