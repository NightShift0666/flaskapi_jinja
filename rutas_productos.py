from flask import Blueprint, render_template, request, redirect, url_for
import requests

rutas_productos = Blueprint("rutas_productos", __name__)

API_URL = "http://localhost:5031/api/producto"
API_TIPO_PRODUCTO = "http://localhost:5031/api/tipo_producto"

#-----Listar productos--------

@rutas_productos.route("/productos")
def productos():
    try:
        respuesta = requests.get(API_URL)
        productos = respuesta.json().get("datos",[])
        
        # Obtener tipo de producto para cada producto
        for producto in productos:
            producto['tipo_producto_info'] = obtener_tipo_producto(producto.get('id_tipo_producto'))
            
    except Exception as e:
        productos = []
        print("Error al conectar con la API", e)
    
    # Obtener todos los tipos de producto para el formulario
    try:
        respuesta_tipos = requests.get(API_TIPO_PRODUCTO)
        todos_tipos_producto = respuesta_tipos.json().get("datos", [])
    except Exception as e:
        todos_tipos_producto = []
        print("Error al obtener tipos de producto", e)
        
    return render_template(
        "productos.html",
        productos = productos,
        producto = None,
        todos_tipos_producto = todos_tipos_producto,
        modo = "crear"
    )        

# Funcion para obtener información del tipo de producto
def obtener_tipo_producto(id_tipo_producto):
    if not id_tipo_producto:
        return None
    try:
        respuesta = requests.get(f"{API_TIPO_PRODUCTO}/id/{id_tipo_producto}")
        datos = respuesta.json().get("datos", [])
        return datos[0] if datos else None
    except Exception as e:
        print(f"Error al obtener tipo de producto {id_tipo_producto}: {e}")
        return None
    
#------- Buscar producto --------

@rutas_productos.route("/productos/buscar", methods=["POST"])
def buscar_producto():
        
        id = request.form.get("id_buscar")
        
        if id:
            try:
                respuesta = requests.get(f"{API_URL}/id/{id}")
                if respuesta.status_code == 200:
                    datos = respuesta.json().get("datos", [])
                    if datos:
                        producto = datos[0]
                        # Obtener tipo de producto del producto encontrado
                        producto['tipo_producto_info'] = obtener_tipo_producto(producto.get('id_tipo_producto'))
                        
                        productos = requests.get(API_URL).json().get("datos", [])
                        # Obtener tipo de producto para cada producto de la lista
                        for p in productos:
                            p['tipo_producto_info'] = obtener_tipo_producto(p.get('id_tipo_producto'))
                        
                        # Obtener todos los tipos de producto
                        todos_tipos_producto = requests.get(API_TIPO_PRODUCTO).json().get("datos", [])
                        
                        return render_template(
                            "productos.html",
                            productos = productos,
                            producto = producto,
                            todos_tipos_producto = todos_tipos_producto,
                            modo = "actualizar"
                        )
                
            
            except Exception as e:
                return f"Error en la búsqueda: {e}"             
        
        productos = requests.get(API_URL).json().get("datos", [])
        for p in productos:
            p['tipo_producto_info'] = obtener_tipo_producto(p.get('id_tipo_producto'))
        todos_tipos_producto = requests.get(API_TIPO_PRODUCTO).json().get("datos", [])
        
        return render_template(
            "productos.html",
            productos=productos,
            producto=None,
            todos_tipos_producto=todos_tipos_producto,
            mensaje="Producto no encontrado",
            modo="crear"
        )       
        
        
# --------------- Crear producto ------------------

@rutas_productos.route("/productos/crear", methods=["POST"])
def crear_producto():
    
    datos ={
        "id_tipo_producto": request.form.get("id_tipo_producto"),
        "codigo": request.form.get("codigo"),
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion"),
        "fecha_inicio": request.form.get("fecha_inicio") or None,
        "fecha_fin_prevista": request.form.get("fecha_fin_prevista") or None,
        "fecha_modificacion": request.form.get("fecha_modificacion") or None,
        "fecha_finalizacion": request.form.get("fecha_finalizacion") or None,
        "ruta_logo": request.form.get("ruta_logo") or None
    }  
    
    try:
        respuesta = requests.post(API_URL, json=datos)
        if respuesta.status_code not in [200, 201]:
            return f"Error al crear producto: {respuesta.text}"
                
    except Exception as e:
        return f"Error al crear producto: {e}"
    
    return redirect(url_for("rutas_productos.productos"))    
            
            
            
# ------- Actualizar producto -----------
@rutas_productos.route("/producto/actualizar", methods=["POST"])
def actualizar_producto():
    
    id =  request.form.get("id")
    datos = {
        "id_tipo_producto": request.form.get("id_tipo_producto"),
        "codigo": request.form.get("codigo"),
        "titulo": request.form.get("titulo"),
        "descripcion": request.form.get("descripcion"),
        "fecha_inicio": request.form.get("fecha_inicio") or None,
        "fecha_fin_prevista": request.form.get("fecha_fin_prevista") or None,
        "fecha_modificacion": request.form.get("fecha_modificacion") or None,
        "fecha_finalizacion": request.form.get("fecha_finalizacion") or None,
        "ruta_logo": request.form.get("ruta_logo") or None
    }   
    
    try:
        respuesta = requests.put(f"{API_URL}/id/{id}", json=datos)
        if respuesta.status_code not in [200, 201]:
            return f"Error al actualizar producto: {respuesta.text}"
        
    except Exception as e:
        return f"Error al actualizar producto {e}"
    
    return redirect(url_for("rutas_productos.productos"))  


# -------- Eliminar producto ----------

@rutas_productos.route("/productos/eliminar/<string:id>", methods=["POST"])
def eliminar_producto(id):
    
    try:
        requests.delete(f"{API_URL}/id/{id}")       
    except Exception as e:
        return f"Error al eliminar producto: {e}"
    
    return redirect(url_for("rutas_productos.productos"))