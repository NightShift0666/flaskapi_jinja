from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_distribucion_presupuesto = Blueprint("rutas_distribucion_presupuesto", __name__)

API_URL = "http://localhost:5031/api/distribucion_presupuesto"
API_PRESUPUESTOS = "http://localhost:5031/api/presupuesto"
API_PROYECTOS = "http://localhost:5031/api/proyecto"

#-----Listar distribuciones presupuesto--------

@rutas_distribucion_presupuesto.route("/distribucion_presupuesto")
def distribucion_presupuesto():
    try:
        respuesta = requests.get(API_URL)
        distribuciones = respuesta.json().get("datos",[])
    except Exception as e:
        distribuciones = []
        print("Error al conectar con la API", e)
    
    # Obtener presupuestos
    try:
        respuesta_presupuestos = requests.get(API_PRESUPUESTOS)
        presupuestos = respuesta_presupuestos.json().get("datos", [])
    except Exception as e:
        presupuestos = []
        print("Error al obtener presupuestos", e)
    
    # Obtener proyectos
    try:
        respuesta_proyectos = requests.get(API_PROYECTOS)
        proyectos = respuesta_proyectos.json().get("datos", [])
    except Exception as e:
        proyectos = []
        print("Error al obtener proyectos", e)
        
    return render_template(
        "distribucion_presupuesto.html",
        distribuciones = distribuciones,
        distribucion = None,
        presupuestos = presupuestos,
        proyectos = proyectos,
        modo = "crear"
    )        
    
#------- Buscar distribución presupuesto --------

@rutas_distribucion_presupuesto.route("/distribucion_presupuesto/buscar", methods=["POST"])
def buscar_distribucion_presupuesto():
        
        id = request.form.get("id_buscar")
        
        if id:
            try:
                respuesta = requests.get(f"{API_URL}/id/{id}")
                if respuesta.status_code == 200:
                    datos = respuesta.json().get("datos", [])
                    if datos:
                        distribucion = datos[0]
                        distribuciones = requests.get(API_URL).json().get("datos", [])
                        
                        # Obtener presupuestos
                        presupuestos = requests.get(API_PRESUPUESTOS).json().get("datos", [])
                        
                        # Obtener proyectos
                        proyectos = requests.get(API_PROYECTOS).json().get("datos", [])
                        
                        return render_template(
                            "distribucion_presupuesto.html",
                            distribuciones = distribuciones,
                            distribucion = distribucion,
                            presupuestos = presupuestos,
                            proyectos = proyectos,
                            modo = "actualizar"
                        )
                
            
            except Exception as e:
                return f"Error en la búsqueda: {e}"             
        
        distribuciones = requests.get(API_URL).json().get("datos", [])
        presupuestos = requests.get(API_PRESUPUESTOS).json().get("datos", [])
        proyectos = requests.get(API_PROYECTOS).json().get("datos", [])
        
        return render_template(
            "distribucion_presupuesto.html",
            distribuciones=distribuciones,
            distribucion=None,
            presupuestos=presupuestos,
            proyectos=proyectos,
            mensaje="Distribución presupuesto no encontrada",
            modo="crear"
        )       
        
        
# --------------- Crear distribución presupuesto ------------------

@rutas_distribucion_presupuesto.route("/distribucion_presupuesto/crear", methods=["POST"])
def crear_distribucion_presupuesto():
    
    datos = {
        "presupuesto_padre_id": request.form.get("presupuesto_padre_id"),
        "proyecto_hijo_id": request.form.get("proyecto_hijo_id"),
        "monto_asignado": request.form.get("monto_asignado")
    }  
    
    try:
        requests.post(API_URL, json=datos)  
    except Exception as e:
        return f"Error al crear distribución presupuesto: {e}"
    
    return redirect(url_for("rutas_distribucion_presupuesto.distribucion_presupuesto"))    
            
            
            
# ------- Actualizar distribución presupuesto -----------
@rutas_distribucion_presupuesto.route("/distribucion_presupuesto/actualizar", methods=["POST"])
def actualizar_distribucion_presupuesto():
    
    id =  request.form.get("id")
    datos = {
        "id": request.form.get("id"),
        "presupuesto_padre_id": request.form.get("presupuesto_padre_id"),
        "proyecto_hijo_id": request.form.get("proyecto_hijo_id"),
        "monto_asignado": request.form.get("monto_asignado")
    }   
    
    try:
        requests.put(f"{API_URL}/id/{id}", json=datos)
    except Exception as e:
        return f"Error al actualizar distribución presupuesto {e}"
    
    return redirect(url_for("rutas_distribucion_presupuesto.distribucion_presupuesto"))  


# -------- Eliminar distribución presupuesto ----------

@rutas_distribucion_presupuesto.route("/distribucion_presupuesto/eliminar/<string:id>", methods=["POST"])
def eliminar_distribucion_presupuesto(id):
    
    try:
        requests.delete(f"{API_URL}/id/{id}")       
    except Exception as e:
        return f"Error al eliminar distribución presupuesto: {e}"
    
    return redirect(url_for("rutas_distribucion_presupuesto.distribucion_presupuesto"))