"""Reference-based blockout: west/east shop order, individual stationary NPCs."""
import unreal as u
import os, math, json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A=u.get_editor_subsystem(u.EditorActorSubsystem)
L=u.get_editor_subsystem(u.LevelEditorSubsystem)
V=u.Vector
R=lambda yaw: u.Rotator(pitch=0,yaw=yaw,roll=0)
mesh=u.load_asset('/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple')
idle=u.load_asset('/Game/Characters/Mannequins/Anims/Unarmed/MM_Idle')
assert mesh and idle,'Missing NPC placeholder assets'
rows=[('Blacksmith','Demirci',-3600,-3500,90),('Protector','Zırhçı',-3600,-6500,90),('Stable','Ahır',-3600,-9500,90),
      ('DrugStore','İksirci',3600,-3500,-90),('Grocery','Bakkal',3600,-6500,-90),('Specialty','Özel Eşya',3600,-9500,-90)]

def capture_group(all_actors,x,y):
    parts=[]
    for a in all_actors:
        if not isinstance(a,u.StaticMeshActor): continue
        if not a.get_actor_label().startswith(('Courtyard_house','Courtyard_back_wall','Courtyard_side_wall','Tree_trunk','Tree_crown')): continue
        p=a.get_actor_location()
        if abs(p.x-x)<=1200 and -1100<=p.y-y<=2200:
            parts.append((a,(p.x-x,p.y-y,p.z),a.get_actor_rotation(),a.get_actor_scale3d()))
    return parts

def transform_part(part,role,i,x,y,yaw,duplicate=False):
    src,p,r,scale=part
    angle=math.radians(yaw)
    loc=V(x+p[0]*math.cos(angle)-p[1]*math.sin(angle),y+p[0]*math.sin(angle)+p[1]*math.cos(angle),p[2])
    rot=u.Rotator(pitch=r.pitch,yaw=r.yaw+yaw,roll=r.roll)
    if duplicate:
        a=A.spawn_actor_from_class(u.StaticMeshActor,loc,rot)
        sc=src.static_mesh_component;c=a.static_mesh_component
        c.set_static_mesh(sc.static_mesh)
        for j in range(sc.get_num_materials()): c.set_material(j,sc.get_material(j))
        c.set_mobility(u.ComponentMobility.STATIC)
        solid=str(sc.get_collision_profile_name())!='NoCollision'
        c.set_collision_profile_name('BlockAll' if solid else 'NoCollision')
        c.set_collision_enabled(u.CollisionEnabled.QUERY_AND_PHYSICS if solid else u.CollisionEnabled.NO_COLLISION)
        a.set_actor_enable_collision(solid)
    else:
        a=src;a.set_actor_location(loc,False,False);a.set_actor_rotation(rot,False)
    a.set_actor_scale3d(scale)
    a.set_actor_label('Shop_'+role+'_part_%02d'%i)
    a.set_folder_path('NPC_Shops/'+role)
    return a

def text(label,title,x,y,z,yaw,size):
    a=A.spawn_actor_from_class(u.TextRenderActor,V(x,y,z),R(yaw))
    a.set_actor_label(label);a.set_folder_path('NPC_Shops/Signs')
    c=a.text_render;c.set_text(title);c.set_world_size(size)
    c.set_horizontal_alignment(u.HorizTextAligment.EHTA_CENTER)
    c.set_text_render_color(u.Color(245,207,115,255))
    a.set_actor_enable_collision(False)

def npc(role,title,x,y,yaw,z=30):
    a=A.spawn_actor_from_class(u.SkeletalMeshActor,V(x,y,z),R(yaw))
    a.set_actor_label('NPC_'+role);a.set_folder_path('NPC_Shops/NPCs')
    c=a.skeletal_mesh_component;c.set_skeletal_mesh_asset(mesh)
    c.set_mobility(u.ComponentMobility.MOVABLE)
    c.set_animation_mode(u.AnimationMode.ANIMATION_SINGLE_NODE)
    c.override_animation_data(idle,True,True,0.0,1.0)
    c.set_collision_profile_name('NoCollision');a.set_actor_enable_collision(False)
    # NPC mesh faces +Y; rotate to face the road.
    a.set_actor_rotation(R(yaw-90),False)
    c.set_editor_property('visibility_based_anim_tick_option',u.VisibilityBasedAnimTickOption.ONLY_TICK_POSE_WHEN_RENDERED)
    text('NPC_Name_'+role,title,x,y,z+230,yaw,55)
    return a

reports=[]
L.save_current_level()
for day in ['Night','Day']:
    assert L.load_level('/Game/Jangan/Maps/Jangan_'+day)
    all_actors=list(A.get_all_level_actors())
    labels={a.get_actor_label() for a in all_actors}
    groups={(side,row):capture_group(all_actors,side*4700,row) for side in [-1,1] for row in [-4600,-8300]}
    # Clone the third storefront before moving the two existing buildings.
    for side,role in [(-1,'Stable'),(1,'Specialty')]:
        if 'Shop_'+role+'_part_00' in labels: continue
        assert len(groups[(side,-4600)])>=15,'Shop seed not found'
        for i,part in enumerate(groups[(side,-4600)]): transform_part(part,role,i,side*3600,-9500,-side*90,True)
    for role,title,x,y,yaw in rows:
        if role not in ['Stable','Specialty'] and 'Shop_'+role+'_part_00' not in labels:
            side=-1 if x<0 else 1
            old_y=-4600 if y==-3500 else -8300
            for i,part in enumerate(groups[(side,old_y)]): transform_part(part,role,i,x,y,yaw)
        if 'NPC_'+role not in labels:
            # Threshold is 645cm from hall center after rotation; NPC stands on street side.
            nx=x+(1050 if x<0 else -1050)
            npc(role,title,nx,y,0 if x<0 else 180)
            text('Shop_Sign_'+role,title,x+(680 if x<0 else -680),y,490,0 if x<0 else 180,90)
    # A small dedicated depot southwest of the monument, as in the supplied layout.
    if 'Shop_Storage_part_00' not in labels:
        seed=next(a for a in all_actors if a.get_actor_label().startswith('Garden_pavilion_foundation'))
        sx=seed.get_actor_location().x;sy=seed.get_actor_location().y
        parts=[]
        for a in all_actors:
            if isinstance(a,u.StaticMeshActor) and a.get_actor_label().startswith('Garden_pavilion'):
                p=a.get_actor_location();parts.append((a,(p.x-sx,p.y-sy,p.z),a.get_actor_rotation(),a.get_actor_scale3d()))
        for i,part in enumerate(parts): transform_part(part,'Storage',i,-2050,-1200,90,True)
        npc('Storage','Depocu',-1300,-1200,0)
        text('Shop_Sign_Storage','Depo',-1580,-1200,420,0,90)
    # Extra reference landmarks reuse existing buildings instead of growing the city.
    for role,title,x,y in [('Gambling','Oyun Evi',8100,-4600),('HunterAssociation','Avcı Birliği',-8100,3800)]:
        if 'NPC_'+role in labels: continue
        parts=capture_group(all_actors,x,y)
        for i,part in enumerate(parts): transform_part(part,role,i,x,y,0)
        npc(role,title,x,y-1100,-90)
        text('Shop_Sign_'+role,title,x,y-660,490,-90,80)
    if 'NPC_LegendsGate' not in labels:
        # Dedicated small pavilion northeast of the central dragon.
        seed_parts=[]
        for a in all_actors:
            if isinstance(a,u.StaticMeshActor) and a.get_actor_label().startswith('Garden_pavilion'):
                p=a.get_actor_location();seed_parts.append((a,(p.x-8600,p.y-8500,p.z),a.get_actor_rotation(),a.get_actor_scale3d()))
        for i,part in enumerate(seed_parts): transform_part(part,'LegendsGate',i,2350,2100,0,True)
        npc('LegendsGate','Legends Gate',2350,1350,-90)
        text('Shop_Sign_LegendsGate','Legends Gate',2350,1650,420,-90,70)
    for a in A.get_all_level_actors():
        if isinstance(a,u.SkeletalMeshActor) and a.get_actor_label().startswith('NPC_'):
            a.skeletal_mesh_component.override_animation_data(idle,True,True,0.0,1.0)
    assert L.save_current_level()
    current=list(A.get_all_level_actors())
    reports.append({'map':day,'npcs':[{'role':a.get_actor_label(),'location':str(a.get_actor_location())} for a in current if a.get_actor_label().startswith('NPC_') and isinstance(a,u.SkeletalMeshActor)],'shop_parts':sum(a.get_actor_label().startswith('Shop_') and isinstance(a,u.StaticMeshActor) for a in current)})
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(V(15000,-17000,12500),u.Rotator(pitch=-31,yaw=131,roll=0))
with open(os.path.join(ROOT,'npc_layout_report.json'),'w',encoding='utf-8') as f: json.dump(reports,f,ensure_ascii=False,indent=2)
u.log('NPC_SHOP_LAYOUT_SAVED '+str(reports))
exec(compile(open(os.path.join(ROOT,'Scripts','mirror_npc_layout.py'),encoding='utf-8').read(),os.path.join(ROOT,'Scripts','mirror_npc_layout.py'),'exec'))
