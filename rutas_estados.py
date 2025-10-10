from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_estados = Blueprint("rutas_estados", __name__)

API_URL = "http://localhost:5031/api/estado"

# --- Listar .......

@rutas_estados.route("/estados")
def estados():
    
    try:
        respuesta = requests.get(API_URL)
        estados = respuesta.json().get("datos",[])
    except Exception as e:
        estados = []
        print("Error al conectar con la API:", e)
            
            
    return render_template(
        "estados.html",
        estados = estados,
        estado = None,
        modo = 'crear'
        
    ) 
    
    
# --------- Buscar ------------

@rutas_estados.route("/estados/buscar", methods=["POST"])
def buscar_estado():
    
    id = request.form.get("id_buscar")
    
    if id:
        try:
            respuesta = requests.get(f"{API_URL}/id/{id}")  
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])  
                if datos:
                    estado = datos[0]
                    estados = requests.get(API_URL).json().get("datos", [])  
                    return render_template(
                        "estados.html",
                        estados = estados,
                        estado = estado,
                        modo = "actualizar"
                        
                    )
        except Exception as e:
            return f"Error en la busqueda {e}"
    estados = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "estados.html",
        estados = estados,
        estado = None,
        modo = "crear"
                        
                    )  
    
    
# ------ Crear  ..........  

@rutas_estados.route("/estados/crear", methods = ["POST"])
def crear_estado():
    
    datos = {
        "id" : request.form.get("id"),
        "nombre": request.form.get("nombre"),
        "descripcion" : request.form.get("descripcion")
    }  
    
    try:
        requests.post(API_URL, json = datos)
    except Exception as e:
        return f"Error al crear estado {e}"
    
    return redirect(url_for("rutas_estados.estados"))  


# ------ Actualizar -------------

@rutas_estados.route("/estados/actualizar", methods=["POST"])
def actualizar_estado():
    
    id = request.form.get("id")
    datos = {
        "nombre": request.form.get("nombre"),
        "descripcion" : request.form.get("descripcion")
    }
    try:
        requests.put(f"{API_URL}/id/{id}", json=datos)
    except Exception as e:
        return f"Error al actualizar estado {e}"
    
    return redirect(url_for("rutas_estados.estados"))

#------- Eliminar ----------

@rutas_estados.route("/estados/eliminar/<string:id>", methods=["POST"])
def eliminar_estado(id):   
    try:
        requests.delete(f"{API_URL}/id/{id}")
    except Exception as e:
        return f"Error al eliminar estado: {e}"
            
    return redirect(url_for("rutas_estados.estados"))