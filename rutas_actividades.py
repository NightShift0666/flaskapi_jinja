from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_actividades = Blueprint("rutas_actividades", __name__)

API_URL = "http://localhost:5031/api/actividad"
API_ENTREGABLES = "http://localhost:5031/api/entregable"

#Listar

@rutas_actividades.route("/actividades")
def actividades():
    try:
        respuesta = requests.get(API_URL)
        actividades = respuesta.json().get("datos",[])
    except Exception as e:
        actividades = []
        print("Error al conectar con la API", e)
        
    #obtener entregables
    try:
        respuesta = requests.get(API_ENTREGABLES)
        entregables = respuesta.json().get("datos",[])
    except Exception as e:
        entregables = []
        print("Error al conectar con la API", e)     
        
        
    return render_template(
        "actividades.html",
        actividades = actividades,
        actividad = None,
        entregables = entregables,
        modo = "crear"
        
    )       
    
    
# Buscar

@rutas_actividades.route("/actividades/buscar", methods=["POST"])  
def buscar_actividad():
    
    id = request.form.get("id_buscar")  
    
    if id:
        
        try:
                respuesta = requests.get(f"{API_URL}/id/{id}")
                if respuesta.status_code == 200:
                    datos = respuesta.json().get("datos", [])
                    if datos:
                        actividad = datos[0]
                        actividades = requests.get(API_URL).json().get("datos", [])
                        entregables = requests.get(API_ENTREGABLES).json().get("datos", [])
                        return render_template(
                            "actividades.html",
                            actividades = actividades,
                            actividad = actividad,
                            entregables = entregables,
                            modo = "actualizar"
        
                        )    
        except Exception as e:
                return f"Error en la búsqueda: {e}"    
            
    actividades = requests.get(API_URL).json().get("datos", [])
    entregables = requests.get(API_ENTREGABLES).json().get("datos", [])
    
        
    return render_template(
            "actividades.html",
            actividades = actividades,
            actividad = None,
            entregables = entregables,
            mensaje = "actividad no encontrada",
            modo = "crear"
        )                 
    

#Crear

@rutas_actividades.route("/actividades/crear", methods=["POST"])
def crear_actividad():
    
    datos = {
        "id_entregable": request.form.get("id_entregable"),
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion"),
        "fecha_inicio": request.form.get("fecha_inicio"),
        "fecha_fin_prevista": request.form.get("fecha_fin_prevista"),
        "fecha_modificacion": request.form.get("fecha_modificacion"),
        "fecha_finalizacion": request.form.get("fecha_finalizacion"),
        "prioridad": request.form.get("prioridad"),
        "porcentaje_avance": request.form.get("porcentaje_avance")
        
    }  
    
    try:
        requests.post(API_URL, json=datos)  
    except Exception as e:
        return f"Error al crear actividad: {e}"
    
    return redirect(url_for("rutas_actividades.actividades"))  


#Actualizar

@rutas_actividades.route("/actividades/actualizar", methods=["POST"])
def actualizar_actividad():
    
    id =  request.form.get("id")
    datos = {
        "id_entregable": request.form.get("id_entregable"),
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion"),
        "fecha_inicio": request.form.get("fecha_inicio"),
        "fecha_fin_prevista": request.form.get("fecha_fin_prevista"),
        "fecha_modificacion": request.form.get("fecha_modificacion"),
        "fecha_finalizacion": request.form.get("fecha_finalizacion"),
        "prioridad": request.form.get("prioridad"),
        "porcentaje_avance": request.form.get("porcentaje_avance")
        
    }
    try:
        requests.put(f"{API_URL}/id/{id}", json=datos)
    except Exception as e:
        return f"Error al actualizar actividad {e}"
    
    return redirect(url_for("rutas_actividades.actividades"))  

#Eliminar

@rutas_actividades.route("/actividades/eliminar/<string:id>", methods=["POST"])
def eliminar_actividad(id):
    
    try:
        requests.delete(f"{API_URL}/id/{id}")       
    except Exception as e:
        return f"Error al eliminar actividad: {e}"
    
    return redirect(url_for("rutas_actividades.actividades"))

    
      
    