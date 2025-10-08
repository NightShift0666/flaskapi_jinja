# Importar módulos necesarios de Flask y la librería requests para conectarse a la API externa
from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_tipos_producto = Blueprint("rutas_tipos_producto", __name__)

API_URL = "http://localhost:5031/api/tipo_producto"

# ------------------- LISTAR tipos de producto -------------------

@rutas_tipos_producto.route("/tipos_producto")
def tipos_producto():
    try:
        respuesta = requests.get(API_URL)
        tipos_producto = respuesta.json().get("datos", [])
    except Exception as e:
        tipos_producto = []
        print("Error al conectar con la API:", e)
        
    return render_template(
        "tipos_producto.html",
        tipos_producto=tipos_producto,
        tipo_producto=None,
        modo="crear"
    )    
    
    
# ------------------- BUSCAR tipos de producto-------------------
    
@rutas_tipos_producto.route("/tipos_producto/buscar", methods=['POST'])
def buscar_tipo_producto():
    id = request.form.get("id_buscar")
    
    if id:
        try:
            respuesta = requests.get(f"{API_URL}/id/{id}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    # Si la API retorna datos, se asume que es una lista con un tipo de producto
                    tipo_producto = datos[0]
                    tipos_producto = requests.get(API_URL).json().get("datos", [])
                    return render_template(
                        "tipos_producto.html",
                        tipos_producto=tipos_producto,
                        tipo_producto=tipo_producto,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    # Si no se encuentra el tipo de producto, recargar la lista completa
    tipos_producto = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "tipos_producto.html",
        tipos_producto=tipos_producto,
        tipo_producto=None,
        mensaje="Tipo de producto no encontrado",
        modo="crear"
    )
    
    
# ------------------- CREAR tipo de producto -------------------    

@rutas_tipos_producto.route("/tipos_producto/crear", methods=["POST"])
def crear_tipo_producto():

    datos = {
        "id": request.form.get("id"),
        "nombre": request.form.get("nombre"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear producto: {e}"

    return redirect(url_for("rutas_tipos_producto.tipos_producto"))



# ------------------- ACTUALIZAR tipo de producto -------------------
@rutas_tipos_producto.route("/tipos_producto/actualizar", methods=["POST"])
def actualizar_tipo_producto():

    id = request.form.get("id")
    datos = {
        "nombre": request.form.get("nombre"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        requests.put(f"{API_URL}/id/{id}", json=datos)
    except Exception as e:
        return f"Error al actualizar el tipo de producto: {e}"

    return redirect(url_for("rutas_tipos_producto.tipos_producto"))

# ------------------- ELIMINAR tipo de producto -------------------
@rutas_tipos_producto.route("/tipos_producto/eliminar/<string:id>", methods=["POST"])
def eliminar_tipo_producto(id):

    try:
        requests.delete(f"{API_URL}/id/{id}")
    except Exception as e:
        return f"Error al eliminar tipo de producto: {e}"
        

    return redirect(url_for("rutas_tipos_producto.tipos_producto"))