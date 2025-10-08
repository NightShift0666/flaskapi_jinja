from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_usuarios = Blueprint("rutas_usuarios",__name__)

API_URL = "http://localhost:5031/api/usuario"

@rutas_usuarios.route("/usuarios")
def usuarios():
    
    try:
        respuesta = requests.get(API_URL)
        usuarios = respuesta.json().get("datos",[])
    except Exception as e:
        usuarios = []
        print("Error al conectar con la API:", e)
            
            
    return render_template(
        "usuarios.html",
        usuarios = usuarios,
        usuario = None,
        modo = 'crear')
        
@rutas_usuarios.route("/usuarios/buscar", methods=["POST"])
def buscar_usuario():
    
    id = request.form.get("id_buscar")
    
    if id:
        try:
            respuesta = requests.get(f"{API_URL}/id/{id}")  
            if respuesta.status_code == 200:
                datos = respuesta.json().get("datos", [])  
                if datos:
                    usuario = datos[0]
                    usuarios = requests.get(API_URL).json().get("datos", [])  
                    return render_template(
                        "usuarios.html",
                        usuarios = usuarios,
                        usuario = usuario,
                        modo = "actualizar"
                        
                    )
        except Exception as e:
            return f"Error en la busqueda {e}"
    usuarios = requests.get(API_URL).json().get("datos", [])
    return render_template(
        "usuarios.html",
        usuarios = usuarios,
        usuario = None,
        modo = "crear"
                        
                    )  
    
        
        
@rutas_usuarios.route("/usuarios/crear", methods = ["POST"])
def crear_usuario():
    
    datos = {
        "id" : request.form.get("id"),
        "email": request.form.get("email"),
        "contrasena" : request.form.get("contrasena"),
        "ruta_avatar" : request.form.get("ruta_avatar"),
        "activo" : request.form.get("activo")
    }  
    
    try:
        requests.post(API_URL, json = datos)
    except Exception as e:
        return f"Error al crear usuario {e}"
    
    return redirect(url_for("rutas_usuarios.usuarios"))  

        
        
@rutas_usuarios.route("/usuarios/actualizar", methods=["POST"])
def actualizar_usuario():
    
    id = request.form.get("id")
    datos = {
        "email": request.form.get("email"),
        "contrasena" : request.form.get("contrasena"),
        "ruta_avatar" : request.form.get("ruta_avatar"),
        "activo" : request.form.get("activo")
    }
    try:
        requests.put(f"{API_URL}/id/{id}", json=datos)
    except Exception as e:
        return f"Error al actualizar usuario {e}"
    
    return redirect(url_for("rutas_usuarios.usuarios"))


@rutas_usuarios.route("/usuarios/eliminar/<string:id>", methods=["POST"])
def eliminar_usuario(id):   
    try:
        requests.delete(f"{API_URL}/id/{id}")
    except Exception as e:
        return f"Error al eliminar usuario: {e}"
            
    return redirect(url_for("rutas_usuarios.usuarios"))
        