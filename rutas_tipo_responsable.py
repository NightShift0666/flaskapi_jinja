# Importar módulos necesarios de Flask y la librería requests para conectarse a la API externa
from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_tipos_responsable = Blueprint("rutas_tipos_responsable", __name__)

API_URL = "http://localhost:5031/api/tipo_responsable"

# ------------------- LISTAR tipos de responsable -------------------

@rutas_tipos_responsable.route("/tipos_responsable")
def tipos_responsable():
    try:
        respuesta = requests.get(API_URL)
        tipos_responsable = respuesta.json().get("datos", [])
    except Exception as e:
        tipos_responsable = []
        print("Error al conectar con la API:", e)
        
    return render_template(
        "tipos_responsable.html",
        tipos_responsable=tipos_responsable,
        tipo_responsable=None,
        modo="crear"
    )    
    
    
# ------------------- BUSCAR tipos de responsable-------------------
    
@rutas_tipos_responsable.route("/tipos_responsable/buscar", methods=['POST'])
def buscar_tipo_responsable():
    id = request.form.get("id_buscar")
    
    if id:
        try:
            respuesta = requests.get(f"{API_URL}/id/{id}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    # Si la API retorna datos, se asume que es una lista con un tipo de responsable
                    tipo_responsable = datos[0]
                    tipos_responsable = requests.get(API_URL).json().get("datos", [])
                    return render_template(
                        "tipos_responsable.html",
                        tipos_responsable=tipos_responsable,
                        tipo_responsable=tipo_responsable,
                        modo="actualizar",
                   
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    # Si no se encuentra el tipo de responsable, recargar la lista completa
    tipos_responsable = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "tipos_responsable.html",
        tipos_responsable=tipos_responsable,
        tipo_responsable=None,
        mensaje="Tipo de responsable no encontrado",
        modo="crear"
    )
    
    
# ------------------- CREAR tipo de responsable -------------------    

@rutas_tipos_responsable.route("/tipos_responsable/crear", methods=["POST"])
def crear_tipo_responsable():

    datos = {
        "id": request.form.get("id"),
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear responsable: {e}"

    return redirect(url_for("rutas_tipos_responsable.tipos_responsable"))



# ------------------- ACTUALIZAR tipo de responsable -------------------
@rutas_tipos_responsable.route("/tipos_responsable/actualizar", methods=["POST"])
def actualizar_tipo_responsable():

    id = request.form.get("id")
    datos = {
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        requests.put(f"{API_URL}/id/{id}", json=datos)
    except Exception as e:
        return f"Error al actualizar el tresponsable: {e}"

    return redirect(url_for("rutas_tipos_responsable.tipos_responsable"))

# ------------------- ELIMINAR tipo de responsable -------------------
@rutas_tipos_responsable.route("/tipos_responsable/eliminar/<string:id>", methods=["POST"])
def eliminar_tipo_responsable(id):

    try:
        requests.delete(f"{API_URL}/id/{id}")
    except Exception as e:
        return f"Error al eliminar tipo de responsable: {e}"
        

    return redirect(url_for("rutas_tipos_responsable.tipos_responsable"))