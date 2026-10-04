import unreal as u,os,json,math
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
source=open(os.path.join(ROOT,'Scripts','build_temple.py'),encoding='utf-8').read()
exec(compile(source.split('L.save_current_level();report=[]')[0],__file__,'exec'))
tag=u.Name('AssemblyRepairV2');reports=[];L.save_current_level()
def bounds(a):
    o,e=a.get_actor_bounds(False);return o,e,o.z-e.z,o.z+e.z
for day in ['Night','Day']:
    path='/Game/Jangan/Maps/Jangan_'+day;assert L.load_level(path)
    current=list(A.get_all_level_actors());world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
    if any(a.get_actor_label()=='Repair_Dry_landing_V2' for a in current):continue
    backup='/Game/Jangan/Backups/Jangan_'+day+'_BeforeAssemblyRepairV2'
    if not u.EditorAssetLibrary.does_asset_exist(backup):assert u.EditorAssetLibrary.duplicate_asset(path,backup)
    roofs=[a for a in current if isinstance(a,u.StaticMeshActor) and a.static_mesh_component.static_mesh==meshes['Roof']]
    fascia=[];columns=[];lamps=[]
    # Put a solid timber cornice under each roof: no exposed air between beam and eaves.
    for r in roofs:
        n=r.get_actor_label();p=r.get_actor_location();s=r.get_actor_scale3d();o,e,low,high=bounds(r)
        if max(e.x,e.y)<250 or n.startswith(('Temple_Pagoda','PalaceGarden_Lantern')):continue
        beam_tops=[]
        for a in current:
            if not isinstance(a,u.StaticMeshActor) or a.static_mesh_component.static_mesh!=meshes['Cube']:continue
            ap=a.get_actor_location();ao,ae,al,ah=bounds(a)
            if abs(ap.x-p.x)<100 and abs(ap.y-p.y)<100 and ae.z<100 and max(ae.x,ae.y)>250 and 0<=low-ah<=600:beam_tops.append(ah)
        base=max(beam_tops) if beam_tops else low-180
        h=max(35,low-base+4)
        a=box('Roof_cornice',p.x,p.y,low-h/2+2,100*s.x*.82,100*s.y*.82,h,'wood',False)
        a.set_actor_rotation(r.get_actor_rotation(),False);a.set_actor_label('Repair_Roof_cornice');a.set_folder_path('Repairs/Roofs');a.tags=[tag];fascia.append(n)
    # Trim all structural columns to the underside of their nearest roof, using actual imported bounds.
    for a in current:
        n=a.get_actor_label()
        if not isinstance(a,u.StaticMeshActor):continue
        c=a.static_mesh_component;p=a.get_actor_location();s=a.get_actor_scale3d();o,e,low,high=bounds(a)
        red=c.get_material(0)==M['red']
        if not ((red and max(e.x,e.y)<100 and e.z>100) or n.startswith('Barracks_Stable_post')):continue
        candidates=[]
        for r in roofs:
            ro,re,rl,rh=bounds(r)
            if abs(p.x-ro.x)<=re.x and abs(p.y-ro.y)<=re.y and low+100<rl<high+600:candidates.append(rl)
        if candidates:
            top=min(candidates)-8
            h=top-low;a.set_actor_location(V(p.x,p.y,low+h/2),False,False);a.set_actor_scale3d(V(s.x,s.y,s.z*h/(high-low)))
            columns.append(n)
    # Treat the post, lantern body and cap as one connected assembly.
    for a in current:
        n=a.get_actor_label()
        if not isinstance(a,u.StaticMeshActor) or not ('Lantern_post' in n or 'lantern_post' in n):continue
        p=a.get_actor_location();o,e,low,high=bounds(a);s=a.get_actor_scale3d()
        nearby=[b for b in current if isinstance(b,u.StaticMeshActor) and abs(b.get_actor_location().x-p.x)<2 and abs(b.get_actor_location().y-p.y)<2 and b.static_mesh_component.get_material(0)==M['lamp']]
        if not nearby:continue
        body=min(nearby,key=lambda b:abs(b.get_actor_location().z-high));bo,be,bl,bh=bounds(body)
        hit=u.SystemLibrary.line_trace_single(world,V(p.x,p.y,p.z),V(p.x,p.y,-300),u.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[a,body],u.DrawDebugTrace.NONE,True)
        floor=hit.to_tuple()[5].z if hit is not None and not hit.to_tuple()[1] else 25
        top=bl+3;h=top-floor;a.set_actor_location(V(p.x,p.y,floor+h/2),False,False);a.set_actor_scale3d(V(s.x,s.y,s.z*h/(high-low)))
        for r in roofs:
            rp=r.get_actor_location()
            if abs(rp.x-p.x)<2 and abs(rp.y-p.y)<2 and abs(bounds(r)[2]-bh)<150:
                delta=bh-2-bounds(r)[2];r.set_actor_location(V(rp.x,rp.y,rp.z+delta),False,False)
        lamps.append(n)
    # Finish water and timber first, then provide dry ground before the stone steps.
    for a in current:
        n=a.get_actor_label();p=a.get_actor_location();s=a.get_actor_scale3d()
        if n.startswith(('Temple_Organic','Temple_Shore','Temple_Lotus_leaf','Temple_Lotus_flower')):
            a.set_actor_location(V(p.x,5650+(p.y-6000)*.60,p.z),False,False)
            if n.startswith('Temple_Organic'):
                # Pond mesh is rotated 90 degrees, so local X controls world Y.
                a.set_actor_scale3d(V(s.x*.60,s.y,s.z))
        elif n.startswith(('Temple_Axis_bridge','Repair_Bridge_piling')):
            a.set_actor_location(V(p.x,4000+(p.y-4000)*.81,p.z),False,False)
            if 'plank' in n or 'rail' in n:a.set_actor_scale3d(V(s.x,s.y*.81,s.z))
    a=box('Dry_landing',-8650,6650,44,1050,600,38,'stone')
    a.set_actor_label('Repair_Dry_landing_V2');a.set_folder_path('Temple/Repairs');a.tags=[tag]
    # Last stair front edge is y=6922.5; landing stops at 6950, with only the first riser meeting it.
    assert L.save_current_level();reports.append({'map':day,'roof_cornices':len(fascia),'trimmed_columns':len(columns),'connected_lanterns':len(lamps),'bridge_end_y':6390,'stone_stairs_start_y':6922.5,'backup':backup})
u.EditorAssetLibrary.save_directory('/Game/Jangan',True,True)
with open(os.path.join(ROOT,'assembly_repair_report.json'),'w',encoding='utf-8') as f:json.dump(reports,f,indent=2)
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(V(-11000,3400,2200),u.Rotator(pitch=-18,yaw=55,roll=0))
u.log('ASSEMBLIES_REPAIRED_V2')
