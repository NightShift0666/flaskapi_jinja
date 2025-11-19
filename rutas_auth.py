from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import requests
import hashlib

rutas_auth = Blueprint("rutas_auth", __name__)

API_USUARIOS = "http://localhost:5031/api/usuario"

def hash_password(password):
    """Genera el hash de la contraseña usando SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

#------- Página de Login --------
@rutas_auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        contrasena = request.form.get("contrasena")
        
        try:
            # Obtener todos los usuarios
            respuesta = requests.get(API_USUARIOS)
            usuarios = respuesta.json().get("datos", [])
            
            # Buscar usuario por email
            usuario_encontrado = None
            for usuario in usuarios:
                if usuario.get("email") == email:
                    usuario_encontrado = usuario
                    break
            
            if usuario_encontrado:
                # Verificar si el usuario está activo
                if not usuario_encontrado.get("activo", False):
                    flash("Usuario inactivo. Contacte al administrador.", "danger")
                    return render_template("login.html")
                
                # Verificar contraseña (comparar hash)
                hash_ingresado = hash_password(contrasena)
                if usuario_encontrado.get("contrasena") == hash_ingresado:
                    # Login exitoso
                    session["usuario_id"] = usuario_encontrado.get("id")
                    session["usuario_email"] = usuario_encontrado.get("email")
                    session["usuario_ruta_avatar"] = usuario_encontrado.get("ruta_avatar")
                    session["logged_in"] = True
                    
                    flash(f"¡Bienvenido {email}!", "success")
                    return redirect(url_for("acerca"))  # Redirigir a la página principal
                else:
                    flash("Contraseña incorrecta", "danger")
            else:
                flash("Usuario no encontrado", "danger")
                
        except Exception as e:
            flash(f"Error al conectar con el servidor: {e}", "danger")
    
    return render_template("login.html")


#------- Logout --------
@rutas_auth.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada exitosamente", "info")
    return redirect(url_for("rutas_auth.login"))


#------- Página de Registro --------
@rutas_auth.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        email = request.form.get("email")
        contrasena = request.form.get("contrasena")
        confirmar_contrasena = request.form.get("confirmar_contrasena")
        ruta_avatar = request.form.get("ruta_avatar", "/static/default-avatar.png")
        
        # Validaciones
        if contrasena != confirmar_contrasena:
            flash("Las contraseñas no coinciden", "danger")
            return render_template("registro.html")
        
        if len(contrasena) < 6:
            flash("La contraseña debe tener al menos 6 caracteres", "danger")
            return render_template("registro.html")
        
        try:
            # Verificar si el email ya existe
            respuesta = requests.get(API_USUARIOS)
            usuarios = respuesta.json().get("datos", [])
            
            for usuario in usuarios:
                if usuario.get("email") == email:
                    flash("El email ya está registrado", "danger")
                    return render_template("registro.html")
            
            # Crear nuevo usuario
            datos = {
                "email": email,
                "contrasena": hash_password(contrasena),
                "ruta_avatar": ruta_avatar,
                "activo": True
            }
            
            respuesta_crear = requests.post(API_USUARIOS, json=datos)
            
            if respuesta_crear.status_code == 200 or respuesta_crear.status_code == 201:
                flash("Usuario registrado exitosamente. Por favor inicia sesión.", "success")
                return redirect(url_for("rutas_auth.login"))
            else:
                flash("Error al registrar usuario", "danger")
                
        except Exception as e:
            flash(f"Error al conectar con el servidor: {e}", "danger")
    
    return render_template("registro.html")