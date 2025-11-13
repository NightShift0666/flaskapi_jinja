from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_responsables = Blueprint("rutas_responsables", __name__)

API_URL = "http://localhost:5031/api/responsable"
API_TIPOS_RESPONSABLE = "http://localhost:5031/api/tipo_responsable"  
API_USUARIOS = "http://localhost:5031/api/usuario"  

#-----Listar responsables--------

@rutas_responsables.route("/responsables")
def responsables():
    try:
        respuesta = requests.get(API_URL)
        responsables = respuesta.json().get("datos",[])
    except Exception as e:
        responsables = []
        print("Error al conectar con la API", e)
    
    # Obtener tipos de responsable
    try:
        respuesta_tipos = requests.get(API_TIPOS_RESPONSABLE)
        tipos_responsable = respuesta_tipos.json().get("datos", [])
    except Exception as e:
        tipos_responsable = []
        print("Error al obtener tipos de responsable", e)
    
    # Obtener usuarios
    try:
        respuesta_usuarios = requests.get(API_USUARIOS)
        usuarios = respuesta_usuarios.json().get("datos", [])
    except Exception as e:
        usuarios = []
        print("Error al obtener usuarios", e)
        
    return render_template(
        "responsables.html",
        responsables = responsables,
        responsable = None,
        tipos_responsable = tipos_responsable,
        usuarios = usuarios,
        modo = "crear"
    )        
    
#------- Buscar responsable --------

@rutas_responsables.route("/responsables/buscar", methods=["POST"])
def buscar_responsable():
        
        id = request.form.get("id_buscar")
        
        if id:
            try:
                respuesta = requests.get(f"{API_URL}/id/{id}")
                if respuesta.status_code == 200:
                    datos = respuesta.json().get("datos", [])
                    if datos:
                        responsable = datos[0]
                        responsables = requests.get(API_URL).json().get("datos", [])
                        
                        # Obtener tipos de responsable
                        tipos_responsable = requests.get(API_TIPOS_RESPONSABLE).json().get("datos", [])
                        
                        # Obtener usuarios
                        usuarios = requests.get(API_USUARIOS).json().get("datos", [])
                        
                        return render_template(
                            "responsables.html",
                            responsables = responsables,
                            responsable = responsable,
                            tipos_responsable = tipos_responsable,
                            usuarios = usuarios,
                            modo = "actualizar"
                        )
                
            
            except Exception as e:
                return f"Error en la búsqueda: {e}"             
        
        responsables = requests.get(API_URL).json().get("datos", [])
        tipos_responsable = requests.get(API_TIPOS_RESPONSABLE).json().get("datos", [])
        usuarios = requests.get(API_USUARIOS).json().get("datos", [])
        
        return render_template(
            "responsables.html",
            responsables=responsables,
            responsable=None,
            tipos_responsable=tipos_responsable,
            usuarios=usuarios,
            mensaje="responsable no encontrado",
            modo="crear"
        )       
        
        
# --------------- Crear responsable ------------------

@rutas_responsables.route("/responsables/crear", methods=["POST"])
def crear_responsable():
    
    datos = {
        "id_tipo_responsable": request.form.get("id_tipo_responsable"),
        "id_usuario": request.form.get("id_usuario"),
        "nombre": request.form.get("nombre")
    }  
    
    try:
        requests.post(API_URL, json=datos)  
    except Exception as e:
        return f"Error al crear responsable: {e}"
    
    return redirect(url_for("rutas_responsables.responsables"))    
            
            
            
# ------- Actualizar responsable -----------
@rutas_responsables.route("/responsables/actualizar", methods=["POST"])
def actualizar_responsable():
    
    id =  request.form.get("id")
    datos = {
        "id": request.form.get("id"),
        "id_tipo_responsable": request.form.get("id_tipo_responsable"),
        "id_usuario": request.form.get("id_usuario"),
        "nombre": request.form.get("nombre")
    }   
    
    try:
        requests.put(f"{API_URL}/id/{id}", json=datos)
    except Exception as e:
        return f"Error al actualizar responsable {e}"
    
    return redirect(url_for("rutas_responsables.responsables"))  


# -------- Eliminar responsable ----------

@rutas_responsables.route("/responsables/eliminar/<string:id>", methods=["POST"])
def eliminar_responsable(id):
    
    try:
        requests.delete(f"{API_URL}/id/{id}")       
    except Exception as e:
        return f"Error al eliminar responsable: {e}"
    
    return redirect(url_for("rutas_responsables.responsables"))