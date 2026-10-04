import unreal as u,os,math,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
source=open(os.path.join(ROOT,'Scripts','build_temple.py'),encoding='utf-8').read()
exec(compile(source.split('L.save_current_level();report=[]')[0],__file__,'exec'))
reports=[];tag=u.Name('RoofSupportV1');L.save_current_level()
for day in ['Night','Day']:
    assert L.load_level('/Game/Jangan/Maps/Jangan_'+day)
    current=list(A.get_all_level_actors());roofs=[a for a in current if isinstance(a,u.StaticMeshActor) and a.static_mesh_component.static_mesh==meshes['Roof']]
    changes=[]
    for a in current:
        n=a.get_actor_label()
        if not isinstance(a,u.StaticMeshActor) or tag in a.tags:continue
        if 'red_column' not in n and not (n.startswith('Barracks_') and '_column_' in n):continue
        p=a.get_actor_location();s=a.get_actor_scale3d();o,e=a.get_actor_bounds(False);bottom=o.z-e.z;top=o.z+e.z;candidates=[]
        for r in roofs:
            rp=r.get_actor_location();rs=r.get_actor_scale3d();yaw=math.radians(r.get_actor_rotation().yaw)
            dx=p.x-rp.x;dy=p.y-rp.y;rx=abs(dx*math.cos(yaw)+dy*math.sin(yaw))/(50*rs.x);ry=abs(-dx*math.sin(yaw)+dy*math.cos(yaw))/(50*rs.y)
            if rx>1 or ry>1 or rp.z<top-50:continue
            t=max(0,min(1,(1-rx)/.78,(1-ry)/.97));i=min(4,int(t*5));f=t*5-i
            z0=6 if i==0 else 30*(i/5)**.62;z1=30*((i+1)/5)**.62
            target=rp.z+(z0+(z1-z0)*f)*rs.z+3
            if 2<target-top<500:candidates.append(target)
        if candidates:
            target=min(candidates);height=target-bottom
            a.set_actor_location(V(p.x,p.y,(target+bottom)/2),False,False);a.set_actor_scale3d(V(s.x,s.y,height/100));a.tags=list(a.tags)+[tag]
            changes.append({'label':n,'extended_cm':target-top})
    if not any(a.get_actor_label().startswith('Repair_Bridge_piling') for a in current):
        planks=sorted([a for a in current if a.get_actor_label().startswith('Temple_Axis_bridge_plank')],key=lambda a:a.get_actor_location().y)
        for i in [3,8,13,18,23,27]:
            a=planks[i];p=a.get_actor_location();top=p.z-12
            for side in [-1,1]:
                support=box('Bridge_piling',p.x+side*320,p.y,(top+43)/2,35,35,max(5,top-43),'wood')
                support.set_actor_label('Repair_Bridge_piling');support.set_folder_path('Temple/Repairs')
    assert L.save_current_level();reports.append({'map':day,'column_repairs':changes,'bridge_pilings':12})
with open(os.path.join(ROOT,'roof_support_report.json'),'w',encoding='utf-8') as f:json.dump(reports,f,indent=2)
u.EditorAssetLibrary.save_directory('/Game/Jangan',True,True)
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(V(14000,1000,2600),u.Rotator(pitch=-15,yaw=135,roll=0))
u.log('ROOF_SUPPORTS_FIXED')
