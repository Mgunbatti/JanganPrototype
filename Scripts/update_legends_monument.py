"""Clear bridge approaches, enlarge pagoda, move Buddha to Legends Gate."""
import unreal as u,os,json,math
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
source=open(os.path.join(ROOT,'Scripts','build_temple.py'),encoding='utf-8').read()
exec(compile(source.split('L.save_current_level();report=[]')[0],__file__,'exec'))
p='/Game/Jangan/Materials'; glow=u.load_asset(p+'/M_LegendsMysticGlow')
if not glow:
    glow=u.AssetToolsHelpers.get_asset_tools().create_asset('M_LegendsMysticGlow',p,u.Material,u.MaterialFactoryNew())
    glow.set_editor_property('shading_model',u.MaterialShadingModel.MSM_UNLIT)
    n=u.MaterialEditingLibrary.create_material_expression(glow,u.MaterialExpressionConstant3Vector,-300,0)
    n.set_editor_property('constant',u.LinearColor(.12,1.8,2.8,1));u.MaterialEditingLibrary.connect_material_property(n,'',u.MaterialProperty.MP_EMISSIVE_COLOR)
    u.MaterialEditingLibrary.recompile_material(glow);u.EditorAssetLibrary.save_loaded_asset(glow)
M['mystic']=glow
tag=u.Name('LegendsMonumentV1');reports=[];L.save_current_level()
for day in ['Night','Day']:
    path='/Game/Jangan/Maps/Jangan_'+day;assert L.load_level(path)
    current=list(A.get_all_level_actors())
    if any(tag in a.tags for a in current):continue
    backup='/Game/Jangan/Backups/Jangan_'+day+'_BeforeLegendsMonument'
    if not u.EditorAssetLibrary.does_asset_exist(backup):assert u.EditorAssetLibrary.duplicate_asset(path,backup)
    removed=[];moved=0
    for a in current:
        n=a.get_actor_label();v=a.get_actor_location();s=a.get_actor_scale3d()
        if n.startswith('Shop_LegendsGate_'):
            removed.append(n);A.destroy_actor(a);continue
        if n=='Shop_Sign_LegendsGate':
            a.set_actor_location(V(-2350,1500,500),False,False)
        if n.startswith(('Temple_Buddha','Temple_Lotus_plinth','Temple_Lotus_gold_band','Temple_Lotus_petal','Temple_Incense')):
            a.set_actor_location(V(v.x+6350,v.y-3600,v.z),False,False)
            a.set_actor_label(n.replace('Temple_','Legends_'));a.set_folder_path('LegendsGate');moved+=1
        elif n.startswith('Temple_Pagoda'):
            a.set_actor_location(V(-7500+(v.x+7500)*1.15,8300+(v.y-8300)*1.15,25+(v.z-25)*1.1),False,False)
            a.set_actor_scale3d(V(s.x*1.15,s.y*1.15,s.z*1.1))
        elif n.startswith(('Temple_Organic','Temple_Shore','Temple_Lotus_leaf','Temple_Lotus_flower')):
            a.set_actor_location(V(v.x+500,v.y,v.z),False,False)
        elif n.startswith('Temple_Bridge'):
            a.set_actor_location(V(-9800+(v.x+10300)*.8,v.y,v.z),False,False)
            a.set_actor_scale3d(V(s.x*.8,s.y,s.z))
    # Mystic halo sits behind the seated statue; all energy decorations have no collision.
    for i in range(48):
        t=i*math.tau/48
        a=shape('Legends_aura','Sphere',-2350+710*math.cos(t),2310,860+710*math.sin(t),45,30,45,'mystic')
        a.set_actor_label('Legends_Mystic_halo');a.set_folder_path('LegendsGate');a.tags=[tag]
    for side in [-1,1]:
        a=shape('Legends_orb','Sphere',-2350+side*780,1900,400,120,120,120,'mystic');a.set_actor_label('Legends_Energy_orb');a.set_folder_path('LegendsGate')
    world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
    # Verify the full walking lane with rays above each tread; railings stay outside the lane.
    checks=[]
    for i in range(26):
        x1=-10840+i*80;x2=x1+80;z=65+min(i,26-i,8)*14+230
        hit=u.SystemLibrary.line_trace_single(world,V(x1,6650,z),V(x2,6650,z),u.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[],u.DrawDebugTrace.NONE,True)
        assert hit is None,'Bridge walking lane obstructed at '+str(i)
        checks.append(i)
    for x in [-11000,-8600]:
        hit=u.SystemLibrary.line_trace_single(world,V(x,6650,400),V(x,6650,-100),u.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[],u.DrawDebugTrace.NONE,True)
        assert hit is not None,'Bridge approach missing floor'
    assert L.save_current_level();reports.append({'map':day,'removed_gate_parts':removed,'moved_statue_parts':moved,'bridge_lane_clear':len(checks),'approaches_have_floor':True,'backup':backup,'teleport':'visual only; destination not yet configured'})
u.EditorAssetLibrary.save_directory('/Game/Jangan',True,True)
with open(os.path.join(ROOT,'legends_monument_report.json'),'w',encoding='utf-8') as f:json.dump(reports,f,indent=2)
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(V(-15000,-1500,7000),u.Rotator(pitch=-29,yaw=52,roll=0))
u.log('LEGENDS_MONUMENT_SAVED')
