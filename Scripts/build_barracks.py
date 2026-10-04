"""Replace the pool precinct with a compact Tang-inspired barracks blockout."""
import unreal as u,os,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A=u.get_editor_subsystem(u.EditorActorSubsystem);L=u.get_editor_subsystem(u.LevelEditorSubsystem)
V=u.Vector
roof=u.load_asset('/Game/Jangan/Meshes/SM_CurvedHipRoof')
cube=u.load_asset('/Engine/BasicShapes/Cube');cylinder=u.load_asset('/Engine/BasicShapes/Cylinder')
def mat(name,color):
    path='/Game/Jangan/Materials/'+name;m=u.load_asset(path)
    if m:return m
    m=u.AssetToolsHelpers.get_asset_tools().create_asset(name,'/Game/Jangan/Materials',u.Material,u.MaterialFactoryNew())
    m.set_editor_property('two_sided',True)
    n=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant3Vector,-300,0)
    n.set_editor_property('constant',u.LinearColor(*color,1))
    u.MaterialEditingLibrary.connect_material_property(n,'',u.MaterialProperty.MP_BASE_COLOR)
    u.MaterialEditingLibrary.recompile_material(m);u.EditorAssetLibrary.save_loaded_asset(m)
    return m
M={k:u.load_asset('/Game/Jangan/Materials/'+n) for k,n in [('stone','M_WarmLimestone'),('red','M_CinnabarWood'),('wood','M_DarkTimber'),('gold','M_ImperialGold'),('lamp','M_LanternGlow'),('water','M_JadeWater')]}
M.update(roof=mat('M_BarracksGrayTile',(.075,.085,.085)),wall=mat('M_BarracksEarthPlaster',(.38,.30,.21)),earth=mat('M_BarracksDrillEarth',(.22,.15,.08)))
def shape(name,mesh,loc,scale,material,yaw=0,solid=True):
    a=A.spawn_actor_from_class(u.StaticMeshActor,V(*loc),u.Rotator(pitch=0,yaw=yaw,roll=0))
    a.set_actor_label('Barracks_'+name);a.set_folder_path('Barracks')
    c=a.static_mesh_component;c.set_static_mesh(mesh);c.set_material(0,M[material]);c.set_mobility(u.ComponentMobility.STATIC)
    a.set_actor_scale3d(V(*scale));c.set_collision_profile_name('BlockAll' if solid else 'NoCollision')
    c.set_collision_enabled(u.CollisionEnabled.QUERY_AND_PHYSICS if solid else u.CollisionEnabled.NO_COLLISION);a.set_actor_enable_collision(solid)
    return a
def box(n,x,y,z,w,d,h,m,yaw=0):return shape(n,cube,(x,y,z),(w/100,d/100,h/100),m,yaw)
def tile(n,x,y,z,w,d,h,yaw=0):return shape(n,roof,(x,y,z),(w/100,d/100,h/30),'roof',yaw,False)
def hall(n,x,y,w,d,h,yaw=0):
    box(n+'_foundation',x,y,75,w+140,d+140,100,'stone',yaw)
    box(n+'_plaster',x,y,125+h/2,w*.94,d*.82,h,'wall',yaw)
    import math
    q=math.radians(yaw)
    def point(dx,dy):return x+dx*math.cos(q)-dy*math.sin(q),y+dx*math.sin(q)+dy*math.cos(q)
    for i,dx in enumerate([-w*.42,0,w*.42]):
        for side in [-1,1]:
            px,py=point(dx,side*d*.46)
            shape(n+'_column_'+str(i)+'_'+str(side),cylinder,(px,py,125+h/2),(.6,.6,h/100),'red')
        px,py=point(dx,-d*.42-8);box(n+'_door_'+str(i),px,py,270,155,20,290,'wood',yaw)
    box(n+'_beam',x,y,125+h,w,d,65,'wood',yaw)
    tile(n+'_roof',x,y,160+h,w+240,d+260,310,yaw)
def lantern(n,x,y):
    shape(n+'_post',cylinder,(x,y,180),(.22,.22,3.1),'wood')
    shape(n+'_lantern',cylinder,(x,y,365),(.7,.7,.8),'lamp',solid=False)
    tile(n+'_cap',x,y,410,110,110,30)

L.save_current_level();reports=[]
for day in ['Night','Day']:
    path='/Game/Jangan/Maps/Jangan_'+day;assert L.load_level(path)
    current=list(A.get_all_level_actors())
    if any(a.get_actor_label()=='Barracks_Drill_ground' for a in current):
        reports.append({'map':day,'already_built':True});continue
    backup='/Game/Jangan/Backups/Jangan_'+day+'_BeforeBarracks'
    if not u.EditorAssetLibrary.does_asset_exist(backup):assert u.EditorAssetLibrary.duplicate_asset(path,backup)
    removed=[]
    for a in current:
        label=a.get_actor_label();p=a.get_actor_location()
        in_area=5600<=p.x<=12000 and 2500<=p.y<=10500
        eligible=(label.startswith('Shop_HunterAssociation_') or (in_area and label.startswith(('Garden_pond','Garden_bridge','Bridge_rail','Garden_pavilion','Tree_trunk','Tree_crown'))))
        if isinstance(a,u.StaticMeshActor) and eligible:
            removed.append(label);A.destroy_actor(a)
    # Preserve the association NPC at the new precinct entrance.
    for a in current:
        if a.get_actor_label() in ['NPC_HunterAssociation','NPC_Name_HunterAssociation','Shop_Sign_HunterAssociation']:
            p=a.get_actor_location();a.set_actor_location(V(7300,2700,p.z),False,False)
    box('Drill_ground',8850,6700,33,5700,7200,16,'earth')
    box('Front_path',8600,2300,35,1800,1800,20,'stone')
    for x in [6000,11700]:box('Side_wall',x,6700,190,100,7200,330,'wall')
    box('Rear_wall',8850,10300,190,5700,100,330,'wall')
    box('Front_wall_left',6750,3100,190,1500,100,330,'wall')
    box('Front_wall_right',10650,3100,190,2100,100,330,'wall')
    for x in [7500,9700]:
        box('Gate_pier',x,3100,375,280,620,700,'stone')
        box('Gate_red_post',x,3100,740,90,100,140,'red')
    box('Gate_beam',8600,3100,820,2600,740,100,'wood')
    tile('Main_gate_roof',8600,3100,890,3100,1100,370)
    hall('Command_hall',8850,9200,3700,1400,650)
    hall('West_barrack',6650,6600,3300,1050,470,90)
    hall('East_barrack',11050,6600,3300,1050,470,-90)
    # Small covered stable and practical water trough.
    for x in [9950,11250]:
        for y in [3800,4500]:box('Stable_post',x,y,290,45,45,530,'wood')
    tile('Stable_shelter',10600,4150,580,1650,1100,260)
    box('Stable_tie_rail',10600,4450,160,1400,35,35,'wood')
    box('Water_trough',6550,4100,100,460,230,150,'stone')
    shape('Water_trough_surface',cube,(6550,4100,181),(3.8,1.6,.05),'water',solid=False)
    # Targets sit at the rear of the training space, leaving the center open.
    for x in [8000,8600,9200]:
        box('Target_post',x,7900,180,35,35,300,'wood')
        box('Archery_target',x,7900,330,200,30,200,'stone')
        box('Target_mark',x,7878,330,60,8,60,'red')
    for x in [7400,9800]:
        shape('Banner_pole',cylinder,(x,3400,540),(.22,.22,10),'wood')
        shape('Military_banner',cube,(x+115,3400,825),(2.1,.08,3.3),'red',solid=False)
    for x in [7700,9500]:lantern('Gate_lantern',x,2800)
    if day=='Night':
        for x in [7700,9500]:
            a=A.spawn_actor_from_class(u.PointLight,V(x,2800,390));a.set_actor_label('Barracks_Gate_light');a.set_folder_path('Barracks')
            c=a.light_component;c.set_mobility(u.ComponentMobility.MOVABLE);c.set_editor_property('intensity',130)
            c.set_editor_property('attenuation_radius',1500);c.set_editor_property('cast_shadows',False);c.set_light_color(u.LinearColor(1,.55,.22))
    world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
    gate=u.SystemLibrary.line_trace_single(world,V(8600,2300,180),V(8600,4000,180),u.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[],u.DrawDebugTrace.NONE,True)
    assert gate is None,'Barracks gate is blocked'
    floor=u.SystemLibrary.line_trace_single(world,V(8600,6000,400),V(8600,6000,-100),u.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[],u.DrawDebugTrace.NONE,True)
    assert floor is not None,'Training yard has no collision'
    assert L.save_current_level()
    reports.append({'map':day,'removed':removed,'gate_clear':True,'yard_floor':str(floor.to_tuple()),'backup':backup})
with open(os.path.join(ROOT,'barracks_report.json'),'w',encoding='utf-8') as f:json.dump(reports,f,ensure_ascii=False,indent=2)
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(V(14500,-1500,7400),u.Rotator(pitch=-31,yaw=126,roll=0))
u.log('BARRACKS_SAVED '+str([(r['map'],len(r.get('removed',[]))) for r in reports]))
