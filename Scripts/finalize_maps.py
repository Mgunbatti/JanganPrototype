import unreal as u
import os

root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
level=u.get_editor_subsystem(u.LevelEditorSubsystem)
actors=u.get_editor_subsystem(u.EditorActorSubsystem)
for name in ['Day','Night']:
    level.load_level('/Game/Jangan/Maps/Jangan_'+name)
    for a in actors.get_all_level_actors():
        if isinstance(a,u.SkyLight):
            a.light_component.set_editor_property('sky_distance_threshold',10000)
            a.light_component.set_editor_property('intensity',1.2 if name=='Night' else 1.6)
            a.light_component.recapture_sky()
    u.EditorLevelLibrary.set_level_viewport_camera_info(u.Vector(6200,-9600,4800),u.Rotator(pitch=-19,yaw=120,roll=0))
    if not level.save_current_level(): raise RuntimeError('Map save failed '+name)
path=os.path.join(root,'Scripts','inspect_city.py')
exec(compile(open(path,encoding='utf-8').read(),path,'exec'),{'__file__':path})
u.log('JANGAN_MAPS_FINALIZED')
