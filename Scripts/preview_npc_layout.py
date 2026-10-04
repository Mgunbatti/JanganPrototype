import unreal as u,os
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(u.Vector(0,-18500,14500),u.Rotator(pitch=-43,yaw=90,roll=0))
u.AutomationLibrary.take_high_res_screenshot(1280,720,os.path.join(root,'Previews','Jangan_NPC_Layout.png'))
