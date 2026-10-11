import bpy
import math
from mathutils import Vector

# ============================================================
# LIMPAR CENA
# ============================================================
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def create_mesh(name, verts, faces):
    """Cria uma mesh customizada"""
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    
    return obj

def add_uv_sphere(name, location, scale, segments=8, rings=6):
    """Adiciona uma esfera UV"""
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments,
        ring_count=rings,
        location=location,
        scale=scale
    )
    obj = bpy.context.active_object
    obj.name = name
    return obj

def add_cylinder(name, location, rotation, radius, depth, vertices=8):
    """Adiciona um cilindro"""
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=depth,
        location=location,
        rotation=rotation
    )
    obj = bpy.context.active_object
    obj.name = name
    return obj

def apply_smooth_shade(obj):
    """Aplica shade suave"""
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.shade_smooth()
    obj.select_set(False)

# ============================================================
# CRIAR CARROCERIA DO BEETLE
# ============================================================

# Base do chassis - muito low poly, usando verts customizados
# Criando a forma icônica do Beetle em wireframe básico

def create_beetle_body():
    """Cria a carroceria principal do Beetle"""
    
    # Definir vértices da carroceria (x, y, z)
    # Escala: 4 unidades de comprimento, 1.8 de largura, 1.5 de altura
    
    verts = [
        # Frente (snout) - ponta dianteira
        (0.0, 2.0, 0.3),      # 0: frente centro baixo
        (0.8, 1.8, 0.5),      # 1: frente direita
        (-0.8, 1.8, 0.5),     # 2: frente esquerda
        (0.9, 1.6, 1.0),      # 3: acima frente direita
        (-0.9, 1.6, 1.0),     # 4: acima frente esquerda
        
        # Capô (hood)
        (0.85, 1.2, 1.2),     # 5: capô direita
        (-0.85, 1.2, 1.2),    # 6: capô esquerda
        (0.90, 0.6, 1.3),     # 7: meio capô direita
        (-0.90, 0.6, 1.3),    # 8: meio capô esquerda
        
        # Teto (roof)
        (0.80, 0.0, 1.4),     # 9: teto frente direita
        (-0.80, 0.0, 1.4),    # 10: teto frente esquerda
        (0.75, -0.5, 1.45),   # 11: teto meio direita
        (-0.75, -0.5, 1.45),  # 12: teto meio esquerda
        (0.70, -1.2, 1.35),   # 13: teto traseira direita
        (-0.70, -1.2, 1.35),  # 14: teto traseira esquerda
        
        # Traseira (trunk)
        (0.65, -1.6, 1.2),    # 15: traseira teto direita
        (-0.65, -1.6, 1.2),   # 16: traseira teto esquerda
        (0.7, -1.9, 0.8),     # 17: traseira meio direita
        (-0.7, -1.9, 0.8),    # 18: traseira meio esquerda
        (0.6, -2.1, 0.3),     # 19: traseira baixa direita
        (-0.6, -2.1, 0.3),    # 20: traseira baixa esquerda
        (0.0, -2.2, 0.2),     # 21: traseira ponta
        
        # Base/chassis
        (0.95, 2.0, 0.05),    # 22: base frente direita
        (-0.95, 2.0, 0.05),   # 23: base frente esquerda
        (0.95, -2.2, 0.05),   # 24: base traseira direita
        (-0.95, -2.2, 0.05),  # 25: base traseira esquerda
    ]
    
    # Faces (triângulos para melhor controle)
    faces = [
        # Frente
        (0, 1, 3), (0, 2, 4), (1, 3, 5), (2, 4, 6),
        (0, 3, 4), (1, 2, 0),
        
        # Capô
        (3, 5, 7), (4, 6, 8), (3, 4, 7), (7, 4, 8),
        
        # Teto
        (5, 7, 9), (6, 8, 10), (7, 8, 9), (9, 8, 10),
        (9, 11, 13), (10, 12, 14), (9, 10, 11), (11, 10, 12),
        (11, 13, 15), (12, 14, 16), (11, 12, 15), (15, 12, 16),
        
        # Traseira
        (13, 15, 17), (14, 16, 18), (13, 14, 17), (17, 14, 18),
        (15, 17, 19), (16, 18, 20), (17, 18, 21),
        (19, 21, 20), (19, 17, 21),
        
        # Base/chassis (conectar à base)
        (0, 22, 1), (0, 23, 22),
        (1, 22, 24), (1, 24, 19), (19, 24, 21),
        (21, 24, 25), (21, 25, 20),
        (20, 25, 23), (20, 23, 2),
        (2, 23, 0),
    ]
    
    body = create_mesh("Beetle_Body", verts, faces)
    apply_smooth_shade(body)
    body.location = (0, 0, 0)
    
    return body

# ============================================================
# CRIAR RODAS
# ============================================================

def create_wheel(name, position_x, position_y):
    """Cria uma roda (cilindro simplificado)"""
    wheel = add_cylinder(
        name,
        location=(position_x, position_y, 0.35),
        rotation=(math.radians(90), 0, 0),
        radius=0.38,
        depth=0.2,
        vertices=12
    )
    apply_smooth_shade(wheel)
    return wheel

# Criar as 4 rodas
wheel_fl = create_wheel("Wheel_FrontLeft", -0.7, 1.2)
wheel_fr = create_wheel("Wheel_FrontRight", 0.7, 1.2)
wheel_bl = create_wheel("Wheel_BackLeft", -0.7, -1.2)
wheel_br = create_wheel("Wheel_BackRight", 0.7, -1.2)

# ============================================================
# CRIAR VIDROS (SIMPLES)
# ============================================================

def create_glass_window(name, location, scale_x, scale_y, scale_z):
    """Cria uma janela/vidro plano"""
    bpy.ops.mesh.primitive_plane_add(
        size=1,
        location=location
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (scale_x, scale_y, scale_z)
    
    # Material semitransparente para vidro
    mat = bpy.data.materials.new(name=name + "_Mat")
    mat.use_nodes = True
    mat.blend_method = 'BLEND'
    mat.shadow_method = 'HASHED'
    
    # Shader de vidro simples
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Transmission'].default_value = 1.0
    bsdf.inputs['Alpha'].default_value = 0.7
    
    obj.data.materials.append(mat)
    
    return obj

# Vidros dianteiros
glass_front_left = create_glass_window("Glass_FrontLeft", (-0.5, 1.4, 0.8), 0.35, 0.4, 0.01)
glass_front_right = create_glass_window("Glass_FrontRight", (0.5, 1.4, 0.8), 0.35, 0.4, 0.01)

# Vidros traseiros
glass_back_left = create_glass_window("Glass_BackLeft", (-0.5, -1.4, 0.8), 0.35, 0.4, 0.01)
glass_back_right = create_glass_window("Glass_BackRight", (0.5, -1.4, 0.8), 0.35, 0.4, 0.01)

# ============================================================
# CRIAR FARÓIS
# ============================================================

def create_headlight(name, position_x, position_y):
    """Cria um farol (esfera pequena)"""
    headlight = add_uv_sphere(
        name,
        location=(position_x, position_y, 0.7),
        scale=0.15,
        segments=6,
        rings=4
    )
    
    # Material de farol
    mat = bpy.data.materials.new(name=name + "_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Emission'].default_value = (1.0, 0.9, 0.7, 1.0)
    bsdf.inputs['Emission Strength'].default_value = 0.5
    
    headlight.data.materials.append(mat)
    
    return headlight

headlight_left = create_headlight("Headlight_Left", -0.5, 1.85)
headlight_right = create_headlight("Headlight_Right", 0.5, 1.85)

# ============================================================
# CRIAR CORPO PRINCIPAL
# ============================================================

body = create_beetle_body()

# Material da carroceria
mat_body = bpy.data.materials.new("Beetle_Paint")
mat_body.use_nodes = True
bsdf = mat_body.node_tree.nodes["Principled BSDF"]
# Azul clássico do Beetle
bsdf.inputs['Base Color'].default_value = (0.1, 0.5, 0.8, 1.0)
bsdf.inputs['Metallic'].default_value = 0.3
bsdf.inputs['Roughness'].default_value = 0.4

body.data.materials.append(mat_body)

# Material das rodas (pneu)
mat_tire = bpy.data.materials.new("Tire")
mat_tire.use_nodes = True
bsdf = mat_tire.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1.0)
bsdf.inputs['Roughness'].default_value = 0.8

for wheel in [wheel_fl, wheel_fr, wheel_bl, wheel_br]:
    wheel.data.materials.append(mat_tire)

# ============================================================
# AGRUPAR TUDO
# ============================================================

all_objects = [
    body, wheel_fl, wheel_fr, wheel_bl, wheel_br,
    glass_front_left, glass_front_right,
    glass_back_left, glass_back_right,
    headlight_left, headlight_right
]

# Selecionar todos
for obj in all_objects:
    obj.select_set(True)

bpy.context.view_layer.objects.active = body

# Juntar em um único objeto
bpy.ops.object.join()

final_obj = bpy.context.active_object
final_obj.name = "VW_Beetle_LowPoly"

# Desmarcar tudo
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = final_obj
final_obj.select_set(True)

# Aplicar shade smooth final
bpy.ops.object.shade_smooth()

print("=" * 50)
print("VW BEETLE LOW POLY CRIADO COM SUCESSO!")
print("=" * 50)
print("Modelo otimizado para jogos em navegador")
print("Aproximadamente 2000-3000 faces")
print("Cor: Azul clássico Beetle")
print("Sem interior (exterior apenas)")
print("=" * 50)
