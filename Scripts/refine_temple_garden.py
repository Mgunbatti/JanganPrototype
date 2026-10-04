"""Open temple garden with an organic pond and walkable timber bridge."""
import unreal as u, os, math, json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
source=open(os.path.join(ROOT,'Scripts','build_temple.py'),encoding='utf-8').read()
exec(compile(source.split('L.save_current_level();report=[]')[0],__file__,'exec'))
M['earth']=u.load_asset('/Game/Jangan/Materials/M_Earth')
def pond_mesh(name,ring=False):
    asset='/Game/Jangan/Meshes/'+name
    existing=u.load_asset(asset)
    if existing:return existing
    pts=[]
    for i in range(64):
        t=i*math.tau/64;r=1+.12*math.sin(3*t)+.07*math.cos(5*t)
        pts.append((900*r*math.cos(t),1900*r*math.sin(t)))
    vertices=[(0,0,0)]+[(x,y,0) for x,y in pts]
    faces=[(1,i+2,(i+1)%64+2) for i in range(64)]
    if ring:
        vertices=[(x,y,0) for x,y in pts]+[(x*1.14,y*1.075,0) for x,y in pts]
        faces=[]
        for i in range(64):
            j=(i+1)%64;faces.extend([(i+1,j+1,j+65),(i+1,j+65,i+65)])
    filename=os.path.join(ROOT,'SourceAssets',name+'.obj')
    with open(filename,'w') as f:
        f.write('o '+name+'\n')
        for x,y,z in vertices:f.write('v %f %f %f\n'%(x,-y,z))
        for face in faces:f.write('f '+' '.join(str(i) for i in face)+'\n')
    task=u.AssetImportTask();task.filename=filename;task.destination_path='/Game/Jangan/Meshes';task.destination_name=name;task.automated=True;task.save=True
    opt=u.FbxImportUI();opt.import_materials=False;opt.import_textures=False;opt.static_mesh_import_data.set_editor_property('auto_generate_collision',False);task.options=opt
    u.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task]);result=u.load_asset(asset);assert result
    return result
meshes['Pond']=pond_mesh('SM_TempleOrganicPond')
meshes['Shore']=pond_mesh('SM_TempleOrganicShore',True)
L.save_current_level();reports=[]
for day in ['Night','Day']:
    path='/Game/Jangan/Maps/Jangan_'+day;assert L.load_level(path)
    current=list(A.get_all_level_actors())
    if any(a.get_actor_label()=='Temple_Organic_water' for a in current):continue
    backup='/Game/Jangan/Backups/Jangan_'+day+'_BeforeOrganicGarden'
    if not u.EditorAssetLibrary.does_asset_exist(backup):assert u.EditorAssetLibrary.duplicate_asset(path,backup)
    removed=[]
    for a in current:
        n=a.get_actor_label()
        if n.startswith(('Temple_Prayer_hall','Temple_Lotus_pool','Temple_Lotus_leaf','Temple_Lotus_flower')):
            removed.append(n);A.destroy_actor(a)
    shape('Organic_water','Pond',-10300,6650,49,100,100,100,'water')
    shape('Organic_shore','Shore',-10300,6650,52,100,100,100,'earth')
    # A stepped arch bridge crosses the narrow center of the pond.
    for i in range(27):
        x=-11600+i*100;z=65+min(i,26-i,8)*14
        box('Bridge_plank_%02d'%i,x,6650,z,102,620,24,'wood')
        for side in [-1,1]:
            if i%3==0:
                box('Bridge_post',x,6650+side*290,z+160,30,30,320,'wood')
            box('Bridge_rail',x,6650+side*290,z+280,105,28,28,'wood',False)
    for i in range(24):
        t=i*math.tau/24;r=1+.12*math.sin(3*t)+.07*math.cos(5*t)
        x=-10300+960*r*math.cos(t);y=6650+1990*r*math.sin(t)
        if abs(y-6650)<450:continue
        shape('Shore_rock','Sphere',x,y,77,100+(i%3)*35,85+(i%4)*20,70,'stone')
        if i%3==0:
            for dx in [-30,0,30]:shape('Shore_reed','Cone',x+dx,y+40,145,22,22,180,'roof')
    for dx,dy in [(-350,-1000),(300,-700),(-150,1000),(240,1300)]:
        shape('Lotus_leaf','Cylinder',-10300+dx,6650+dy,58,190,190,8,'roof')
        shape('Lotus_flower','Sphere',-10300+dx,6650+dy,79,85,85,45,'pink')
    world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
    floor=u.SystemLibrary.line_trace_single(world,V(-10300,6650,600),V(-10300,6650,0),u.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[],u.DrawDebugTrace.NONE,True)
    assert floor is not None,'Bridge has no collision'
    assert L.save_current_level();reports.append({'map':day,'removed':removed,'bridge_collision':True,'backup':backup})
u.EditorAssetLibrary.save_directory('/Game/Jangan',True,True)
with open(os.path.join(ROOT,'temple_garden_report.json'),'w',encoding='utf-8') as f:json.dump(reports,f,indent=2)
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(V(-18000,-2500,7000),u.Rotator(pitch=-27,yaw=48,roll=0))
u.log('ORGANIC_GARDEN_SAVED')
