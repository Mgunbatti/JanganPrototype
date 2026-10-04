"""Separate the monuments and create low ornamental gardens beside the palace axis."""
import unreal as u,os,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
source=open(os.path.join(ROOT,'Scripts','build_temple.py'),encoding='utf-8').read()
exec(compile(source.split('L.save_current_level();report=[]')[0],__file__,'exec'))
M['leaf']=u.load_asset('/Game/Jangan/Materials/M_JadeFoliage');M['earth']=u.load_asset('/Game/Jangan/Materials/M_Earth');M['blossom']=u.load_asset('/Game/Jangan/Materials/M_Blossom')
tag=u.Name('PalaceGardenV1')
def decor(n,mesh,x,y,z,w,d,h,m,solid=False):
    a=shape(n,mesh,x,y,z,w,d,h,m,solid);a.set_actor_label('PalaceGarden_'+n);a.set_folder_path('PalaceGardens');a.tags=[tag];return a
def tree(x,y,pink=False,scale=1):
    decor('Tree_trunk','Cylinder',x,y,43+210*scale,40*scale,40*scale,420*scale,'wood',True)
    for dx,dy,z,w in [(-100,-60,490,350),(110,30,530,400),(0,100,650,300)]:
        decor('Tree_crown','Sphere',x+dx*scale,y+dy*scale,43+z*scale,w*scale,w*.85*scale,w*.7*scale,'blossom' if pink else 'leaf')
def lantern(x,y):
    decor('Lantern_post','Cylinder',x,y,200,24,24,314,'wood',True)
    decor('Lantern_glow','Cylinder',x,y,390,70,70,80,'lamp')
    decor('Lantern_cap','Roof',x,y,438,120,120,35,'roof')
glow=u.load_asset('/Game/Jangan/Materials/M_LegendsMysticGlow')
# Replace the emissive connection explicitly, as expression enumeration varies across UE versions.
e=u.MaterialEditingLibrary.create_material_expression(glow,u.MaterialExpressionConstant3Vector,-320,0)
e.set_editor_property('constant',u.LinearColor(.045,.38,.55,1));u.MaterialEditingLibrary.connect_material_property(e,'',u.MaterialProperty.MP_EMISSIVE_COLOR);u.MaterialEditingLibrary.recompile_material(glow);u.EditorAssetLibrary.save_loaded_asset(glow)
L.save_current_level();reports=[]
for day in ['Night','Day']:
    path='/Game/Jangan/Maps/Jangan_'+day;assert L.load_level(path)
    current=list(A.get_all_level_actors())
    if any(tag in a.tags for a in current):continue
    backup='/Game/Jangan/Backups/Jangan_'+day+'_BeforePalaceGardens'
    if not u.EditorAssetLibrary.does_asset_exist(backup):assert u.EditorAssetLibrary.duplicate_asset(path,backup)
    moved=0
    for a in current:
        n=a.get_actor_label();p=a.get_actor_location();s=a.get_actor_scale3d()
        if n.startswith(('Legends_Buddha','Legends_Lotus','Legends_Incense','Legends_Mystic','Legends_Energy')):
            a.set_actor_location(V(-6600+(p.x+2350)*.75,8200+(p.y-2100)*.75,43+(p.z-43)*.75),False,False)
            a.set_actor_scale3d(V(s.x*.75,s.y*.75,s.z*.75));moved+=1
        elif n in ['NPC_LegendsGate','NPC_Name_LegendsGate']:
            a.set_actor_location(V(-6600,7250,p.z),False,False)
        elif n=='Shop_Sign_LegendsGate':a.set_actor_location(V(-6600,7600,400),False,False)
    for side in [-1,1]:
        x=side*4700;y=3900
        decor('Garden_plinth','Cube',x,y,65,1900,1500,44,'stone',True)
        decor('Garden_soil','Cube',x,y,90,1770,1370,8,'earth')
        for dx,dy,pink,sc in [(-520,180,True,.95),(490,230,False,1.05)]:tree(x+dx,y+dy,pink,sc)
        for dx,dy in [(-650,-380),(-250,-420),(250,-420),(650,-380)]:
            decor('Shrub','Sphere',x+dx,y+dy,150,260,200,140,'leaf')
            decor('Flower_cluster','Sphere',x+dx,y+dy,215,130,110,65,'blossom')
        for dx in [-540,540]:
            decor('Bench_seat','Cube',x+dx,y-1050,125,500,145,45,'wood',True)
            for leg in [-180,180]:decor('Bench_leg','Cube',x+dx+leg,y-1050,80,45,120,75,'wood',True)
        for dx in [-1000,1000]:lantern(x+dx,y-750)
        for dx,dy in [(-700,600),(500,630)]:decor('Garden_rock','Sphere',x+dx,y+dy,140,220,150,130,'stone')
    # Low planting around the new teleport alcove, away from the pagoda axis.
    for x,y in [(-6050,8750),(-7050,9150)]:tree(x,y,True,.7)
    for x in [-7100,-6100]:lantern(x,7450)
    world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
    axis=u.SystemLibrary.line_trace_single(world,V(0,4300,200),V(0,6200,200),u.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[],u.DrawDebugTrace.NONE,True)
    assert axis is None,'Palace approach blocked'
    assert L.save_current_level();reports.append({'map':day,'moved_monument_parts':moved,'buddha_scale':.75,'buddha_center':[-6600,8200],'palace_approach_clear':True,'backup':backup})
u.EditorAssetLibrary.save_directory('/Game/Jangan',True,True)
with open(os.path.join(ROOT,'palace_garden_report.json'),'w',encoding='utf-8') as f:json.dump(reports,f,indent=2)
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(V(0,-11500,11000),u.Rotator(pitch=-36,yaw=90,roll=0))
u.log('PALACE_GARDENS_SAVED')
