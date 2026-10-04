import unreal as u,os,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
source=open(os.path.join(ROOT,'Scripts','build_temple.py'),encoding='utf-8').read()
exec(compile(source.split('L.save_current_level();report=[]')[0],__file__,'exec'))
M['wall']=u.load_asset('/Game/Jangan/Materials/M_IvoryPlaster')
tag=u.Name('GateRoofRepairV1');reports=[];L.save_current_level()
def bounds(a):
    o,e=a.get_actor_bounds(False);return o,e,o.z-e.z,o.z+e.z
for day in ['Night','Day']:
    path='/Game/Jangan/Maps/Jangan_'+day;assert L.load_level(path)
    current=list(A.get_all_level_actors());roofs=[a for a in current if isinstance(a,u.StaticMeshActor) and a.static_mesh_component.static_mesh==meshes['Roof']]
    backup='/Game/Jangan/Backups/Jangan_'+day+'_BeforeGateRidgeRepair'
    if not u.EditorAssetLibrary.does_asset_exist(backup):assert u.EditorAssetLibrary.duplicate_asset(path,backup)
    gates=[]
    for side in ['South','East','West']:
        matching=[a for a in current if isinstance(a,u.StaticMeshActor) and (a.get_actor_label().startswith(('Jangan_South_Gate','Jangan_Gate_upper','Gate_overpass')) if side=='South' else a.get_actor_label().startswith(side+'_Gate_'))]
        lower=next(a for a in matching if a.static_mesh_component.static_mesh==meshes['Roof'] and 'South_Gate' in a.get_actor_label())
        upper=next(a for a in matching if a.static_mesh_component.static_mesh==meshes['Roof'] and 'Gate_upper' in a.get_actor_label())
        beam=next(a for a in matching if 'Gate_overpass' in a.get_actor_label())
        if tag not in lower.tags:
            p=lower.get_actor_location();delta=bounds(beam)[3]-bounds(lower)[2]+1
            lower.set_actor_location(V(p.x,p.y,p.z+delta),False,False);lower.tags=list(lower.tags)+[tag]
            # Proper compact upper gate chamber supports the second roof, rather than a thick band.
            floor=bounds(lower)[3]-35;ceiling=floor+220
            p=upper.get_actor_location();upper.set_actor_location(V(p.x,p.y,p.z+ceiling-bounds(upper)[2]),False,False)
            s=upper.get_actor_scale3d();yaw=upper.get_actor_rotation()
            a=box('Gate_upper_chamber',p.x,p.y,(floor+ceiling)/2,100*s.x*.55,100*s.y*.50,220,'wall')
            a.set_actor_rotation(yaw,False);a.set_actor_label('GateRepair_'+side+'_upper_chamber');a.set_folder_path('Fortifications/Repairs')
            gates.append(side)
    # Match gold ornaments by material, mesh and proximity, including anonymously named NPC shop parts.
    ridges=[]
    for a in current:
        if not isinstance(a,u.StaticMeshActor):continue
        c=a.static_mesh_component
        if c.static_mesh!=meshes['Cube'] or c.get_material(0)!=M['gold']:continue
        p=a.get_actor_location();o,e,low,high=bounds(a)
        if e.z>40 or max(e.x,e.y)<45:continue
        candidates=[]
        for r in roofs:
            rp=r.get_actor_location();ro,re,rl,rh=bounds(r)
            if abs(p.x-rp.x)<5 and abs(p.y-rp.y)<5 and abs(low-rh)<850:candidates.append((abs(low-rh),r,rh))
        if candidates:
            _,r,target=min(candidates,key=lambda x:x[0]);delta=target-2-low
            if abs(delta)>.5:a.set_actor_location(V(p.x,p.y,p.z+delta),False,False);ridges.append({'label':a.get_actor_label(),'delta':delta})
    assert L.save_current_level();reports.append({'map':day,'gates_repaired':gates,'gold_ridges':ridges,'backup':backup})
u.EditorAssetLibrary.save_directory('/Game/Jangan',True,True)
with open(os.path.join(ROOT,'gate_ridge_report.json'),'w',encoding='utf-8') as f:json.dump(reports,f,indent=2)
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(V(6500,-16500,4000),u.Rotator(pitch=-12,yaw=125,roll=0))
u.log('GATE_ROOFS_RIDGES_FIXED')
