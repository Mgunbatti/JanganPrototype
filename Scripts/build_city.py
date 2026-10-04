"""Run with UnrealEditor-Cmd -run=pythonscript -script=<this file>."""
import unreal as u
import math
import os
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = '/Game/Jangan'
FORCE_REIMPORT = False  # Set True after editing the procedural mesh geometry.
assets = u.AssetToolsHelpers.get_asset_tools()
actors = u.get_editor_subsystem(u.EditorActorSubsystem)
levels = u.get_editor_subsystem(u.LevelEditorSubsystem)
V = u.Vector
def R(pitch=0,yaw=0,roll=0):
    return u.Rotator(pitch=pitch,yaw=yaw,roll=roll)

def material(name, color, metal=0, rough=.65, glow=0, unlit=False):
    path = OUT + '/Materials/' + name
    m = u.load_asset(path)
    if m:
        return m
    m = assets.create_asset(name, OUT + '/Materials', u.Material, u.MaterialFactoryNew())
    m.set_editor_property('two_sided', True)
    if unlit:
        m.set_editor_property('shading_model', u.MaterialShadingModel.MSM_UNLIT)
    lib = u.MaterialEditingLibrary
    c = lib.create_material_expression(m, u.MaterialExpressionConstant3Vector, -400, 0)
    c.set_editor_property('constant', u.LinearColor(*color, 1))
    lib.connect_material_property(c, '', u.MaterialProperty.MP_EMISSIVE_COLOR if unlit else u.MaterialProperty.MP_BASE_COLOR)
    for prop, val in [(u.MaterialProperty.MP_METALLIC, metal), (u.MaterialProperty.MP_ROUGHNESS, rough)]:
        n = lib.create_material_expression(m, u.MaterialExpressionConstant, -300, 150)
        n.set_editor_property('r', val)
        lib.connect_material_property(n, '', prop)
    if glow and not unlit:
        e = lib.create_material_expression(m, u.MaterialExpressionConstant3Vector, -400, 300)
        e.set_editor_property('constant', u.LinearColor(*(x * glow for x in color), 1))
        lib.connect_material_property(e, '', u.MaterialProperty.MP_EMISSIVE_COLOR)
    lib.recompile_material(m)
    u.EditorAssetLibrary.save_loaded_asset(m)
    return m

M = {
    'stone': material('M_WarmLimestone', (.34,.28,.20)),
    'wall': material('M_IvoryPlaster', (.57,.43,.27)),
    'red': material('M_CinnabarWood', (.40,.032,.018)),
    'roof': material('M_JadeRoof', (.025,.16,.12), .2, .38),
    'gold': material('M_ImperialGold', (.83,.49,.085), .72, .26),
    'dark': material('M_DarkTimber', (.10,.052,.029)),
    'ground': material('M_Earth', (.19,.22,.12)),
    'road': material('M_StonePaving', (.31,.28,.22)),
    'leaf': material('M_JadeFoliage', (.06,.22,.095)),
    'pink': material('M_Blossom', (.68,.22,.28)),
    'water': material('M_JadeWater', (.015,.19,.22), .35, .18),
    'lamp': material('M_LanternGlow', (.95,.24,.035), 0, .4, 3),
    'blue': material('M_IndigoCloth', (.045,.08,.25)),
    'skyday': material('M_DaySky', (.30,.48,.68), unlit=True),
    'skynight': material('M_NightSky', (.008,.015,.045), unlit=True),
}

class Mesh:
    def __init__(self): self.v, self.f = [], []
    def vert(self, p): self.v.append(p); return len(self.v)
    def face(self, *ids): self.f.append(ids)
    def ellipsoid(self, center, scale, rings=10, sides=16):
        start = len(self.v)
        for i in range(rings+1):
            a = math.pi*i/rings
            for j in range(sides):
                b = math.tau*j/sides
                self.vert(tuple(center[k] + scale[k]*q for k,q in enumerate((math.sin(a)*math.cos(b),math.sin(a)*math.sin(b),math.cos(a)))))
        for i in range(rings):
            for j in range(sides):
                a=start+i*sides+j+1; b=start+i*sides+(j+1)%sides+1
                self.face(a,b,b+sides); self.face(a,b+sides,a+sides)
    def tube(self, pts, radii, sides=12):
        start=len(self.v)
        for i,p in enumerate(pts):
            prev=pts[max(0,i-1)]; nxt=pts[min(len(pts)-1,i+1)]
            d=[nxt[k]-prev[k] for k in range(3)]
            l=math.sqrt(sum(x*x for x in d)); d=[x/l for x in d]
            ref=(0,0,1) if abs(d[2])<.9 else (1,0,0)
            n=[d[1]*ref[2]-d[2]*ref[1],d[2]*ref[0]-d[0]*ref[2],d[0]*ref[1]-d[1]*ref[0]]
            l=math.sqrt(sum(x*x for x in n)); n=[x/l for x in n]
            b=[d[1]*n[2]-d[2]*n[1],d[2]*n[0]-d[0]*n[2],d[0]*n[1]-d[1]*n[0]]
            for j in range(sides):
                a=math.tau*j/sides
                self.vert(tuple(p[k]+radii[i]*(n[k]*math.cos(a)+b[k]*math.sin(a)) for k in range(3)))
        for i in range(len(pts)-1):
            for j in range(sides):
                a=start+i*sides+j+1; b=start+i*sides+(j+1)%sides+1
                self.face(a,b,b+sides); self.face(a,b+sides,a+sides)
        self.face(*reversed(tuple(start+j+1 for j in range(sides))))
        self.face(*(start+(len(pts)-1)*sides+j+1 for j in range(sides)))
    def save(self,name):
        path=os.path.join(ROOT,'SourceAssets',name+'.obj')
        with open(path,'w') as f:
            f.write('o '+name+'\n')
            # UE 5.8 Interchange OBJ importer flips the source Y axis.
            for x,y,z in self.v: f.write('v %.5f %.5f %.5f\n'%(x,-y,z))
            for x,y,z in self.v: f.write('vt %.5f %.5f\n'%(x/2000,y/2000))
            for ids in self.f: f.write('f '+' '.join('%d/%d'%(i,i) for i in ids)+'\n')
        return path

def import_mesh(mesh,name):
    path=OUT+'/Meshes/'+name
    existing=u.load_asset(path)
    if existing and not FORCE_REIMPORT:
        return existing
    t=u.AssetImportTask()
    t.filename=mesh.save(name); t.destination_path=OUT+'/Meshes'; t.destination_name=name
    t.automated=True; t.save=True; t.replace_existing=True
    opt=u.FbxImportUI(); opt.import_mesh=True; opt.import_materials=False; opt.import_textures=False
    opt.import_as_skeletal=False
    opt.static_mesh_import_data.set_editor_property('generate_lightmap_u_vs',False)
    opt.static_mesh_import_data.set_editor_property('auto_generate_collision',True)
    t.options=opt
    assets.import_asset_tasks([t])
    result=u.load_asset(path)
    if not result: raise RuntimeError('Mesh import failed: '+name+' '+str(t.imported_object_paths))
    return result

# Curved hip roof with an elevated ridge and turned-up eaves, reusable at every scale.
roof=Mesh()
for ring in range(6):
    t=ring/5
    hx=50*(1-.78*t); hy=50*(1-.97*t)
    for x,y in [(-hx,-hy),(hx,-hy),(hx,hy),(-hx,hy)]:
        z=30*t**.62 + (6 if ring==0 else 0)
        roof.vert((x,y,z))
for r in range(5):
    for j in range(4):
        a=r*4+j+1; b=r*4+(j+1)%4+1
        roof.face(a,b,b+4); roof.face(a,b+4,a+4)
roof.face(21,22,23,24); roof.face(4,3,2,1)
ROOF=import_mesh(roof,'SM_CurvedHipRoof')

# A long coiling body, muzzle, antler horns, whiskers and four clawed legs.
dragon=Mesh()
pts=[]; radii=[]
for i in range(121):
    t=i/120; a=math.tau*1.55*t
    radius=330*(1-.22*t)
    pts.append((radius*math.cos(a),radius*math.sin(a),100+1250*t))
    radii.append(20+75*math.sin(math.pi*t/2))
dragon.tube(pts,radii,16)
hx,hy,hz=pts[-1]
dragon.ellipsoid((hx,hy,hz+45),(125,100,95))
dragon.ellipsoid((hx+125,hy,hz+5),(140,68,50))
dragon.ellipsoid((hx+130,hy,hz-52),(125,62,18))
for side in [-1,1]:
    dragon.tube([(hx-35,hy+side*60,hz+100),(hx-90,hy+side*105,hz+230),(hx-45,hy+side*140,hz+330)],[24,17,2])
    dragon.tube([(hx-90,hy+side*105,hz+230),(hx-170,hy+side*130,hz+285)],[14,1])
    dragon.tube([(hx+180,hy+side*60,hz+15),(hx+240,hy+side*160,hz+40),(hx+195,hy+side*270,hz+110)],[10,6,1],8)
for idx in [49,82]:
    x,y,z=pts[idx]
    for side in [-1,1]:
        end=(x+170, y+side*220, z-160)
        dragon.tube([(x,y,z),(x+125,y+side*170,z-30),end],[48,34,20])
        for claw in [-1,0,1]:
            dragon.tube([end,(end[0]+95,end[1]+claw*38,end[2]-20),(end[0]+115,end[1]+claw*42,end[2]-55)],[15,9,1],8)
for i in range(12,115,6):
    x,y,z=pts[i]; a=math.tau*1.55*i/120
    dragon.tube([(x,y,z+65),(x+math.cos(a)*85,y+math.sin(a)*85,z+140)],[24,1],6)
DRAGON=import_mesh(dragon,'SM_GoldenDragon')
dragon_bounds=DRAGON.get_bounds()
if dragon_bounds.box_extent.z < 700 or dragon_bounds.origin.z < 700:
    raise RuntimeError('Dragon import axis validation failed: '+str(dragon_bounds))
roof_bounds=ROOF.get_bounds()
if roof_bounds.origin.z < 0 or roof_bounds.box_extent.z > 30:
    raise RuntimeError('Roof import axis validation failed: '+str(roof_bounds))

meshes={n:u.load_asset('/Engine/BasicShapes/'+n) for n in ['Cube','Cylinder','Sphere','Cone']}
count=0
def shape(name,mesh,loc,scale,mat,rot=(0,0,0),folder='Architecture',collision=True):
    global count
    a=actors.spawn_actor_from_class(u.StaticMeshActor,V(*loc),R(*rot))
    a.set_actor_label(name)
    a.set_folder_path(folder)
    c=a.static_mesh_component
    c.set_static_mesh(meshes.get(mesh,mesh))
    c.set_material(0,M[mat]); c.set_mobility(u.ComponentMobility.STATIC)
    a.set_actor_scale3d(V(*scale))
    if collision:
        c.set_collision_profile_name('BlockAll')
        c.set_collision_enabled(u.CollisionEnabled.QUERY_AND_PHYSICS)
        a.set_actor_enable_collision(True)
    else:
        c.set_collision_profile_name('NoCollision')
        c.set_collision_enabled(u.CollisionEnabled.NO_COLLISION)
        a.set_actor_enable_collision(False)
    count+=1
    return a
def box(name,x,y,z,sx,sy,sz,mat,folder='Architecture'):
    return shape(name,'Cube',(x,y,z),(sx/100,sy/100,sz/100),mat,folder=folder)
def cyl(name,x,y,z,r,h,mat,folder='Architecture',collision=True):
    return shape(name,'Cylinder',(x,y,z),(r/50,r/50,h/100),mat,folder=folder,collision=collision)
def roof_at(name,x,y,z,w,d,h=500):
    shape(name,ROOF,(x,y,z),(w/100,d/100,h/30),'roof',collision=False)
    box(name+'_ridge',x,y,z+h,w*.22,35,35,'gold')
def hall(name,x,y,w,d,height=700,base=0,palace=False):
    box(name+'_foundation',x,y,base+60,w+150,d+150,120,'stone')
    box(name+'_plaster',x,y,base+height/2,w*.92,d*.86,height,'wall')
    for xx in [-w*.43,0,w*.43]:
        for yy in [-d*.46,d*.46]:
            cyl(name+'_red_column',x+xx,y+yy,base+height/2+120,32,height,'red')
    for xx in [-w*.3,0,w*.3]:
        box(name+'_door',x+xx,y-d*.435-4,base+210,170,20,300,'dark')
        box(name+'_lintel',x+xx,y-d*.46,base+390,200,25,30,'gold')
    box(name+'_beam',x,y,base+height,w,d,70,'red')
    roof_at(name+'_roof',x,y,base+height+50,w+300,d+300,450 if not palace else 620)
    if palace:
        roof_at(name+'_upper_roof',x,y,base+height+560,w*.74,d*.72,440)

def lantern(x,y,z=340):
    cyl('Lantern_post',x,y,z/2,12,z,'dark','Lanterns')
    cyl('Red_lantern',x,y,z,38,85,'lamp','Lanterns',False)
    roof_at('Lantern_cap',x,y,z+60,110,110,35)

def tree(x,y,pink=False):
    cyl('Tree_trunk',x,y,210,28,420,'dark','Gardens')
    shape('Tree_crown','Sphere',(x,y,530),(4.7,4.4,4.8),'pink' if pink else 'leaf',folder='Gardens',collision=False)
    shape('Tree_crown_small','Sphere',(x+180,y-50,460),(3.7,3.3,3.4),'pink' if pink else 'leaf',folder='Gardens',collision=False)

def build(night=False):
    global count
    count=0
    path=OUT+'/Maps/Jangan_'+('Night' if night else 'Day')
    if u.EditorAssetLibrary.does_asset_exist(path):
        if not levels.load_level(path): raise RuntimeError('Cannot load '+path)
        for a in actors.get_all_level_actors():
            if isinstance(a,(u.StaticMeshActor,u.Light,u.PlayerStart,u.CameraActor)):
                actors.destroy_actor(a)
    elif not levels.new_level(path):
        raise RuntimeError('Cannot create '+path)
    box('City_ground',0,0,-70,60000,60000,100,'ground','Ground')
    box('City_stone_platform',0,1000,-15,26000,28000,80,'stone','Ground')
    box('Imperial_avenue',0,-2000,30,1800,21000,22,'road','Ground')
    box('East_west_avenue',0,500,32,24000,1400,22,'road','Ground')
    cyl('Central_square',0,500,45,3300,30,'road','Monument')
    cyl('Dragon_outer_dais',0,500,115,1100,140,'stone','Monument')
    cyl('Dragon_gold_band',0,500,195,850,35,'gold','Monument')
    cyl('Dragon_inner_plinth',0,500,280,650,150,'dark','Monument')
    shape('GOLDEN_DRAGON',DRAGON,(0,500,355),(1,1,1),'gold',folder='Monument',collision=False)
    # Small eyes and the pearl held above the square.
    cyl('Monument_core',0,500,650,115,650,'stone','Monument')
    shape('Dragon_pearl','Sphere',(500,350,1700),(1.7,1.7,1.7),'lamp',folder='Monument',collision=False)
    for xx in [-950,950]:
        for yy in [-450,1450]:
            cyl('Guardian_obelisk',xx,yy,240,55,400,'red','Monument')
            shape('Obelisk_finial','Sphere',(xx,yy,475),(.85,.85,.85),'gold',folder='Monument')
    # The fortified perimeter leaves a broad entrance opening.
    for x in [-13000,13000]:
        box('City_wall',x,1000,470,240,28000,940,'wall','Fortifications')
    box('North_wall',0,15000,470,26000,240,940,'wall','Fortifications')
    for x in [-7600,7600]: box('South_wall',x,-13000,470,10800,240,940,'wall','Fortifications')
    for x in [-13000,13000]:
        for y in [-13000,15000]: hall('Corner_watchtower',x,y,1000,1000,1100)
    for x in [-1800,1800]:
        box('Gate_stone_pier',x,-12800,650,1000,1400,1300,'stone','Fortifications')
    box('Gate_overpass',0,-12800,1350,4700,1500,300,'red','Fortifications')
    roof_at('Jangan_South_Gate',0,-12800,1520,5300,2000,650)
    roof_at('Jangan_Gate_upper',0,-12800,2100,3400,1400,500)
    # Palace terrace and walkable stairs; 15cm rises.
    box('Daming_terrace',0,10300,250,10600,6800,500,'stone','Palace')
    for i in range(32):
        box('Palace_stair_%02d'%i,0,6300+i*32,(i+1)*15/2,2200,40,(i+1)*15,'stone','Palace')
    hall('DAMING_MAIN_HALL',0,10800,5700,2800,1000,500,True)
    for x in [-3900,3900]: hall('Daming_side_hall',x,9300,1600,2400,700,500)
    for x in [-3800,-2200,2200,3800]:
        cyl('Terrace_ceremonial_column',x,7400,850,45,700,'red','Palace')
    # Mixed-scale market and residential blocks.
    for x in [-8100,-4700,4700,8100]:
        for y in [-8300,-4600,3800]:
            hall('Courtyard_house',x,y,1800,1500,550)
            box('Courtyard_back_wall',x,y+1700,170,2100,60,340,'wall')
            for dx in [-1000,1000]: box('Courtyard_side_wall',x+dx,y+1050,170,60,1300,340,'wall')
            tree(x+650,y+1050,True)
    for side in [-1,1]:
        for i in range(6):
            x=side*(3500+i*1100); y=-1700
            box('Market_counter',x,y,75,620,330,150,'dark','Market')
            for dx in [-290,290]: cyl('Market_post',x+dx,y,180,10,360,'dark','Market')
            box('Silk_canopy',x,y,360,740,520,25,'red' if i%2 else 'blue','Market')
            for dx in [-160,0,160]: shape('Trade_bale','Cube',(x+dx,y,180),(1.3,1.6,.75),'gold' if i%2 else 'blue',folder='Market')
    # Eastern garden with a bridge across a shallow ornamental pond.
    box('Garden_pond',8600,6500,25,3400,2300,30,'water','Gardens')
    box('Garden_bridge',8600,6500,90,700,2600,130,'dark','Gardens')
    for dx in [-380,380]:
        box('Bridge_rail',8600+dx,6500,200,30,2600,35,'red','Gardens')
    for x,y in [(6500,5800),(10500,5200),(10800,7700),(6300,7600),(-10200,6200),(-6900,6100)]: tree(x,y,True)
    hall('Garden_pavilion',8600,8500,950,950,440)
    for side in [-1,1]:
        for y in range(-11000,6000,1700): lantern(side*1150,y)
        for x in range(3500,11500,1800): lantern(side*x,1500)
    # Low-poly distant landforms outside the walls.
    for i in range(12):
        a=math.tau*i/12
        shape('Distant_hill','Cone',(math.cos(a)*35000,math.sin(a)*35000,-500),(140,120,55),'ground',folder='Backdrop',collision=False)
    sky=shape('Sky_dome','Sphere',(0,0,0),(1800,1800,1800),'skynight' if night else 'skyday',folder='Lighting',collision=False)
    sky.static_mesh_component.set_editor_property('cast_shadow',False)
    sun=actors.spawn_actor_from_class(u.DirectionalLight,V(0,0,3000),R(-32,-35,0))
    sun.set_actor_label('Moonlight' if night else 'Late_afternoon_sun'); sun.set_folder_path('Lighting')
    sun.light_component.set_mobility(u.ComponentMobility.MOVABLE)
    sun.light_component.set_editor_property('intensity',.7 if night else 3.5)
    sun.light_component.set_light_color(u.LinearColor(.22,.36,.8) if night else u.LinearColor(1,.78,.53))
    sky_light=actors.spawn_actor_from_class(u.SkyLight,V(0,0,2000))
    sky_light.set_folder_path('Lighting')
    sky_light.light_component.set_mobility(u.ComponentMobility.MOVABLE)
    sky_light.light_component.set_editor_property('intensity',1.2 if night else 1.6)
    sky_light.light_component.set_editor_property('lower_hemisphere_is_black',False)
    sky_light.light_component.set_editor_property('sky_distance_threshold',10000)
    sky_light.light_component.recapture_sky()
    if night:
        for x,y in [(-600,-100),(600,1100),(0,1700)]:
            a=actors.spawn_actor_from_class(u.PointLight,V(x,y,500)); a.set_actor_label('Dragon_gold_uplight'); a.set_folder_path('Lighting')
            a.light_component.set_mobility(u.ComponentMobility.MOVABLE)
            a.light_component.set_editor_property('intensity',650)
            a.light_component.set_editor_property('attenuation_radius',2400)
            a.light_component.set_editor_property('cast_shadows',False)
            a.light_component.set_light_color(u.LinearColor(1,.52,.12))
        for side in [-1,1]:
            for y in [-9500,-6000,-2500,3000]:
                a=actors.spawn_actor_from_class(u.PointLight,V(side*1150,y,350))
                a.set_folder_path('Lighting'); a.set_actor_label('Warm_street_light')
                a.light_component.set_mobility(u.ComponentMobility.MOVABLE)
                a.light_component.set_editor_property('intensity',120)
                a.light_component.set_editor_property('attenuation_radius',1000)
                a.light_component.set_editor_property('cast_shadows',False)
                a.light_component.set_light_color(u.LinearColor(1,.35,.08))
    spawn=actors.spawn_actor_from_class(u.PlayerStart,V(0,-10700,150),R(0,90,0))
    spawn.set_actor_label('PlayerStart_SouthGate')
    gm=u.load_class(None,'/Game/ThirdPerson/Blueprints/BP_ThirdPersonGameMode.BP_ThirdPersonGameMode_C')
    if not gm: raise RuntimeError('Third person game mode missing')
    u.EditorLevelLibrary.get_editor_world().get_world_settings().set_editor_property('default_game_mode',gm)
    cam=actors.spawn_actor_from_class(u.CameraActor,V(7400,-11500,6700),R(-23,120,0))
    cam.set_actor_label('City_overview_camera')
    u.EditorLevelLibrary.set_level_viewport_camera_info(V(6200,-9600,4800),R(-19,120,0))
    if not levels.save_current_level():
        raise RuntimeError('Map save failed; close other instances of this project: '+path)
    u.log('JANGAN_MAP_SAVED '+path+' meshes='+str(count))
    return {'map':path,'static_mesh_actors':count}

results=[build(False),build(True)]
if not u.EditorAssetLibrary.save_directory(OUT,only_if_is_dirty=True,recursive=True):
    raise RuntimeError('Asset save failed; close other instances of this project')
with open(os.path.join(ROOT,'build_report.json'),'w') as f:
    json.dump({'maps':results,'dragon_vertices':len(dragon.v),'dragon_faces':len(dragon.f),'dragon_bounds':str(dragon_bounds),'roof_bounds':str(roof_bounds),'game_mode':'BP_ThirdPersonGameMode'},f,indent=2)
u.log('JANGAN_BUILD_COMPLETE')
# Keep side gates and the reviewed lighting when regenerating the prototype.
exec(compile(open(os.path.join(ROOT,'Scripts','add_side_gates.py'),encoding='utf-8').read(),os.path.join(ROOT,'Scripts','add_side_gates.py'),'exec'))
exec(compile(open(os.path.join(ROOT,'Scripts','place_npc_shops.py'),encoding='utf-8').read(),os.path.join(ROOT,'Scripts','place_npc_shops.py'),'exec'))
exec(compile(open(os.path.join(ROOT,'Scripts','build_barracks.py'),encoding='utf-8').read(),os.path.join(ROOT,'Scripts','build_barracks.py'),'exec'))
exec(compile(open(os.path.join(ROOT,'Scripts','build_temple.py'),encoding='utf-8').read(),os.path.join(ROOT,'Scripts','build_temple.py'),'exec'))
exec(compile(open(os.path.join(ROOT,'Scripts','refine_temple_garden.py'),encoding='utf-8').read(),os.path.join(ROOT,'Scripts','refine_temple_garden.py'),'exec'))
exec(compile(open(os.path.join(ROOT,'Scripts','update_legends_monument.py'),encoding='utf-8').read(),os.path.join(ROOT,'Scripts','update_legends_monument.py'),'exec'))
exec(compile(open(os.path.join(ROOT,'Scripts','align_pagoda_garden.py'),encoding='utf-8').read(),os.path.join(ROOT,'Scripts','align_pagoda_garden.py'),'exec'))
exec(compile(open(os.path.join(ROOT,'Scripts','clear_monument_houses.py'),encoding='utf-8').read(),os.path.join(ROOT,'Scripts','clear_monument_houses.py'),'exec'))
exec(compile(open(os.path.join(ROOT,'Scripts','decorate_palace_square.py'),encoding='utf-8').read(),os.path.join(ROOT,'Scripts','decorate_palace_square.py'),'exec'))
exec(compile(open(os.path.join(ROOT,'Scripts','fix_city_contacts.py'),encoding='utf-8').read(),os.path.join(ROOT,'Scripts','fix_city_contacts.py'),'exec'))
exec(compile(open(os.path.join(ROOT,'Scripts','fix_roof_supports.py'),encoding='utf-8').read(),os.path.join(ROOT,'Scripts','fix_roof_supports.py'),'exec'))
exec(compile(open(os.path.join(ROOT,'Scripts','repair_building_assemblies.py'),encoding='utf-8').read(),os.path.join(ROOT,'Scripts','repair_building_assemblies.py'),'exec'))
exec(compile(open(os.path.join(ROOT,'Scripts','remove_roof_cornices.py'),encoding='utf-8').read(),os.path.join(ROOT,'Scripts','remove_roof_cornices.py'),'exec'))
exec(compile(open(os.path.join(ROOT,'Scripts','fix_gate_roofs_and_ridges.py'),encoding='utf-8').read(),os.path.join(ROOT,'Scripts','fix_gate_roofs_and_ridges.py'),'exec'))
exec(compile(open(os.path.join(ROOT,'Scripts','replace_storage_with_chest.py'),encoding='utf-8').read(),os.path.join(ROOT,'Scripts','replace_storage_with_chest.py'),'exec'))
exec(compile(open(os.path.join(ROOT,'Scripts','fix_garden_palace_grounding.py'),encoding='utf-8').read(),os.path.join(ROOT,'Scripts','fix_garden_palace_grounding.py'),'exec'))

