from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_ejecucion_presupuesto = Blueprint("rutas_ejecucion_presupuesto", __name__)

API_URL = "http://localhost:5031/api/ejecucion_presupuesto"
API_PRESUPUESTOS = "http://localhost:5031/api/presupuesto"

#-----Listar ejecuciones presupuesto--------

@rutas_ejecucion_presupuesto.route("/ejecucion_presupuesto")
def ejecucion_presupuesto():
    try:
        respuesta = requests.get(API_URL)
        ejecuciones = respuesta.json().get("datos",[])
    except Exception as e:
        ejecuciones = []
        print("Error al conectar con la API", e)
    
    # Obtener presupuestos
    try:
        respuesta_presupuestos = requests.get(API_PRESUPUESTOS)
        presupuestos = respuesta_presupuestos.json().get("datos", [])
    except Exception as e:
        presupuestos = []
        print("Error al obtener presupuestos", e)
        
    return render_template(
        "ejecucion_presupuesto.html",
        ejecuciones = ejecuciones,
        ejecucion = None,
        presupuestos = presupuestos,
        modo = "crear"
    )        
    
#------- Buscar ejecución presupuesto --------

@rutas_ejecucion_presupuesto.route("/ejecucion_presupuesto/buscar", methods=["POST"])
def buscar_ejecucion_presupuesto():
        
        id = request.form.get("id_buscar")
        
        if id:
            try:
                respuesta = requests.get(f"{API_URL}/id/{id}")
                if respuesta.status_code == 200:
                    datos = respuesta.json().get("datos", [])
                    if datos:
                        ejecucion = datos[0]
                        ejecuciones = requests.get(API_URL).json().get("datos", [])
                        
                        # Obtener presupuestos
                        presupuestos = requests.get(API_PRESUPUESTOS).json().get("datos", [])
                        
                        return render_template(
                            "ejecucion_presupuesto.html",
                            ejecuciones = ejecuciones,
                            ejecucion = ejecucion,
                            presupuestos = presupuestos,
                            modo = "actualizar"
                        )
                
            
            except Exception as e:
                return f"Error en la búsqueda: {e}"             
        
        ejecuciones = requests.get(API_URL).json().get("datos", [])
        presupuestos = requests.get(API_PRESUPUESTOS).json().get("datos", [])
        
        return render_template(
            "ejecucion_presupuesto.html",
            ejecuciones=ejecuciones,
            ejecucion=None,
            presupuestos=presupuestos,
            mensaje="Ejecución presupuesto no encontrada",
            modo="crear"
        )       
        
        
# --------------- Crear ejecución presupuesto ------------------

@rutas_ejecucion_presupuesto.route("/ejecucion_presupuesto/crear", methods=["POST"])
def crear_ejecucion_presupuesto():
    
    datos = {
        "presupuesto_id": request.form.get("presupuesto_id"),
        "anio": request.form.get("anio"),
        "monto_planeado": request.form.get("monto_planeado"),
        "monto_ejecutado": request.form.get("monto_ejecutado"),
        "observaciones": request.form.get("observaciones") or None
    }  
    
    try:
        requests.post(API_URL, json=datos)  
    except Exception as e:
        return f"Error al crear ejecución presupuesto: {e}"
    
    return redirect(url_for("rutas_ejecucion_presupuesto.ejecucion_presupuesto"))    
            
            
            
# ------- Actualizar ejecución presupuesto -----------
@rutas_ejecucion_presupuesto.route("/ejecucion_presupuesto/actualizar", methods=["POST"])
def actualizar_ejecucion_presupuesto():
    
    id =  request.form.get("id")
    datos = {
        "id": request.form.get("id"),
        "presupuesto_id": request.form.get("presupuesto_id"),
        "anio": request.form.get("anio"),
        "monto_planeado": request.form.get("monto_planeado"),
        "monto_ejecutado": request.form.get("monto_ejecutado"),
        "observaciones": request.form.get("observaciones") or None
    }   
    
    try:
        requests.put(f"{API_URL}/id/{id}", json=datos)
    except Exception as e:
        return f"Error al actualizar ejecución presupuesto {e}"
    
    return redirect(url_for("rutas_ejecucion_presupuesto.ejecucion_presupuesto"))  


# -------- Eliminar ejecución presupuesto ----------

@rutas_ejecucion_presupuesto.route("/ejecucion_presupuesto/eliminar/<string:id>", methods=["POST"])
def eliminar_ejecucion_presupuesto(id):
    
    try:
        requests.delete(f"{API_URL}/id/{id}")       
    except Exception as e:
        return f"Error al eliminar ejecución presupuesto: {e}"
    
    return redirect(url_for("rutas_ejecucion_presupuesto.ejecucion_presupuesto"))