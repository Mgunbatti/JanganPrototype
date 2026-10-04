import unreal as u, os, json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A=u.get_editor_subsystem(u.EditorActorSubsystem)
L=u.get_editor_subsystem(u.LevelEditorSubsystem)
idle=u.load_asset('/Game/Characters/Mannequins/Anims/Unarmed/MM_Idle')
result=[]
for day in ['Night','Day']:
    assert L.load_level('/Game/Jangan/Maps/Jangan_'+day)
    current=list(A.get_all_level_actors())
    npcs=[a for a in current if isinstance(a,u.SkeletalMeshActor) and a.get_actor_label().startswith('NPC_')]
    assert len(npcs)==10,'Expected 10 NPCs'
    for a in npcs: a.skeletal_mesh_component.override_animation_data(idle,True,True,0.0,1.0)
    assert L.save_current_level()
    assert L.load_level('/Game/Jangan/Maps/Jangan_'+day)
    world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
    checks=[]
    for a in A.get_all_level_actors():
        if isinstance(a,u.SkeletalMeshActor) and a.get_actor_label().startswith('NPC_'):
            c=a.skeletal_mesh_component
            data=c.get_editor_property('animation_data')
            p=a.get_actor_location()
            floor=u.SystemLibrary.line_trace_single(world,p+u.Vector(0,0,300),p-u.Vector(0,0,100),u.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[a],u.DrawDebugTrace.NONE,True)
            assert floor is not None,'NPC has no ground: '+a.get_actor_label()
            checks.append({'npc':a.get_actor_label(),'saved_animation':str(data),'floor':str(floor.to_tuple())})
    result.append({'map':day,'npcs':checks})
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(u.Vector(-1100,-3900,380),u.Rotator(pitch=-8,yaw=164,roll=0))
with open(os.path.join(ROOT,'npc_validation.json'),'w',encoding='utf-8') as f: json.dump(result,f,ensure_ascii=False,indent=2)
u.log('NPC_VALIDATION_COMPLETE')
