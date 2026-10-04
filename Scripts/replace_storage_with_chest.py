"""Replace storage shop with a compact wooden chest beside the dragon square."""
import unreal as u,os,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
source=open(os.path.join(ROOT,'Scripts','build_temple.py'),encoding='utf-8').read()
exec(compile(source.split('L.save_current_level();report=[]')[0],__file__,'exec'))
reports=[];L.save_current_level()
for day in ['Night','Day']:
    path='/Game/Jangan/Maps/Jangan_'+day;assert L.load_level(path)
    current=list(A.get_all_level_actors())
    if any(a.get_actor_label()=='StorageChest_Body' for a in current):continue
    backup='/Game/Jangan/Backups/Jangan_'+day+'_BeforeStorageChest'
    if not u.EditorAssetLibrary.does_asset_exist(backup):assert u.EditorAssetLibrary.duplicate_asset(path,backup)
    removed=[]
    for a in current:
        if isinstance(a,u.StaticMeshActor) and a.get_actor_label().startswith('Shop_Storage_part_'):
            removed.append(a.get_actor_label());A.destroy_actor(a)
    x,y=1900,-1200
    world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
    hit=u.SystemLibrary.line_trace_single(world,V(x,y,600),V(x,y,-300),u.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[],u.DrawDebugTrace.NONE,True)
    assert hit is not None;floor=hit.to_tuple()[5].z
    def chest(n,dx,dy,z,w,d,h,m,solid=False):
        a=box(n,x+dx,y+dy,floor+z,w,d,h,m,solid);a.set_actor_label('StorageChest_'+n);a.set_folder_path('NPC_Shops/StorageChest');return a
    chest('Body',0,0,77,250,170,150,'wood',True)
    chest('Lid',0,0,165,270,188,30,'wood',True)
    for dx in [-105,105]:
        chest('Metal_band',dx,0,78,15,174,150,'bronze')
        chest('Lid_band',dx,0,182,18,190,6,'bronze')
    for dy in [-80,80]:
        chest('Bottom_trim',0,dy,12,250,12,18,'bronze')
    # The lock faces the depot NPC on the west side.
    chest('Lock_plate',-132,0,112,12,45,60,'bronze')
    chest('Keyhole',-140,0,112,5,12,20,'wood')
    for dy in [-57,57]:chest('Corner_cap',-127,dy,35,12,30,55,'bronze')
    for a in current:
        n=a.get_actor_label()
        if n=='Shop_Sign_Storage':
            a.set_actor_location(V(x,y,floor+270),False,False);a.set_actor_rotation(u.Rotator(pitch=0,yaw=180,roll=0),False)
        elif n=='NPC_Storage':a.set_actor_rotation(u.Rotator(pitch=0,yaw=0,roll=0),False)
    assert L.save_current_level();reports.append({'map':day,'removed_parts':len(removed),'chest_position':[x,y,floor],'backup':backup})
u.EditorAssetLibrary.save_directory('/Game/Jangan',True,True)
with open(os.path.join(ROOT,'storage_chest_report.json'),'w',encoding='utf-8') as f:json.dump(reports,f,indent=2)
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(V(5000,-4200,2200),u.Rotator(pitch=-20,yaw=137,roll=0))
u.log('STORAGE_CHEST_SAVED')
