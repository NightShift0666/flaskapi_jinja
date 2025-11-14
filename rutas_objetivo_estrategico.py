from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_objetivo_estrategico = Blueprint("rutas_objetivo_estrategico", __name__)

API_URL = "http://localhost:5031/api/objetivo_estrategico"
API_VARIABLES_ESTRATEGICAS = "http://localhost:5031/api/variable_estrategica"

#-----Listar objetivos estratégicos--------

@rutas_objetivo_estrategico.route("/objetivo_estrategico")
def objetivo_estrategico():
    try:
        respuesta = requests.get(API_URL)
        objetivos = respuesta.json().get("datos",[])
    except Exception as e:
        objetivos = []
        print("Error al conectar con la API", e)
    
    # Obtener variables estratégicas
    try:
        respuesta_variables = requests.get(API_VARIABLES_ESTRATEGICAS)
        variables_estrategicas = respuesta_variables.json().get("datos", [])
    except Exception as e:
        variables_estrategicas = []
        print("Error al obtener variables estratégicas", e)
        
    return render_template(
        "objetivo_estrategico.html",
        objetivos = objetivos,
        objetivo = None,
        variables_estrategicas = variables_estrategicas,
        modo = "crear"
    )        
    
#------- Buscar objetivo estratégico --------

@rutas_objetivo_estrategico.route("/objetivo_estrategico/buscar", methods=["POST"])
def buscar_objetivo_estrategico():
        
        id = request.form.get("id_buscar")
        
        if id:
            try:
                respuesta = requests.get(f"{API_URL}/id/{id}")
                if respuesta.status_code == 200:
                    datos = respuesta.json().get("datos", [])
                    if datos:
                        objetivo = datos[0]
                        objetivos = requests.get(API_URL).json().get("datos", [])
                        
                        # Obtener variables estratégicas
                        variables_estrategicas = requests.get(API_VARIABLES_ESTRATEGICAS).json().get("datos", [])
                        
                        return render_template(
                            "objetivo_estrategico.html",
                            objetivos = objetivos,
                            objetivo = objetivo,
                            variables_estrategicas = variables_estrategicas,
                            modo = "actualizar"
                        )
                
            
            except Exception as e:
                return f"Error en la búsqueda: {e}"             
        
        objetivos = requests.get(API_URL).json().get("datos", [])
        variables_estrategicas = requests.get(API_VARIABLES_ESTRATEGICAS).json().get("datos", [])
        
        return render_template(
            "objetivo_estrategico.html",
            objetivos=objetivos,
            objetivo=None,
            variables_estrategicas=variables_estrategicas,
            mensaje="Objetivo estratégico no encontrado",
            modo="crear"
        )       
        
        
# --------------- Crear objetivo estratégico ------------------

@rutas_objetivo_estrategico.route("/objetivo_estrategico/crear", methods=["POST"])
def crear_objetivo_estrategico():
    
    datos = {
        "id_var": request.form.get("id_var"),
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion")
    }  
    
    try:
        requests.post(API_URL, json=datos)  
    except Exception as e:
        return f"Error al crear objetivo estratégico: {e}"
    
    return redirect(url_for("rutas_objetivo_estrategico.objetivo_estrategico"))    
            
            
            
# ------- Actualizar objetivo estratégico -----------
@rutas_objetivo_estrategico.route("/objetivo_estrategico/actualizar", methods=["POST"])
def actualizar_objetivo_estrategico():
    
    id =  request.form.get("id")
    datos = {
        "id": request.form.get("id"),
        "id_var": request.form.get("id_var"),
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion")
    }   
    
    try:
        requests.put(f"{API_URL}/id/{id}", json=datos)
    except Exception as e:
        return f"Error al actualizar objetivo estratégico {e}"
    
    return redirect(url_for("rutas_objetivo_estrategico.objetivo_estrategico"))  


# -------- Eliminar objetivo estratégico ----------

@rutas_objetivo_estrategico.route("/objetivo_estrategico/eliminar/<string:id>", methods=["POST"])
def eliminar_objetivo_estrategico(id):
    
    try:
        requests.delete(f"{API_URL}/id/{id}")       
    except Exception as e:
        return f"Error al eliminar objetivo estratégico: {e}"
    
    return redirect(url_for("rutas_objetivo_estrategico.objetivo_estrategico"))