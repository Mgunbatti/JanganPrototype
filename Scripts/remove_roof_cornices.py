"""Remove bulky repair bands and seat roofs directly on existing beams."""
import unreal as u,os,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
source=open(os.path.join(ROOT,'Scripts','build_temple.py'),encoding='utf-8').read()
exec(compile(source.split('L.save_current_level();report=[]')[0],__file__,'exec'))
reports=[];L.save_current_level()
for day in ['Night','Day']:
    path='/Game/Jangan/Maps/Jangan_'+day;assert L.load_level(path)
    current=list(A.get_all_level_actors())
    bands=[a for a in current if a.get_actor_label()=='Repair_Roof_cornice']
    if not bands:continue
    backup='/Game/Jangan/Backups/Jangan_'+day+'_BeforeCorniceRemoval'
    if not u.EditorAssetLibrary.does_asset_exist(backup):assert u.EditorAssetLibrary.duplicate_asset(path,backup)
    roofs=[a for a in current if isinstance(a,u.StaticMeshActor) and a.static_mesh_component.static_mesh==meshes['Roof']]
    moved=[]
    for b in bands:
        p=b.get_actor_location();o,e=b.get_actor_bounds(False);band_bottom=o.z-e.z
        candidates=[r for r in roofs if abs(r.get_actor_location().x-p.x)<1 and abs(r.get_actor_location().y-p.y)<1]
        if candidates:
            r=min(candidates,key=lambda r:abs((r.get_actor_bounds(False)[0].z-r.get_actor_bounds(False)[1].z)-(o.z+e.z)))
            ro,re=r.get_actor_bounds(False);rp=r.get_actor_location();delta=band_bottom+2-(ro.z-re.z)
            r.set_actor_location(V(rp.x,rp.y,rp.z+delta),False,False);moved.append((r,delta))
            # Ridge ornaments follow their own roof; do not move separate upper tiers.
            for a in current:
                if not isinstance(a,u.StaticMeshActor) or a.get_actor_label()=='Repair_Roof_cornice':continue
                ap=a.get_actor_location();ao,ae=a.get_actor_bounds(False)
                if 'ridge' in a.get_actor_label().lower() and abs(ap.x-rp.x)<1 and abs(ap.y-rp.y)<1 and abs(ap.z-(ro.z+re.z))<100:
                    a.set_actor_location(V(ap.x,ap.y,ap.z+delta),False,False)
        A.destroy_actor(b)
    # Column ends stop inside the underside, avoiding protruding tips.
    columns=0
    for a in current:
        if not isinstance(a,u.StaticMeshActor) or a.get_actor_label()=='Repair_Roof_cornice':continue
        n=a.get_actor_label();c=a.static_mesh_component
        if c.static_mesh not in [meshes['Cylinder'],meshes['Cube']]:continue
        o,e=a.get_actor_bounds(False)
        if not ((c.get_material(0)==M['red'] and max(e.x,e.y)<100 and e.z>100) or n.startswith('Barracks_Stable_post')):continue
        p=a.get_actor_location();s=a.get_actor_scale3d();bottom=o.z-e.z;top=o.z+e.z;targets=[]
        for r,delta in moved:
            ro,re=r.get_actor_bounds(False);low=ro.z-re.z
            if abs(p.x-ro.x)<=re.x and abs(p.y-ro.y)<=re.y and bottom+100<low<top+300:targets.append(low)
        if targets:
            target=min(targets)+2;h=target-bottom
            a.set_actor_location(V(p.x,p.y,bottom+h/2),False,False);a.set_actor_scale3d(V(s.x,s.y,s.z*h/(2*e.z)));columns+=1
    assert L.save_current_level();reports.append({'map':day,'removed_bands':len(bands),'seated_roofs':len(moved),'adjusted_columns':columns,'backup':backup})
u.EditorAssetLibrary.save_directory('/Game/Jangan',True,True)
with open(os.path.join(ROOT,'cornice_removal_report.json'),'w',encoding='utf-8') as f:json.dump(reports,f,indent=2)
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(V(0,3500,2500),u.Rotator(pitch=-8,yaw=90,roll=0))
u.log('ROOF_CORNICES_REMOVED')
