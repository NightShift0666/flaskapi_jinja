from flask import session, redirect, url_for, flash
from functools import wraps

def login_required(f):
    """
    Decorador para proteger rutas que requieren autenticación.
    Uso: @login_required encima de la función de la ruta
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Debes iniciar sesión para acceder a esta página', 'warning')
            return redirect(url_for('rutas_auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def logout_required(f):
    """
    Decorador para rutas que solo pueden acceder usuarios NO autenticados.
    Por ejemplo, login y registro.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in'):
            flash('Ya has iniciado sesión', 'info')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function