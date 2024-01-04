"""
Módulo principal para la aplicación Flask.

Este módulo incluye la configuración inicial y las importaciones necesarias
para la aplicación Flask, así como la configuración de la conexión con Redis
y la gestión del tiempo.

Contiene:
- time: Módulo para trabajar con funciones relacionadas con el tiempo.
- redis: Cliente de Redis para interactuar con la base de datos en memoria.
- Flask: Clase principal para la creación de la aplicación web.

"""
import time
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)
def get_hit_count():
    """
    Obtiene el número de visitas desde la caché.

    La función utiliza el método 'incr' de la caché para incrementar
    el contador de visitas. Si hay un error de conexión, la función
    realiza varios intentos antes de lanzar una excepción.

    Returns:
        int: Número de visitas.
    """
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)
@app.route('/')
def hello():
    """
    Obtiene el número de visitas y devuelve un saludo con la cantidad de visitas.

    Returns:
        str: Saludo con el número de visitas.
    """
    count = get_hit_count()
    return f'Hola! Este sitio se ha visitado checkout {count} veces.\n'
