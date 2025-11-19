# Importar la clase principal de Flask y la función para renderizar plantillas
from flask import Flask, render_template
from flask import Flask, session
from rutas_auth import rutas_auth
from middleware_auth import login_required

# Importar el Blueprint que contiene las rutas de productos
from rutas_productos import rutas_productos
from rutas_tipos_producto import rutas_tipos_producto
from rutas_entregables1 import rutas_entregables
from rutas_tipo_responsable import rutas_tipos_responsable
from rutas_tipos_proyecto import rutas_tipos_proyecto
from rutas_usuarios import rutas_usuarios
from rutas_variables_estrategicas import rutas_variables_estrategicas
from rutas_estados import rutas_estados
from rutas_responsables import rutas_responsables
from rutas_actividades import rutas_actividades
from rutas_presupuesto import rutas_presupuesto
from rutas_objetivo_estrategico import rutas_objetivo_estrategico
from rutas_ejecucion_presupuesto import rutas_ejecucion_presupuesto
from rutas_distribucion_presupuesto import rutas_distribucion_presupuesto
from rutas_proyectos import rutas_proyectos


# Crear la instancia de la aplicación Flask
aplicacion = Flask(__name__)
aplicacion.secret_key = "tu_clave_secreta_super_segura_12345"

# ------------------- Registro de Blueprints -------------------
# Registrar el Blueprint de productos en la aplicación principal
aplicacion.register_blueprint(rutas_productos)
aplicacion.register_blueprint(rutas_tipos_producto)
aplicacion.register_blueprint(rutas_entregables)
aplicacion.register_blueprint(rutas_tipos_responsable)
aplicacion.register_blueprint(rutas_tipos_proyecto)
aplicacion.register_blueprint(rutas_usuarios)
aplicacion.register_blueprint(rutas_variables_estrategicas)
aplicacion.register_blueprint(rutas_estados)
aplicacion.register_blueprint(rutas_responsables)
aplicacion.register_blueprint(rutas_actividades)
aplicacion.register_blueprint(rutas_presupuesto)
aplicacion.register_blueprint(rutas_objetivo_estrategico)
aplicacion.register_blueprint(rutas_ejecucion_presupuesto)
aplicacion.register_blueprint(rutas_distribucion_presupuesto)
aplicacion.register_blueprint(rutas_proyectos)





aplicacion.register_blueprint(rutas_auth)



# ------------------- Rutas principales -------------------

@aplicacion.route("/")
@login_required
def inicio():
    """
    Función asociada a la ruta principal (/).
    Retorna la plantilla index.html.
    """
    return render_template("index.html")


@aplicacion.route("/acerca")
def acerca():
    """
    Función asociada a la ruta /acerca.
    Retorna la plantilla acerca.html con información sobre el proyecto.
    """
    return render_template("acerca.html")

# ---------------------------------------------------------

# Punto de entrada de la aplicación
if __name__ == "__main__":
    # Ejecutar la aplicación en modo depuración, en el puerto 5000
    # host="0.0.0.0" permite que la app sea accesible desde la red local
    # debug=True permite reinicio automático ante cambios
    aplicacion.run(host="0.0.0.0", port=5000, debug=True)
