from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_tipos_proyecto = Blueprint("rutas_tipos_proyecto", __name__)

API_URL = "http://localhost:5031/api/tipo_proyecto"

# --- Listar .......

@rutas_tipos_proyecto.route("/tipos_proyecto")
def tipos_proyecto():
    
    try:
        respuesta = requests.get(API_URL)
        tipos_proyecto = respuesta.json().get("datos",[])
    except Exception as e:
        tipos_proyecto = []
        print("Error al conectar con la API:", e)
            
            
    return render_template(
        "tipos_proyecto.html",
        tipos_proyecto = tipos_proyecto,
        tipo_proyecto = None,
        modo = 'crear'
        
    ) 
    
    
# --------- Buscar ------------

@rutas_tipos_proyecto.route("/tipos_proyecto/buscar", methods=["POST"])
def buscar_tipo_proyecto():
    
    id = request.form.get("id_buscar")
    
    if id:
        try:
            respuesta = requests.get(f"{API_URL}/id/{id}")  
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])  
                if datos:
                    tipo_proyecto = datos[0]
                    tipos_proyecto = requests.get(API_URL).json().get("datos", [])  
                    return render_template(
                        "tipos_proyecto.html",
                        tipos_proyecto = tipos_proyecto,
                        tipo_proyecto = tipo_proyecto,
                        modo = "actualizar"
                        
                    )
        except Exception as e:
            return f"Error en la busqueda {e}"
    tipos_proyecto = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "tipos_proyecto.html",
        tipos_proyecto = tipos_proyecto,
        tipo_proyecto = None,
        modo = "crear"
                        
                    )  
    
    
# ------ Crear  ..........  

@rutas_tipos_proyecto.route("/tipos_proyecto/crear", methods = ["POST"])
def crear_tipo_proyecto():
    
    datos = {
        "id" : request.form.get("id"),
        "nombre": request.form.get("nombre"),
        "descripcion" : request.form.get("descripcion")
    }  
    
    try:
        requests.post(API_URL, json = datos)
    except Exception as e:
        return f"Error al crear el tipo de proyecto {e}"
    
    return redirect(url_for("rutas_tipos_proyecto.tipos_proyecto"))  


# ------ Actualizar -------------

@rutas_tipos_proyecto.route("/tipos_proyecto/actualizar", methods=["POST"])
def actualizar_tipo_proyecto():
    
    id = request.form.get("id")
    datos = {
        "nombre": request.form.get("nombre"),
        "descripcion" : request.form.get("descripcion")
    }
    try:
        requests.put(f"{API_URL}/id/{id}", json=datos)
    except Exception as e:
        return f"Error al actualizar el tipo de proyecto {e}"
    
    return redirect(url_for("rutas_tipos_proyecto.tipos_proyecto"))

#------- Eliminar ----------

@rutas_tipos_proyecto.route("/tipos_proyecto/eliminar/<string:id>", methods=["POST"])
def eliminar_tipo_proyecto(id):   
    try:
        requests.delete(f"{API_URL}/id/{id}")
    except Exception as e:
        return f"Error al eliminar tipo de proyecto: {e}"
            
    return redirect(url_for("rutas_tipos_proyecto.tipos_proyecto"))