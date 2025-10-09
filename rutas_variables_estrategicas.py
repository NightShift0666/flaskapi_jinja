from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_variables_estrategicas = Blueprint("rutas_variables_estrategicas",__name__)

API_URL = "http://localhost:5031/api/variable_estrategica"

@rutas_variables_estrategicas.route("/variables_estrategicas")
def variables_estrategicas():
    try:
        respuesta = requests.get(API_URL)
        variables_estrategicas = respuesta.json().get("datos", [])
    except Exception as e:
        variables_estrategicas = []
        print("Error al conectar con la API:", e)
        
    return render_template(
        "variables_estrategicas.html",
        variables_estrategicas=variables_estrategicas,
        variable_estrategica=None,
        modo="crear"
    )    
    
    
@rutas_variables_estrategicas.route("/variables_estrategicas/buscar", methods=['POST'])
def buscar_variable_estrategica():
    id = request.form.get("id_buscar")
    
    if id:
        try:
            respuesta = requests.get(f"{API_URL}/id/{id}")
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])
                if datos:
                    # Si la API retorna datos, se asume que es una lista con un tipo de producto
                    variable_estrategica = datos[0]
                    variables_estrategicas = requests.get(API_URL).json().get("datos", [])
                    return render_template(
                        "variables_estrategicas.html",
                        variables_estrategicas=variables_estrategicas,
                        variable_estrategica=variable_estrategica,
                        modo="actualizar"
                    )
        except Exception as e:
            return f"Error en la búsqueda: {e}"

    # Si no se encuentra el tipo de producto, recargar la lista completa
    variables_estrategicas = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "variables_estrategicas.html",
        variables_estrategicas=variables_estrategicas,
        tipo_producto=None,
        mensaje="Variable no encontrada",
        modo="crear"
    )
    
    
@rutas_variables_estrategicas.route("/variables_estrategicas/crear", methods=["POST"]) 
def crear_variable_estrategica():
    datos = {
        "id": request.form.get("id"),
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion")
        
    }   
    
    try:
        requests.post(API_URL, json=datos)
    except Exception as e:
        return f"Error al crear variable: {e}"

    return redirect(url_for("rutas_variables_estrategicas.variables_estrategicas"))


@rutas_variables_estrategicas.route("/variables_estrategicas/actualizar", methods=["POST"])
def actualizar_variable_estrategica():

    id = request.form.get("id")
    datos = {
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion")
    }

    try:
        requests.put(f"{API_URL}/id/{id}", json=datos)
    except Exception as e:
        return f"Error al actualizar el variable: {e}"

    return redirect(url_for("rutas_variables_estrategicas.variables_estrategicas"))

@rutas_variables_estrategicas.route("/variables_estrategicas/eliminar/<string:id>", methods=["POST"])
def eliminar_variable_estrategica(id):

    try:
        requests.delete(f"{API_URL}/id/{id}")
    except Exception as e:
        return f"Error al eliminar variable: {e}"
        

    return redirect(url_for("rutas_variables_estrategicas.variables_estrategicas"))
