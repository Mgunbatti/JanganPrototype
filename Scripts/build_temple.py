"""Warm Tang-inspired temple blockout; palace remains the dominant landmark."""
import unreal as u, os, json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A=u.get_editor_subsystem(u.EditorActorSubsystem); L=u.get_editor_subsystem(u.LevelEditorSubsystem); V=u.Vector
meshes={n:u.load_asset('/Engine/BasicShapes/'+n) for n in ['Cube','Cylinder','Sphere','Cone']}
meshes['Roof']=u.load_asset('/Game/Jangan/Meshes/SM_CurvedHipRoof')
M={k:u.load_asset('/Game/Jangan/Materials/'+v) for k,v in [('red','M_CinnabarWood'),('wood','M_DarkTimber'),('gold','M_ImperialGold'),('roof','M_JadeRoof'),('stone','M_WarmLimestone'),('water','M_JadeWater'),('lamp','M_LanternGlow')]}
def material(name,color,metal=0):
    p='/Game/Jangan/Materials'; m=u.load_asset(p+'/'+name)
    if not m:
        m=u.AssetToolsHelpers.get_asset_tools().create_asset(name,p,u.Material,u.MaterialFactoryNew())
        n=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant3Vector,-300,0)
        n.set_editor_property('constant',u.LinearColor(*color,1));u.MaterialEditingLibrary.connect_material_property(n,'',u.MaterialProperty.MP_BASE_COLOR)
        for prop,val in [(u.MaterialProperty.MP_ROUGHNESS,.65),(u.MaterialProperty.MP_METALLIC,metal)]:
            n=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant,-300,150)
            n.set_editor_property('r',val);u.MaterialEditingLibrary.connect_material_property(n,'',prop)
        u.MaterialEditingLibrary.recompile_material(m);u.EditorAssetLibrary.save_loaded_asset(m)
    return m
M['ivory']=material('M_TempleWarmIvory',(.72,.49,.25))
M['bronze']=material('M_TempleHoneyBronze',(.46,.23,.065),.55)
M['pink']=material('M_TempleLotusPink',(.64,.16,.23))
def shape(n,mesh,x,y,z,w,d,h,mat,solid=False):
    a=A.spawn_actor_from_class(u.StaticMeshActor,V(x,y,z));a.set_actor_label('Temple_'+n);a.set_folder_path('Temple')
    c=a.static_mesh_component;c.set_static_mesh(meshes[mesh]);c.set_material(0,M[mat]);c.set_mobility(u.ComponentMobility.STATIC)
    a.set_actor_scale3d(V(w/100,d/100,h/(30 if mesh=='Roof' else 100)))
    c.set_collision_profile_name('BlockAll' if solid else 'NoCollision');c.set_collision_enabled(u.CollisionEnabled.QUERY_AND_PHYSICS if solid else u.CollisionEnabled.NO_COLLISION);a.set_actor_enable_collision(solid)
    return a
def box(n,x,y,z,w,d,h,m,solid=True):return shape(n,'Cube',x,y,z,w,d,h,m,solid)
def roof(n,x,y,z,w,d,h):
    shape(n,'Roof',x,y,z,w,d,h,'roof');box(n+'_gold_ridge',x,y,z+h,w*.24,25,25,'gold',False)
def hall(n,x,y,w,d,h):
    box(n+'_base',x,y,85,w+160,d+160,120,'stone')
    box(n+'_wall',x,y,145+h/2,w*.9,d*.72,h,'ivory')
    for dx in [-w*.4,0,w*.4]:
        for sy in [-1,1]:shape(n+'_column','Cylinder',x+dx,y+sy*d*.44,145+h/2,65,65,h,'red',True)
        box(n+'_door',x+dx,y-d*.37-15,340,150,30,390,'wood')
        box(n+'_lintel',x+dx,y-d*.39,550,180,30,30,'gold',False)
    box(n+'_beam',x,y,145+h,w,d,70,'red');roof(n+'_roof',x,y,180+h,w+260,d+260,330)
L.save_current_level();report=[]
for day in ['Night','Day']:
    path='/Game/Jangan/Maps/Jangan_'+day;assert L.load_level(path)
    current=list(A.get_all_level_actors())
    if any(a.get_actor_label()=='Temple_Courtyard' for a in current):continue
    backup='/Game/Jangan/Backups/Jangan_'+day+'_BeforeTemple'
    if not u.EditorAssetLibrary.does_asset_exist(backup):assert u.EditorAssetLibrary.duplicate_asset(path,backup)
    removed=[]
    for a in current:
        p=a.get_actor_location();n=a.get_actor_label()
        if isinstance(a,u.StaticMeshActor) and -12000<p.x<-6000 and 2500<p.y<10500 and n.startswith(('Courtyard_','Tree_')):
            removed.append(n);A.destroy_actor(a)
        # Broaden the main palace and increase its roofline, keeping terrace and stairs intact.
        if n.startswith('DAMING_MAIN_HALL') and 'PalaceDominanceV1' not in [str(t) for t in a.tags]:
            s=a.get_actor_scale3d();a.set_actor_location(V(p.x*1.12,10800+(p.y-10800)*1.12,500+(p.z-500)*1.3),False,False)
            a.set_actor_scale3d(V(s.x*1.12,s.y*1.12,s.z*1.3));a.tags=list(a.tags)+[u.Name('PalaceDominanceV1')]
    box('Courtyard',-8700,6700,34,5400,6500,18,'stone')
    box('Entrance_path',-8500,2700,34,1500,1800,18,'stone')
    for x in [-11400,-6000]:box('Boundary',x,6700,175,90,6500,290,'ivory')
    box('Rear_boundary',-8700,9950,175,5400,90,290,'ivory')
    for x in [-10300,-6800]:box('Front_boundary',x,3450,175,2200,90,290,'ivory')
    for x in [-9400,-7900]:shape('Gate_column','Cylinder',x,3450,380,100,100,680,'red',True)
    roof('Entry_gate',-8650,3450,760,2100,900,240)
    hall('Prayer_hall',-10200,8100,1800,1700,650)
    # Seven compact tiers; final height about 24m versus the palace's 31m roofline.
    px,py=-7500,8300
    box('Pagoda_base',px,py,140,1700,1700,230,'stone')
    for i in range(7):
        w=1400-i*105; z=255+i*275
        box('Pagoda_tier_%d'%i,px,py,z+115,w*.78,w*.78,230,'ivory')
        for dx in [-w*.32,w*.32]:box('Pagoda_red_trim',px+dx,py-w*.4,z+110,35,25,220,'red',False)
        box('Pagoda_window',px,py-w*.395-8,z+115,90,20,140,'wood',False)
        roof('Pagoda_eaves_%d'%i,px,py,z+225,w+230,w+230,120)
    shape('Pagoda_finial','Cone',px,py,2400,100,100,250,'gold')
    # Stylized seated statue placeholder on a lotus dais, facing south.
    bx,by=-8700,5700
    shape('Lotus_plinth','Cylinder',bx,by,165,950,950,240,'stone',True)
    shape('Lotus_gold_band','Cylinder',bx,by,305,800,800,50,'bronze')
    import math
    for i in range(12):
        t=i*math.tau/12;shape('Lotus_petal','Sphere',bx+350*math.cos(t),by+350*math.sin(t),360,210,160,150,'bronze')
    shape('Buddha_crossed_legs','Sphere',bx,by-60,460,650,450,230,'bronze')
    shape('Buddha_robed_torso','Sphere',bx,by+30,740,430,310,600,'bronze')
    shape('Buddha_head','Sphere',bx,by,1150,250,235,310,'bronze')
    shape('Buddha_topknot','Sphere',bx,by+10,1315,110,110,100,'bronze')
    for side in [-1,1]:
        shape('Buddha_arm','Sphere',bx+side*205,by-25,705,155,185,390,'bronze')
        shape('Buddha_hand','Sphere',bx+side*145,by-185,570,150,130,85,'bronze')
        shape('Buddha_ear','Sphere',bx+side*132,by,1110,55,80,180,'bronze')
    for x in [-9850,-7550]:
        shape('Incense_bowl','Cylinder',x,5300,190,200,200,260,'bronze',True)
        for dx in [-35,0,35]:shape('Incense_stick','Cylinder',x+dx,5300,390,8,8,180,'wood')
    box('Lotus_pool_border',-10500,4800,90,1100,1300,130,'stone')
    shape('Lotus_pool','Cube',-10500,4800,159,970,1170,8,'water')
    for dx,dy in [(-230,260),(220,-280),(160,330)]:
        shape('Lotus_leaf','Cylinder',-10500+dx,4800+dy,171,170,170,8,'roof')
        shape('Lotus_flower','Sphere',-10500+dx,4800+dy,185,80,80,45,'pink')
    for x,y in [(-9450,3100),(-7850,3100),(-9500,6100),(-7900,6100)]:
        shape('Lantern_post','Cylinder',x,y,210,25,25,360,'wood',True)
        shape('Lantern','Cylinder',x,y,425,80,80,95,'lamp');roof('Lantern_cap',x,y,475,130,130,40)
        if day=='Night':
            a=A.spawn_actor_from_class(u.PointLight,V(x,y,450));a.set_actor_label('Temple_Warm_light');a.set_folder_path('Temple')
            c=a.light_component;c.set_mobility(u.ComponentMobility.MOVABLE);c.set_editor_property('intensity',110);c.set_editor_property('attenuation_radius',1400);c.set_editor_property('cast_shadows',False);c.set_light_color(u.LinearColor(1,.57,.24))
    world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
    gate=u.SystemLibrary.line_trace_single(world,V(-8650,2900,180),V(-8650,4000,180),u.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[],u.DrawDebugTrace.NONE,True)
    assert gate is None,'Temple gate blocked'
    assert L.save_current_level();report.append({'map':day,'removed':removed,'gate_clear':True,'backup':backup,'statue':'stylized blockout placeholder'})
u.EditorAssetLibrary.save_directory('/Game/Jangan',True,True)
with open(os.path.join(ROOT,'temple_report.json'),'w',encoding='utf-8') as f:json.dump(report,f,indent=2)
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(V(0,-18000,9500),u.Rotator(pitch=-20,yaw=90,roll=0))
u.log('TEMPLE_SAVED '+str(report))
