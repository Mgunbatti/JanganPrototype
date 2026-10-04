import unreal as u
import os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
world = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
name = world.get_name()
u.EditorAssetLibrary.save_directory('/Game/Jangan',only_if_is_dirty=True,recursive=True)
u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()
os.makedirs(os.path.join(root,'Previews'),exist_ok=True)
u.AutomationLibrary.take_high_res_screenshot(1280,720,os.path.join(root,'Previews',name+'.png'))
u.log('JANGAN_SCREENSHOT_REQUESTED '+name)
