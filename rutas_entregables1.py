from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_entregables = Blueprint("rutas_entregables", __name__)

API_URL = "http://localhost:5031/api/entregable"
API_RESPONSABLE_ENTREGABLE = "http://localhost:5031/api/responsable_entregable" 
API_RESPONSABLES = "http://localhost:5031/api/responsable"
API_PRODUCTO_ENTREGABLE = "http://localhost:5031/api/producto_entregable"
API_PRODUCTOS = "http://localhost:5031/api/producto"

#-----Listar entregables--------

@rutas_entregables.route("/entregables")
def entregables():
    try:
        respuesta = requests.get(API_URL)
        entregables = respuesta.json().get("datos",[])
        
        # Obtener responsables y productos para cada entregable
        for entregable in entregables:
            entregable['responsables'] = obtener_responsables_entregable(entregable['id'])
            entregable['productos'] = obtener_productos_entregable(entregable['id'])
            
    except Exception as e:
        entregables = []
        print("Error al conectar con la API", e)
    
    # Obtener todos los responsables y productos para los formularios de asignación
    try:
        respuesta_resp = requests.get(API_RESPONSABLES)
        todos_responsables = respuesta_resp.json().get("datos", [])
    except Exception as e:
        todos_responsables = []
        print("Error al obtener responsables", e)
    
    try:
        respuesta_prod = requests.get(API_PRODUCTOS)
        todos_productos = respuesta_prod.json().get("datos", [])
    except Exception as e:
        todos_productos = []
        print("Error al obtener productos", e)
        
    return render_template(
        "entregables.html",
        entregables = entregables,
        entregable = None,
        todos_responsables = todos_responsables,
        todos_productos = todos_productos,
        modo = "crear"
    )        

# Funcion para obtener responsables de un entregable
def obtener_responsables_entregable(id_entregable):
    try:
        respuesta = requests.get(f"{API_RESPONSABLE_ENTREGABLE}/id_entregable/{id_entregable}")
        return respuesta.json().get("datos", [])
    except Exception as e:
        print(f"Error al obtener responsables del entregable {id_entregable}: {e}")
        return []

# Funcion para obtener productos de un entregable
def obtener_productos_entregable(id_entregable):
    try:
        respuesta = requests.get(f"{API_PRODUCTO_ENTREGABLE}/id_entregable/{id_entregable}")
        return respuesta.json().get("datos", [])
    except Exception as e:
        print(f"Error al obtener productos del entregable {id_entregable}: {e}")
        return []
    
#------- Buscar entregable --------

@rutas_entregables.route("/entregables/buscar", methods=["POST"])
def buscar_entregable():
        
        id = request.form.get("id_buscar")
        
        if id:
            try:
                respuesta = requests.get(f"{API_URL}/id/{id}")
                if respuesta.status_code == 200:
                    datos = respuesta.json().get("datos", [])
                    if datos:
                        entregable = datos[0]
                        # Obtener responsables y productos del entregable encontrado
                        entregable['responsables'] = obtener_responsables_entregable(entregable['id'])
                        entregable['productos'] = obtener_productos_entregable(entregable['id'])
                        
                        entregables = requests.get(API_URL).json().get("datos", [])
                        # Obtener responsables y productos para cada entregable de la lista
                        for e in entregables:
                            e['responsables'] = obtener_responsables_entregable(e['id'])
                            e['productos'] = obtener_productos_entregable(e['id'])
                        
                        # Obtener todos los responsables y productos
                        todos_responsables = requests.get(API_RESPONSABLES).json().get("datos", [])
                        todos_productos = requests.get(API_PRODUCTOS).json().get("datos", [])
                        
                        return render_template(
                            "entregables.html",
                            entregables = entregables,
                            entregable = entregable,
                            todos_responsables = todos_responsables,
                            todos_productos = todos_productos,
                            modo = "actualizar"
                        )
                
            
            except Exception as e:
                return f"Error en la búsqueda: {e}"             
        
        entregables = requests.get(API_URL).json().get("datos", [])
        for e in entregables:
            e['responsables'] = obtener_responsables_entregable(e['id'])
            e['productos'] = obtener_productos_entregable(e['id'])
        todos_responsables = requests.get(API_RESPONSABLES).json().get("datos", [])
        todos_productos = requests.get(API_PRODUCTOS).json().get("datos", [])
        
        return render_template(
            "entregables.html",
            entregables=entregables,
            entregable=None,
            todos_responsables=todos_responsables,
            todos_productos=todos_productos,
            mensaje="Entregable no encontrado",
            modo="crear"
        )       
        
        
# --------------- Crear entregable ------------------

@rutas_entregables.route("/entregables/crear", methods=["POST"])
def crear_entregable():
    
    datos ={
        "codigo": request.form.get("codigo"),
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion"),
        "fecha_inicio": request.form.get("fecha_inicio"),
        "fecha_fin_prevista": request.form.get("fecha_fin_prevista"),
        "fecha_modificacion": request.form.get("fecha_modificacion"),
        "fecha_finalizacion": request.form.get("fecha_finalizacion")
    }  
    
    try:
        respuesta = requests.post(API_URL, json=datos)
        # Obtener el ID del entregable creado para asignar responsables y productos
        if respuesta.status_code == 200 or respuesta.status_code == 201:
            resultado = respuesta.json()
            id_entregable = resultado.get("id") or resultado.get("datos", {}).get("id")
            
            # Asignar responsables seleccionados
            responsables_seleccionados = request.form.getlist("responsables[]")
            if id_entregable and responsables_seleccionados:
                asignar_responsables(id_entregable, responsables_seleccionados)
            
            # Asignar productos seleccionados
            productos_seleccionados = request.form.getlist("productos[]")
            if id_entregable and productos_seleccionados:
                asignar_productos(id_entregable, productos_seleccionados)
                
    except Exception as e:
        return f"Error al crear entregable: {e}"
    
    return redirect(url_for("rutas_entregables.entregables"))    
            
            
            
# ------- Actualizar entregable -----------
@rutas_entregables.route("/entregable/actualizar", methods=["POST"])
def actualizar_entregable():
    
    id =  request.form.get("id")
    datos = {
        "codigo": request.form.get("codigo"),
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion"),
        "fecha_inicio": request.form.get("fecha_inicio"),
        "fecha_fin_prevista": request.form.get("fecha_fin_prevista"),
        "fecha_modificacion": request.form.get("fecha_modificacion"),
        "fecha_finalizacion": request.form.get("fecha_finalizacion")
        
    }   
    
    try:
        requests.put(f"{API_URL}/id/{id}", json=datos)
        
        # Actualizar responsables
        responsables_seleccionados = request.form.getlist("responsables[]")
        actualizar_responsables_entregable(id, responsables_seleccionados)
        
        # Actualizar productos
        productos_seleccionados = request.form.getlist("productos[]")
        actualizar_productos_entregable(id, productos_seleccionados)
        
    except Exception as e:
        return f"Error al actualizar entregable {e}"
    
    return redirect(url_for("rutas_entregables.entregables"))  


# -------- Eliminar entregable ----------

@rutas_entregables.route("/entregables/eliminar/<string:id>", methods=["POST"])
def eliminar_entregable(id):
    
    try:
        requests.delete(f"{API_URL}/id/{id}")       
    except Exception as e:
        return f"Error al eliminar entregable: {e}"
    
    return redirect(url_for("rutas_entregables.entregables"))


# -------- Funciones para gestionar responsables ----------

def asignar_responsables(id_entregable, lista_responsables):
    """Asigna responsables a un entregable"""
    
    from datetime import datetime
    for id_responsable in lista_responsables:
        try:
            datos = {
                "id_entregable": id_entregable,
                "id_responsable": id_responsable,
                "fecha_asociacion": datetime.now().isoformat()
            }
            requests.post(API_RESPONSABLE_ENTREGABLE, json=datos)
        except Exception as e:
            print(f"Error al asignar responsable {id_responsable}: {e}")

def actualizar_responsables_entregable(id_entregable, lista_responsables):
    """Actualiza los responsables de un entregable (elimina los anteriores y agrega los nuevos)"""
    try:
        # eliminar todas las asignaciones actuales
        requests.delete(f"{API_RESPONSABLE_ENTREGABLE}/id_entregable/{id_entregable}")
        
        # Luego agregar las nuevas
        asignar_responsables(id_entregable, lista_responsables)
    except Exception as e:
        print(f"Error al actualizar responsables: {e}")


# -------- Funciones para gestionar productos ----------

def asignar_productos(id_entregable, lista_productos):
    """Asigna productos a un entregable"""
    
    from datetime import datetime
    for id_producto in lista_productos:
        try:
            datos = {
                "id_entregable": id_entregable,
                "id_producto": id_producto,
                "fecha_asociacion": datetime.now().isoformat()
            }
            requests.post(API_PRODUCTO_ENTREGABLE, json=datos)
        except Exception as e:
            print(f"Error al asignar producto {id_producto}: {e}")

def actualizar_productos_entregable(id_entregable, lista_productos):
    """Actualiza los productos de un entregable (elimina los anteriores y agrega los nuevos)"""
    try:
        # eliminar todas las asignaciones actuales
        requests.delete(f"{API_PRODUCTO_ENTREGABLE}/id_entregable/{id_entregable}")
        
        # Luego agregar las nuevas
        asignar_productos(id_entregable, lista_productos)
    except Exception as e:
        print(f"Error al actualizar productos: {e}")