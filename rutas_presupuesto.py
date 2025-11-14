from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_presupuesto = Blueprint("rutas_presupuesto", __name__)

API_URL = "http://localhost:5031/api/presupuesto"
API_PROYECTOS = "http://localhost:5031/api/proyecto"

#-----Listar presupuestos--------

@rutas_presupuesto.route("/presupuesto")
def presupuesto():
    try:
        respuesta = requests.get(API_URL)
        presupuestos = respuesta.json().get("datos",[])
    except Exception as e:
        presupuestos = []
        print("Error al conectar con la API", e)
    
    # Obtener proyectos
    try:
        respuesta_proyectos = requests.get(API_PROYECTOS)
        proyectos = respuesta_proyectos.json().get("datos", [])
    except Exception as e:
        proyectos = []
        print("Error al obtener proyectos", e)
        
    return render_template(
        "presupuesto.html",
        presupuestos = presupuestos,
        presupuesto_item = None,
        proyectos = proyectos,
        modo = "crear"
    )        
    
#------- Buscar presupuesto --------

@rutas_presupuesto.route("/presupuesto/buscar", methods=["POST"])
def buscar_presupuesto():
        
        id = request.form.get("id_buscar")
        
        if id:
            try:
                respuesta = requests.get(f"{API_URL}/id/{id}")
                if respuesta.status_code == 200:
                    datos = respuesta.json().get("datos", [])
                    if datos:
                        presupuesto_item = datos[0]
                        presupuestos = requests.get(API_URL).json().get("datos", [])
                        
                        # Obtener proyectos
                        proyectos = requests.get(API_PROYECTOS).json().get("datos", [])
                        
                        return render_template(
                            "presupuesto.html",
                            presupuestos = presupuestos,
                            presupuesto_item = presupuesto_item,
                            proyectos = proyectos,
                            modo = "actualizar"
                        )
                
            
            except Exception as e:
                return f"Error en la búsqueda: {e}"             
        
        presupuestos = requests.get(API_URL).json().get("datos", [])
        proyectos = requests.get(API_PROYECTOS).json().get("datos", [])
        
        return render_template(
            "presupuesto.html",
            presupuestos=presupuestos,
            presupuesto_item=None,
            proyectos=proyectos,
            mensaje="Presupuesto no encontrado",
            modo="crear"
        )       
        
        
# --------------- Crear presupuesto ------------------

@rutas_presupuesto.route("/presupuesto/crear", methods=["POST"])
def crear_presupuesto():
    
    datos = {
        "id_proyecto": request.form.get("id_proyecto"),
        "monto_solicitado": request.form.get("monto_solicitado"),
        "estado": request.form.get("estado"),
        "monto_aprobado": request.form.get("monto_aprobado") or None,
        "periodo_anio": request.form.get("periodo_anio"),
        "fecha_solicitud": request.form.get("fecha_solicitud"),
        "fecha_aprobacion": request.form.get("fecha_aprobacion") or None,
        "observaciones": request.form.get("observaciones") or None
    }  
    
    try:
        requests.post(API_URL, json=datos)  
    except Exception as e:
        return f"Error al crear presupuesto: {e}"
    
    return redirect(url_for("rutas_presupuesto.presupuesto"))    
            
            
            
# ------- Actualizar presupuesto -----------
@rutas_presupuesto.route("/presupuesto/actualizar", methods=["POST"])
def actualizar_presupuesto():
    
    id =  request.form.get("id")
    datos = {
        "id": request.form.get("id"),
        "id_proyecto": request.form.get("id_proyecto"),
        "monto_solicitado": request.form.get("monto_solicitado"),
        "estado": request.form.get("estado"),
        "monto_aprobado": request.form.get("monto_aprobado") or None,
        "periodo_anio": request.form.get("periodo_anio"),
        "fecha_solicitud": request.form.get("fecha_solicitud"),
        "fecha_aprobacion": request.form.get("fecha_aprobacion") or None,
        "observaciones": request.form.get("observaciones") or None
    }   
    
    try:
        requests.put(f"{API_URL}/id/{id}", json=datos)
    except Exception as e:
        return f"Error al actualizar presupuesto {e}"
    
    return redirect(url_for("rutas_presupuesto.presupuesto"))  


# -------- Eliminar presupuesto ----------

@rutas_presupuesto.route("/presupuesto/eliminar/<string:id>", methods=["POST"])
def eliminar_presupuesto(id):
    
    try:
        requests.delete(f"{API_URL}/id/{id}")       
    except Exception as e:
        return f"Error al eliminar presupuesto: {e}"
    
    return redirect(url_for("rutas_presupuesto.presupuesto"))