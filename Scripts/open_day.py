import unreal as u
u.get_editor_subsystem(u.LevelEditorSubsystem).load_level('/Game/Jangan/Maps/Jangan_Day')
u.EditorLevelLibrary.set_level_viewport_camera_info(u.Vector(6200,-9600,4800),u.Rotator(pitch=-19,yaw=120,roll=0))
