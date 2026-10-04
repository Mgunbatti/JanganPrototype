"""Remove the two unused residential buildings north of the monument square."""
import unreal as u,os,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A=u.get_editor_subsystem(u.EditorActorSubsystem);L=u.get_editor_subsystem(u.LevelEditorSubsystem)
L.save_current_level();report=[]
for day in ['Night','Day']:
    path='/Game/Jangan/Maps/Jangan_'+day;assert L.load_level(path)
    backup='/Game/Jangan/Backups/Jangan_'+day+'_BeforeMonumentClearing'
    if not u.EditorAssetLibrary.does_asset_exist(backup):assert u.EditorAssetLibrary.duplicate_asset(path,backup)
    removed=[]
    for a in list(A.get_all_level_actors()):
        n=a.get_actor_label();p=a.get_actor_location()
        if isinstance(a,u.StaticMeshActor) and n.startswith(('Courtyard_house','Courtyard_back_wall','Courtyard_side_wall')) and abs(abs(p.x)-4700)<=1200 and 2500<=p.y<=6100:
            removed.append(n);A.destroy_actor(a)
    assert L.save_current_level();report.append({'map':day,'removed':removed,'backup':backup})
with open(os.path.join(ROOT,'monument_clearing_report.json'),'w',encoding='utf-8') as f:json.dump(report,f,indent=2)
u.log('MONUMENT_HOUSES_CLEARED')
