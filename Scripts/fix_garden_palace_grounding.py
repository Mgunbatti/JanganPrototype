"""Ground complete garden/lantern assemblies and rebuild the palace's full-width stairs."""
import unreal as u,os,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
source=open(os.path.join(ROOT,'Scripts','build_temple.py'),encoding='utf-8').read()
exec(compile(source.split('L.save_current_level();report=[]')[0],__file__,'exec'))
tag=u.Name('GardenPalaceGroundV1');reports=[];L.save_current_level()
def bounds(a):
    o,e=a.get_actor_bounds(False);return o,e,o.z-e.z,o.z+e.z
for day in ['Night','Day']:
    path='/Game/Jangan/Maps/Jangan_'+day;assert L.load_level(path)
    current=list(A.get_all_level_actors());world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
    if any(a.get_actor_label()=='Repair_Palace_wide_stair_00' for a in current):continue
    backup='/Game/Jangan/Backups/Jangan_'+day+'_BeforeGardenPalaceGround'
    if not u.EditorAssetLibrary.does_asset_exist(backup):assert u.EditorAssetLibrary.duplicate_asset(path,backup)
    garden_deltas=[];bench_count=0;lamp_count=0;urn_count=0
    def floor_at(x,y,z,ignored):
        h=u.SystemLibrary.line_trace_single(world,V(x,y,z),V(x,y,-300),u.TraceTypeQuery.TRACE_TYPE_QUERY1,False,ignored,u.DrawDebugTrace.NONE,True)
        assert h is not None,'Missing floor';return h.to_tuple()[5].z
    # Move both garden islands as complete groups so trees and planting retain their relative heights.
    for plinth in [a for a in current if a.get_actor_label()=='PalaceGarden_Garden_plinth']:
        p=plinth.get_actor_location();group=[a for a in current if isinstance(a,u.StaticMeshActor) and a.get_actor_label().startswith('PalaceGarden_') and abs(a.get_actor_location().x-p.x)<1150 and abs(a.get_actor_location().y-p.y)<1200]
        floor=floor_at(p.x,p.y,250,group);delta=floor-bounds(plinth)[2]
        for a in group:
            q=a.get_actor_location();a.set_actor_location(V(q.x,q.y,q.z+delta),False,False)
        garden_deltas.append(delta)
    # Bench feet meet ground; tops remain embedded in the seats.
    for a in current:
        if a.get_actor_label()!='PalaceGarden_Bench_leg':continue
        p=a.get_actor_location();s=a.get_actor_scale3d();o,e,lo,hi=bounds(a)
        seats=[b for b in current if b.get_actor_label()=='PalaceGarden_Bench_seat' and abs(b.get_actor_location().x-p.x)<260 and abs(b.get_actor_location().y-p.y)<5]
        if not seats:continue
        floor=floor_at(p.x,p.y,90,[a]+seats);top=bounds(seats[0])[2]+5;h=top-floor
        a.set_actor_location(V(p.x,p.y,(top+floor)/2),False,False);a.set_actor_scale3d(V(s.x,s.y,s.z*h/(2*e.z)));bench_count+=1
    # Sit the luminous body on the actual post, then sit the cap on that body.
    roofs=[a for a in current if isinstance(a,u.StaticMeshActor) and a.static_mesh_component.static_mesh==meshes['Roof']]
    for post in current:
        if not isinstance(post,u.StaticMeshActor) or 'lantern_post' not in post.get_actor_label().lower():continue
        p=post.get_actor_location();s=post.get_actor_scale3d();o,e,lo,hi=bounds(post)
        bodies=[a for a in current if isinstance(a,u.StaticMeshActor) and a.static_mesh_component.get_material(0)==M['lamp'] and abs(a.get_actor_location().x-p.x)<2 and abs(a.get_actor_location().y-p.y)<2]
        if not bodies:continue
        body=min(bodies,key=lambda a:abs(a.get_actor_location().z-hi))
        cap=[a for a in roofs if abs(a.get_actor_location().x-p.x)<2 and abs(a.get_actor_location().y-p.y)<2 and abs(bounds(a)[2]-bounds(body)[3])<160]
        floor=floor_at(p.x,p.y,p.z,[post,body]+cap);delta=floor-lo
        post.set_actor_location(V(p.x,p.y,p.z+delta),False,False)
        q=body.get_actor_location();body.set_actor_location(V(q.x,q.y,q.z+(hi+delta)-bounds(body)[2]-2),False,False)
        for c in cap:
            q=c.get_actor_location();c.set_actor_location(V(q.x,q.y,q.z+bounds(body)[3]-bounds(c)[2]-2),False,False)
        lamp_count+=1
    # Ground the two incense cylinders and move their sticks with them.
    for body in [a for a in current if a.get_actor_label()=='Legends_Incense_bowl']:
        p=body.get_actor_location();group=[a for a in current if a.get_actor_label().startswith('Legends_Incense') and abs(a.get_actor_location().x-p.x)<100 and abs(a.get_actor_location().y-p.y)<100]
        floor=floor_at(p.x,p.y,400,group);delta=floor-bounds(body)[2]
        for a in group:
            q=a.get_actor_location();a.set_actor_location(V(q.x,q.y,q.z+delta),False,False)
        urn_count+=1
    # Terrace front is y=6900, top is z=500; stair treads finish exactly at that edge.
    terrace=next(a for a in current if a.get_actor_label()=='Daming_terrace')
    o,e,lo,top=bounds(terrace);front=o.y-e.y;base=25;count=32;tread=50
    for a in current:
        if a.get_actor_label().startswith('Palace_stair_'):A.destroy_actor(a)
    for i in range(count):
        height=(top-base)*(i+1)/count
        a=box('Palace_wide_stair',o.x,front-count*tread+tread/2+i*tread,base+height/2,2*e.x,tread+2,height,'stone')
        a.set_actor_label('Repair_Palace_wide_stair_%02d'%i);a.set_folder_path('Palace/Stairs');a.tags=[tag]
    assert abs(bounds(a)[3]-top)<.1
    assert L.save_current_level();reports.append({'map':day,'garden_deltas':garden_deltas,'bench_feet':bench_count,'lantern_assemblies':lamp_count,'incense_urns':urn_count,'palace_stair_width':2*e.x,'palace_stair_top':top,'backup':backup})
u.EditorAssetLibrary.save_directory('/Game/Jangan',True,True)
with open(os.path.join(ROOT,'garden_palace_ground_report.json'),'w',encoding='utf-8') as f:json.dump(reports,f,indent=2)
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(V(0,1500,3500),u.Rotator(pitch=-15,yaw=90,roll=0))
u.log('GARDENS_PALACE_GROUNDED')
