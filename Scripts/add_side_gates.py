"""In-place update: preserve south gate, add matching side gates and balance colors."""
import unreal as u
import math, os, json

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
actors=u.get_editor_subsystem(u.EditorActorSubsystem)
levels=u.get_editor_subsystem(u.LevelEditorSubsystem)
V=u.Vector
reports=[]
levels.save_current_level()

def copy_part(src,label,loc,yaw=0):
    r=src.get_actor_rotation()
    a=actors.spawn_actor_from_class(u.StaticMeshActor,V(*loc),u.Rotator(pitch=r.pitch,yaw=r.yaw+yaw,roll=r.roll))
    a.set_actor_label(label)
    a.set_folder_path('Fortifications/SideGates')
    a.set_actor_scale3d(src.get_actor_scale3d())
    c=a.static_mesh_component
    sc=src.static_mesh_component
    c.set_static_mesh(sc.static_mesh)
    for i in range(sc.get_num_materials()): c.set_material(i,sc.get_material(i))
    c.set_mobility(u.ComponentMobility.STATIC)
    solid=str(sc.get_collision_profile_name())!='NoCollision'
    c.set_collision_profile_name('BlockAll' if solid else 'NoCollision')
    c.set_collision_enabled(u.CollisionEnabled.QUERY_AND_PHYSICS if solid else u.CollisionEnabled.NO_COLLISION)
    a.set_actor_enable_collision(solid)
    return a

# Update constant base-color nodes directly; material assets remain shared by both maps.
palette={
    'M_WarmLimestone':(.34,.28,.20),
    'M_IvoryPlaster':(.57,.43,.27),
    'M_CinnabarWood':(.40,.032,.018),
    'M_JadeRoof':(.025,.16,.12),
    'M_DarkTimber':(.10,.052,.029),
    'M_StonePaving':(.31,.28,.22),
}
for name,color in (palette.items() if not os.path.exists(os.path.join(ROOT,'palette_applied.txt')) else []):
    m=u.load_asset('/Game/Jangan/Materials/'+name)
    if not m: raise RuntimeError('Missing '+name)
    node=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant3Vector,-500,-150)
    node.set_editor_property('constant',u.LinearColor(*color,1))
    u.MaterialEditingLibrary.connect_material_property(node,'',u.MaterialProperty.MP_BASE_COLOR)
    u.MaterialEditingLibrary.recompile_material(m)
    u.EditorAssetLibrary.save_loaded_asset(m)
with open(os.path.join(ROOT,'palette_applied.txt'),'w') as f: f.write('applied')
for sky_name in ['M_DaySky','M_NightSky']:
    m=u.load_asset('/Game/Jangan/Materials/'+sky_name)
    if not m.get_editor_property('is_sky'):
        m.set_editor_property('is_sky',True)
        u.MaterialEditingLibrary.recompile_material(m)
        u.EditorAssetLibrary.save_loaded_asset(m)

for name in ['Night','Day']:
    if not levels.load_level('/Game/Jangan/Maps/Jangan_'+name): raise RuntimeError('Map load failed')
    current=list(actors.get_all_level_actors())
    south=[a for a in current if isinstance(a,u.StaticMeshActor) and
           (a.get_actor_label().startswith(('Gate_stone_pier','Gate_overpass','Jangan_South_Gate','Jangan_Gate_upper')))]
    if len(south)!=7: raise RuntimeError('South gate parts expected 7, found '+str(len(south)))
    created=[]
    for side,x,yaw in [('East',13000,90),('West',-13000,-90)]:
        for i,src in enumerate(south):
            label=side+'_Gate_'+str(i)+'_'+src.get_actor_label()
            if any(a.get_actor_label()==label for a in current): continue
            p=src.get_actor_location(); dx=p.x; dy=p.y+12800
            rad=math.radians(yaw)
            loc=(x+math.cos(rad)*dx-math.sin(rad)*dy,500+math.sin(rad)*dx+math.cos(rad)*dy,p.z)
            created.append(copy_part(src,label,loc,yaw))
        wall=next((a for a in current if isinstance(a,u.StaticMeshActor) and a.get_actor_label().startswith('City_wall') and abs(a.get_actor_location().x-x)<1),None)
        if wall:
            upper=copy_part(wall,side+'_Wall_North',(x,8400,470))
            upper.set_actor_scale3d(V(2.4,132,9.4))
            wall.set_actor_label(side+'_Wall_South')
            wall.set_actor_location(V(x,-6900,470),False,False)
            wall.set_actor_scale3d(V(2.4,122,9.4))
    for a in actors.get_all_level_actors():
        if a.get_actor_label()=='East_west_avenue': a.set_actor_scale3d(V(350,14,.22))
        if isinstance(a,u.SkyLight):
            c=a.light_component
            c.set_editor_property('sky_distance_threshold',10000)
            c.set_editor_property('lower_hemisphere_is_black',False)
            c.set_editor_property('intensity',.4 if name=='Night' else .15)
            # Real-time capture restores the ambient fill after loading or playing the map.
            c.set_editor_property('real_time_capture',True)
            c.recapture_sky()
        if isinstance(a,u.DirectionalLight) and name=='Day':
            a.light_component.set_editor_property('intensity',2.5)
            a.light_component.set_light_color(u.LinearColor(1,.88,.70))
    # Trace through the empty gate centers at character chest height.
    world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
    checks={}
    for side,x in [('East',13000),('West',-13000)]:
        h=u.SystemLibrary.line_trace_single(world,V(x-1500,500,180),V(x+1500,500,180),u.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[],u.DrawDebugTrace.NONE,True)
        checks[side]='clear' if h is None else str(h.to_tuple())
    levels.save_current_level()
    reports.append({'map':name,'created_gate_parts':len(created),'passage_traces':checks,'project':u.Paths.project_dir()})

u.EditorAssetLibrary.save_directory('/Game/Jangan',False,True)
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(V(23500,-9500,9500),u.Rotator(pitch=-22,yaw=155,roll=0))
with open(os.path.join(ROOT,'gate_update_report.json'),'w',encoding='utf-8') as f: json.dump(reports,f,indent=2)
u.log('JANGAN SIDE GATES AND COLORS SAVED '+str(reports))
