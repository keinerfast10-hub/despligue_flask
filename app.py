import os
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)


# Conexión con MySQL (usa variables de entorno; valores por defecto para uso local)
def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "institucion"),
        port=int(os.getenv("DB_PORT", "3306")),
    )


# Página principal
@app.route("/")
def inicio():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM aprendices")
    aprendices = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template("index.html", aprendices=aprendices)


# Registrar aprendiz
@app.route("/registrar", methods=["POST"])
def registrar():
    nombre = request.form["nombre"]
    correo = request.form["correo"]
    conexion = conectar()
    cursor = conexion.cursor()
    sql = """
        INSERT INTO aprendices (nombre, correo)
        VALUES (%s, %s)
    """
    cursor.execute(sql, (nombre, correo))
    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect("/")


# Eliminar aprendiz (POST, no GET)
@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM aprendices WHERE id = %s", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect("/")


if __name__ == "__main__":
    # Solo para pruebas locales. En Railway se usa Gunicorn (ver Procfile).
    app.run(debug=os.getenv("FLASK_DEBUG", "1") == "1")
