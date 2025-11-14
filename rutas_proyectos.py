from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_proyectos = Blueprint("rutas_proyectos", __name__)

API_URL = "http://localhost:5031/api/proyecto"
API_RESPONSABLES = "http://localhost:5031/api/responsable"
API_TIPO_PROYECTO = "http://localhost:5031/api/tipo_proyecto"
API_META_PROYECTO = "http://localhost:5031/api/meta_proyecto"
API_ESTADO_PROYECTO = "http://localhost:5031/api/estado_proyecto"
API_METAS = "http://localhost:5031/api/meta"
API_ESTADOS = "http://localhost:5031/api/estado"

#-----Listar proyectos--------

@rutas_proyectos.route("/proyectos")
def proyectos():
    try:
        respuesta = requests.get(API_URL)
        proyectos = respuesta.json().get("datos",[])
        
        # Obtener información adicional para cada proyecto
        for proyecto in proyectos:
            proyecto['proyecto_padre_info'] = obtener_proyecto_padre(proyecto.get('id_proyecto_padre'))
            proyecto['responsable_info'] = obtener_responsable(proyecto.get('id_responsable'))
            proyecto['tipo_proyecto_info'] = obtener_tipo_proyecto(proyecto.get('id_tipo_proyecto'))
            proyecto['metas'] = obtener_metas_proyecto(proyecto['id'])
            proyecto['estados'] = obtener_estados_proyecto(proyecto['id'])
            
    except Exception as e:
        proyectos = []
        print("Error al conectar con la API", e)
    
    # Obtener datos para los formularios
    try:
        todos_proyectos = requests.get(API_URL).json().get("datos", [])
        todos_responsables = requests.get(API_RESPONSABLES).json().get("datos", [])
        todos_tipos_proyecto = requests.get(API_TIPO_PROYECTO).json().get("datos", [])
        todas_metas = requests.get(API_METAS).json().get("datos", [])
        todos_estados = requests.get(API_ESTADOS).json().get("datos", [])
    except Exception as e:
        todos_proyectos = []
        todos_responsables = []
        todos_tipos_proyecto = []
        todas_metas = []
        todos_estados = []
        print("Error al obtener datos para formularios", e)
        
    return render_template(
        "proyectos.html",
        proyectos = proyectos,
        proyecto = None,
        todos_proyectos = todos_proyectos,
        todos_responsables = todos_responsables,
        todos_tipos_proyecto = todos_tipos_proyecto,
        todas_metas = todas_metas,
        todos_estados = todos_estados,
        modo = "crear"
    )        

# Funciones para obtener información relacionada
def obtener_proyecto_padre(id_proyecto_padre):
    if not id_proyecto_padre:
        return None
    try:
        respuesta = requests.get(f"{API_URL}/id/{id_proyecto_padre}")
        datos = respuesta.json().get("datos", [])
        return datos[0] if datos else None
    except Exception as e:
        print(f"Error al obtener proyecto padre {id_proyecto_padre}: {e}")
        return None

def obtener_responsable(id_responsable):
    if not id_responsable:
        return None
    try:
        respuesta = requests.get(f"{API_RESPONSABLES}/id/{id_responsable}")
        datos = respuesta.json().get("datos", [])
        return datos[0] if datos else None
    except Exception as e:
        print(f"Error al obtener responsable {id_responsable}: {e}")
        return None

def obtener_tipo_proyecto(id_tipo_proyecto):
    if not id_tipo_proyecto:
        return None
    try:
        respuesta = requests.get(f"{API_TIPO_PROYECTO}/id/{id_tipo_proyecto}")
        datos = respuesta.json().get("datos", [])
        return datos[0] if datos else None
    except Exception as e:
        print(f"Error al obtener tipo proyecto {id_tipo_proyecto}: {e}")
        return None

def obtener_metas_proyecto(id_proyecto):
    try:
        respuesta = requests.get(f"{API_META_PROYECTO}/id_proyecto/{id_proyecto}")
        return respuesta.json().get("datos", [])
    except Exception as e:
        print(f"Error al obtener metas del proyecto {id_proyecto}: {e}")
        return []

def obtener_estados_proyecto(id_proyecto):
    try:
        respuesta = requests.get(f"{API_ESTADO_PROYECTO}/id_proyecto/{id_proyecto}")
        return respuesta.json().get("datos", [])
    except Exception as e:
        print(f"Error al obtener estados del proyecto {id_proyecto}: {e}")
        return []
    
#------- Buscar proyecto --------

@rutas_proyectos.route("/proyectos/buscar", methods=["POST"])
def buscar_proyecto():
        
        id = request.form.get("id_buscar")
        
        if id:
            try:
                respuesta = requests.get(f"{API_URL}/id/{id}")
                if respuesta.status_code == 200:
                    datos = respuesta.json().get("datos", [])
                    if datos:
                        proyecto = datos[0]
                        # Obtener información relacionada del proyecto encontrado
                        proyecto['proyecto_padre_info'] = obtener_proyecto_padre(proyecto.get('id_proyecto_padre'))
                        proyecto['responsable_info'] = obtener_responsable(proyecto.get('id_responsable'))
                        proyecto['tipo_proyecto_info'] = obtener_tipo_proyecto(proyecto.get('id_tipo_proyecto'))
                        proyecto['metas'] = obtener_metas_proyecto(proyecto['id'])
                        proyecto['estados'] = obtener_estados_proyecto(proyecto['id'])
                        
                        proyectos = requests.get(API_URL).json().get("datos", [])
                        for p in proyectos:
                            p['proyecto_padre_info'] = obtener_proyecto_padre(p.get('id_proyecto_padre'))
                            p['responsable_info'] = obtener_responsable(p.get('id_responsable'))
                            p['tipo_proyecto_info'] = obtener_tipo_proyecto(p.get('id_tipo_proyecto'))
                            p['metas'] = obtener_metas_proyecto(p['id'])
                            p['estados'] = obtener_estados_proyecto(p['id'])
                        
                        todos_proyectos = requests.get(API_URL).json().get("datos", [])
                        todos_responsables = requests.get(API_RESPONSABLES).json().get("datos", [])
                        todos_tipos_proyecto = requests.get(API_TIPO_PROYECTO).json().get("datos", [])
                        todas_metas = requests.get(API_METAS).json().get("datos", [])
                        todos_estados = requests.get(API_ESTADOS).json().get("datos", [])
                        
                        return render_template(
                            "proyectos.html",
                            proyectos = proyectos,
                            proyecto = proyecto,
                            todos_proyectos = todos_proyectos,
                            todos_responsables = todos_responsables,
                            todos_tipos_proyecto = todos_tipos_proyecto,
                            todas_metas = todas_metas,
                            todos_estados = todos_estados,
                            modo = "actualizar"
                        )
                
            
            except Exception as e:
                return f"Error en la búsqueda: {e}"             
        
        proyectos = requests.get(API_URL).json().get("datos", [])
        for p in proyectos:
            p['proyecto_padre_info'] = obtener_proyecto_padre(p.get('id_proyecto_padre'))
            p['responsable_info'] = obtener_responsable(p.get('id_responsable'))
            p['tipo_proyecto_info'] = obtener_tipo_proyecto(p.get('id_tipo_proyecto'))
            p['metas'] = obtener_metas_proyecto(p['id'])
            p['estados'] = obtener_estados_proyecto(p['id'])
            
        todos_proyectos = requests.get(API_URL).json().get("datos", [])
        todos_responsables = requests.get(API_RESPONSABLES).json().get("datos", [])
        todos_tipos_proyecto = requests.get(API_TIPO_PROYECTO).json().get("datos", [])
        todas_metas = requests.get(API_METAS).json().get("datos", [])
        todos_estados = requests.get(API_ESTADOS).json().get("datos", [])
        
        return render_template(
            "proyectos.html",
            proyectos=proyectos,
            proyecto=None,
            todos_proyectos=todos_proyectos,
            todos_responsables=todos_responsables,
            todos_tipos_proyecto=todos_tipos_proyecto,
            todas_metas=todas_metas,
            todos_estados=todos_estados,
            mensaje="Proyecto no encontrado",
            modo="crear"
        )       
        
        
# --------------- Crear proyecto ------------------

@rutas_proyectos.route("/proyectos/crear", methods=["POST"])
def crear_proyecto():
    
    datos ={
        "id_proyecto_padre": request.form.get("id_proyecto_padre") or None,
        "id_responsable": request.form.get("id_responsable") or None,
        "id_tipo_proyecto": request.form.get("id_tipo_proyecto") or None,
        "codigo": request.form.get("codigo"),
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion"),
        "fecha_inicio": request.form.get("fecha_inicio") or None,
        "fecha_fin_prevista": request.form.get("fecha_fin_prevista") or None,
        "fecha_modificacion": request.form.get("fecha_modificacion") or None,
        "fecha_finalizacion": request.form.get("fecha_finalizacion") or None,
        "ruta_logo": request.form.get("ruta_logo") or None
    }  
    
    try:
        respuesta = requests.post(API_URL, json=datos)
        if respuesta.status_code == 200 or respuesta.status_code == 201:
            resultado = respuesta.json()
            id_proyecto = resultado.get("id") or resultado.get("datos", {}).get("id")
            
            # Asignar metas seleccionadas
            metas_seleccionadas = request.form.getlist("metas[]")
            if id_proyecto and metas_seleccionadas:
                asignar_metas(id_proyecto, metas_seleccionadas)
            
            # Asignar estados seleccionados
            estados_seleccionados = request.form.getlist("estados[]")
            if id_proyecto and estados_seleccionados:
                asignar_estados(id_proyecto, estados_seleccionados)
                
    except Exception as e:
        return f"Error al crear proyecto: {e}"
    
    return redirect(url_for("rutas_proyectos.proyectos"))    
            
            
            
# ------- Actualizar proyecto -----------
@rutas_proyectos.route("/proyecto/actualizar", methods=["POST"])
def actualizar_proyecto():
    
    id =  request.form.get("id")
    datos = {
        "id_proyecto_padre": request.form.get("id_proyecto_padre") or None,
        "id_responsable": request.form.get("id_responsable") or None,
        "id_tipo_proyecto": request.form.get("id_tipo_proyecto") or None,
        "codigo": request.form.get("codigo"),
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion"),
        "fecha_inicio": request.form.get("fecha_inicio") or None,
        "fecha_fin_prevista": request.form.get("fecha_fin_prevista") or None,
        "fecha_modificacion": request.form.get("fecha_modificacion") or None,
        "fecha_finalizacion": request.form.get("fecha_finalizacion") or None,
        "ruta_logo": request.form.get("ruta_logo") or None
    }   
    
    try:
        requests.put(f"{API_URL}/id/{id}", json=datos)
        
        # Actualizar metas
        metas_seleccionadas = request.form.getlist("metas[]")
        actualizar_metas_proyecto(id, metas_seleccionadas)
        
        # Actualizar estados
        estados_seleccionados = request.form.getlist("estados[]")
        actualizar_estados_proyecto(id, estados_seleccionados)
        
    except Exception as e:
        return f"Error al actualizar proyecto {e}"
    
    return redirect(url_for("rutas_proyectos.proyectos"))  


# -------- Eliminar proyecto ----------

@rutas_proyectos.route("/proyectos/eliminar/<string:id>", methods=["POST"])
def eliminar_proyecto(id):
    
    try:
        requests.delete(f"{API_URL}/id/{id}")       
    except Exception as e:
        return f"Error al eliminar proyecto: {e}"
    
    return redirect(url_for("rutas_proyectos.proyectos"))


# -------- Funciones para gestionar metas ----------

def asignar_metas(id_proyecto, lista_metas):
    """Asigna metas a un proyecto"""
    
    from datetime import datetime
    for id_meta in lista_metas:
        try:
            datos = {
                "id_proyecto": id_proyecto,
                "id_meta": id_meta,
                "fecha_asociacion": datetime.now().isoformat()
            }
            requests.post(API_META_PROYECTO, json=datos)
        except Exception as e:
            print(f"Error al asignar meta {id_meta}: {e}")

def actualizar_metas_proyecto(id_proyecto, lista_metas):
    """Actualiza las metas de un proyecto"""
    try:
        requests.delete(f"{API_META_PROYECTO}/id_proyecto/{id_proyecto}")
        asignar_metas(id_proyecto, lista_metas)
    except Exception as e:
        print(f"Error al actualizar metas: {e}")


# -------- Funciones para gestionar estados ----------

def asignar_estados(id_proyecto, lista_estados):
    """Asigna estados a un proyecto"""
    
    from datetime import datetime
    for id_estado in lista_estados:
        try:
            datos = {
                "id_proyecto": id_proyecto,
                "id_estado": id_estado,
                "fecha_asociacion": datetime.now().isoformat()
            }
            requests.post(API_ESTADO_PROYECTO, json=datos)
        except Exception as e:
            print(f"Error al asignar estado {id_estado}: {e}")

def actualizar_estados_proyecto(id_proyecto, lista_estados):
    """Actualiza los estados de un proyecto"""
    try:
        requests.delete(f"{API_ESTADO_PROYECTO}/id_proyecto/{id_proyecto}")
        asignar_estados(id_proyecto, lista_estados)
    except Exception as e:
        print(f"Error al actualizar estados: {e}")