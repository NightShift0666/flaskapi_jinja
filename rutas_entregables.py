from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_entregables = Blueprint("rutas_entregables", __name__)

API_URL = "http://localhost:5031/api/entregable"

#-----Listar entregables--------

@rutas_entregables.route("/entregables")
def entregables():
    try:
        respuesta = requests.get(API_URL)
        entregables = respuesta.json().get("datos",[])
    except Exception as e:
        entregables = []
        print("Error al conectar con la API", e)
        
    return render_template(
        "entregables.html",
        entregables = entregables,
        entregable = None,
        modo = "crear"
    )        
    
#------- Buscar entrgable --------

@rutas_entregables.route("/entregables/buscar", methods=["POST"])
def buscar_entregable():
        
        id = request.form.get("id_buscar")
        
        if id:
            try:
                respuesta = requests.get(f"{API_URL}/id/{id}")
                if respuesta.status_code == 200:
                    datos = respuesta.json().get("datos", [])
                    if datos:
                        entregable = datos[0]
                        entregables = requests.get(API_URL).json().get("datos", [])
                        return render_template(
                            "entregables.html",
                            entregables = entregables,
                            entregable = entregable,
                            modo = "actualizar"
                        )
                
            
            except Exception as e:
                return f"Error en la búsqueda: {e}"             
        
        entregables = requests.get(API_URL).json().get("datos", [])
        return render_template(
            "entregables.html",
            entregables=entregables,
            entregable=None,
            mensaje="Entregable no encontrado",
            modo="crear"
        )       
        
        
# --------------- Crear entregable ------------------

@rutas_entregables.route("/entregables/crear", methods=["POST"])
def crear_entregable():
    
    datos ={
        "id": request.form.get("id"),
        "codigo": request.form.get("codigo"),
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion"),
        "fecha_inicio": request.form.get("fecha_inicio"),
        "fecha_fin_prevista": request.form.get("fecha_fin_prevista"),
        "fecha_modificacion": request.form.get("fecha_modificacion"),
        "fecha_finalizacion": request.form.get("fecha_finalizacion")
    }  
    
    try:
        requests.post(API_URL, json=datos)  
    except Exception as e:
        return f"Error al crear entregable: {e}"
    
    return redirect(url_for("rutas_entregables.entregables"))    
            
            
            
# ------- Actualizar entregable -----------
@rutas_entregables.route("/entregable/actualizar", methods=["POST"])
def actualizar_entregable():
    
    id =  request.form.get("id")
    datos = {
        "codigo": request.form.get("codigo"),
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion"),
        "fecha_inicio": request.form.get("fecha_inicio"),
        "fecha_fin_prevista": request.form.get("fecha_fin_prevista"),
        "fecha_modificacion": request.form.get("fecha_modificacion"),
        "fecha_finalizacion": request.form.get("fecha_finalizacion")
        
    }   
    
    try:
        requests.put(f"{API_URL}/id/{id}", json=datos)
    except Exception as e:
        return f"Error al actualizar entregable {e}"
    
    return redirect(url_for("rutas_entregables.entregables"))  


# -------- Eliminar entregable ----------

@rutas_entregables.route("/entregables/eliminar/<string:id>", methods=["POST"])
def eliminar_entregable(id):
    
    try:
        requests.delete(f"{API_URL}/id/{id}")       
    except Exception as e:
        return f"Error al eliminar entregable: {e}"
    
    return redirect(url_for("rutas_entregables.entregables"))
                