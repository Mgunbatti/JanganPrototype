"""Center pagoda, remove precinct walls, cross a wider pond along the entrance axis."""
import unreal as u,os,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
source=open(os.path.join(ROOT,'Scripts','build_temple.py'),encoding='utf-8').read()
exec(compile(source.split('L.save_current_level();report=[]')[0],__file__,'exec'))
tag=u.Name('PagodaAxisV1');reports=[];L.save_current_level()
for day in ['Night','Day']:
    path='/Game/Jangan/Maps/Jangan_'+day;assert L.load_level(path)
    current=list(A.get_all_level_actors())
    if any(tag in a.tags for a in current):continue
    backup='/Game/Jangan/Backups/Jangan_'+day+'_BeforePagodaAxis'
    if not u.EditorAssetLibrary.does_asset_exist(backup):assert u.EditorAssetLibrary.duplicate_asset(path,backup)
    removed=[]
    for a in current:
        n=a.get_actor_label();p=a.get_actor_location();s=a.get_actor_scale3d()
        if n.startswith(('Temple_Boundary','Temple_Rear_boundary','Temple_Front_boundary','Temple_Bridge')):
            removed.append(n);A.destroy_actor(a);continue
        if n.startswith('Temple_Pagoda'):
            a.set_actor_location(V(p.x-1150,p.y+200,p.z),False,False)
        elif n.startswith(('Temple_Organic','Temple_Shore','Temple_Lotus_leaf','Temple_Lotus_flower')):
            a.set_actor_location(V(-8650-(p.y-6650)*1.2,6000+(p.x+9800)*1.25,p.z),False,False)
            r=a.get_actor_rotation();a.set_actor_rotation(u.Rotator(pitch=r.pitch,yaw=r.yaw+90,roll=r.roll),False)
            if n.startswith('Temple_Organic'):a.set_actor_scale3d(V(s.x*1.25,s.y*1.2,s.z))
    # Wide timber bridge follows the centerline from gate toward tower stairs.
    for i in range(30):
        y=4000+i*100;z=65+min(i,29-i,6)*14
        a=box('Axis_bridge_plank_%02d'%i,-8650,y,z,780,102,24,'wood');a.tags=[tag]
        for side in [-1,1]:
            if i%3==0:box('Axis_bridge_post',-8650+side*365,y,z+155,30,30,310,'wood')
            box('Axis_bridge_rail',-8650+side*365,y,z+265,28,104,28,'wood',False)
    # 18cm rises connect the courtyard to the existing pagoda plinth (~278cm).
    for i in range(13):
        top=43+(i+1)*18
        box('Pagoda_stair_%02d'%i,-8650,6950+i*45,(43+top)/2,1000,55,top-43,'stone')
    world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
    samples=[]
    for y in [3500,3900,4000,4600,5200,6000,6800,6950,7200,7490]:
        hit=u.SystemLibrary.line_trace_single(world,V(-8650,y,700),V(-8650,y,-100),u.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[],u.DrawDebugTrace.NONE,True)
        assert hit is not None,'No walkable floor at '+str(y);samples.append(y)
    clear=u.SystemLibrary.line_trace_single(world,V(-8650,3450,480),V(-8650,7500,480),u.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[],u.DrawDebugTrace.NONE,True)
    assert clear is None,'Entrance axis blocked'
    assert L.save_current_level();reports.append({'map':day,'removed_count':len(removed),'pagoda_center':[-8650,8500],'pond_center':[-8650,6000],'floor_samples':samples,'axis_clear':True,'backup':backup})
u.EditorAssetLibrary.save_directory('/Game/Jangan',True,True)
with open(os.path.join(ROOT,'pagoda_axis_report.json'),'w',encoding='utf-8') as f:json.dump(reports,f,indent=2)
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(V(-8650,-1700,5400),u.Rotator(pitch=-25,yaw=90,roll=0))
u.log('PAGODA_AXIS_SAVED')
