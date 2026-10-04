"""Audit grounded components, repair support gaps, and recolor Buddha as jade."""
import unreal as u,os,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
source=open(os.path.join(ROOT,'Scripts','build_temple.py'),encoding='utf-8').read()
exec(compile(source.split('L.save_current_level();report=[]')[0],__file__,'exec'))
jade=material('M_BuddhaJade',(.028,.33,.19),.08)
tag=u.Name('CityContactFixV1');reports=[];L.save_current_level()
for day in ['Night','Day']:
    path='/Game/Jangan/Maps/Jangan_'+day;assert L.load_level(path)
    current=list(A.get_all_level_actors());world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
    backup='/Game/Jangan/Backups/Jangan_'+day+'_BeforeContactFix'
    if not u.EditorAssetLibrary.does_asset_exist(backup):assert u.EditorAssetLibrary.duplicate_asset(path,backup)
    fixed=[];checked=0
    for a in current:
        if not isinstance(a,u.StaticMeshActor):continue
        n=a.get_actor_label();p=a.get_actor_location();s=a.get_actor_scale3d()
        if n.startswith('Legends_Buddha'):a.static_mesh_component.set_material(0,jade)
        if tag in a.tags:continue
        # Stable columns: feet at yard level, tops inside the sloping roof at their actual XY position.
        if n.startswith('Barracks_Stable_post'):
            h=700-41;a.set_actor_location(V(p.x,p.y,(700+41)/2),False,False);a.set_actor_scale3d(V(s.x,s.y,h/100))
            fixed.append({'label':n,'fix':'stable post extended to roof','bottom':41,'top':700});a.tags=list(a.tags)+[tag];continue
        # Only parts intended to stand on a surface; roofs, leaves, banners and magic remain elevated.
        grounded=(n.endswith('_foundation') or '_Tree_trunk' in n or n.startswith('Tree_trunk') or n.startswith('Lantern_post') or n.endswith('_Lantern_post') or n.endswith('_Banner_pole') or n.endswith('_Bench_leg') or n in ['Temple_Pagoda_base','Legends_Lotus_plinth'] or n.endswith('_Water_trough'))
        if not grounded:continue
        origin,extent=a.get_actor_bounds(False);bottom=origin.z-extent.z;checked+=1
        hit=u.SystemLibrary.line_trace_single(world,V(p.x,p.y,bottom+200),V(p.x,p.y,bottom-1000),u.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[a],u.DrawDebugTrace.NONE,True)
        if hit is None:continue
        data=hit.to_tuple()
        if data[1]:continue
        floor=data[5].z;gap=bottom-floor
        if 1.5<gap<190:
            a.set_actor_location(V(p.x,p.y,p.z-gap+.5),False,False);fixed.append({'label':n,'fix':'grounded','gap_cm':gap,'floor':floor});a.tags=list(a.tags)+[tag]
    # The pagoda tiers had isolated eaves with air gaps above each roof: fill with recessed shafts.
    if not any(a.get_actor_label()=='Repair_Pagoda_connector_0' for a in current):
        for i in range(6):
            z=25+(255+i*275+335-25)*1.1
            w=(1400-(i+1)*105)*.78*1.15
            a=box('Pagoda_connector_%d'%i,-8650,8500,z,w,w,95,'ivory')
            a.set_actor_label('Repair_Pagoda_connector_%d'%i);a.set_folder_path('Temple/Repairs')
        fixed.append({'fix':'six pagoda inter-tier connectors'})
    assert L.save_current_level();reports.append({'map':day,'checked_grounded_components':checked,'repairs':fixed,'buddha_material':'jade','backup':backup})
u.EditorAssetLibrary.save_directory('/Game/Jangan',True,True)
with open(os.path.join(ROOT,'city_contact_report.json'),'w',encoding='utf-8') as f:json.dump(reports,f,indent=2)
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(V(-14000,2500,4300),u.Rotator(pitch=-22,yaw=44,roll=0))
u.log('CITY_CONTACTS_FIXED')
