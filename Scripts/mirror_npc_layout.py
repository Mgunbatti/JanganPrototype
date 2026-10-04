"""Mirror NPC shop layout horizontally only. Tagged actors make repeat runs safe."""
import unreal as u,os,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A=u.get_editor_subsystem(u.EditorActorSubsystem)
L=u.get_editor_subsystem(u.LevelEditorSubsystem)
tag=u.Name('NPCLayout_HorizontalMirror_V1')
report=[]
L.save_current_level()
for day in ['Night','Day']:
    assert L.load_level('/Game/Jangan/Maps/Jangan_'+day)
    current=list(A.get_all_level_actors())
    selected=[a for a in current if a.get_actor_label().startswith(('Shop_','NPC_'))]
    # Swap the residential counterparts of the two repurposed outer buildings too.
    for x,y in [(-8100,-4600),(8100,3800)]:
        for a in current:
            if not isinstance(a,u.StaticMeshActor): continue
            if not a.get_actor_label().startswith(('Courtyard_house','Courtyard_back_wall','Courtyard_side_wall','Tree_trunk','Tree_crown')): continue
            p=a.get_actor_location()
            if abs(p.x-x)<=1200 and -1100<=p.y-y<=2200 and tag not in a.tags:
                selected.append(a)
    changes=[]
    for a in selected:
        tags=list(a.tags)
        if tag in tags: continue
        p=a.get_actor_location();r=a.get_actor_rotation()
        yaw=-r.yaw if isinstance(a,u.SkeletalMeshActor) else 180-r.yaw
        a.set_actor_location(u.Vector(-p.x,p.y,p.z),False,False)
        a.set_actor_rotation(u.Rotator(pitch=r.pitch,yaw=yaw,roll=r.roll),False)
        tags.append(tag);a.set_editor_property('tags',tags)
        after=a.get_actor_location()
        assert abs(after.x+p.x)<.01 and abs(after.y-p.y)<.01 and abs(after.z-p.z)<.01
        changes.append({'label':a.get_actor_label(),'before':[p.x,p.y,p.z],'after':[after.x,after.y,after.z]})
    npcs=[a for a in A.get_all_level_actors() if isinstance(a,u.SkeletalMeshActor) and a.get_actor_label().startswith('NPC_')]
    assert len(npcs)==10
    assert L.save_current_level()
    report.append({'map':day,'moved_actors':len(changes),'npc_count':len(npcs),'changes':changes})
with open(os.path.join(ROOT,'npc_mirror_report.json'),'w',encoding='utf-8') as f: json.dump(report,f,ensure_ascii=False,indent=2)
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(u.Vector(0,-18500,14500),u.Rotator(pitch=-43,yaw=90,roll=0))
u.log('NPC_HORIZONTAL_MIRROR_SAVED '+str([(r['map'],r['moved_actors'],r['npc_count']) for r in report]))
