import unreal as u, os
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
u.AutomationLibrary.take_high_res_screenshot(1280,720,os.path.join(root,'Previews','Jangan_Temple_Layout.png'))
