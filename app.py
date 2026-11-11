
import os
import mysql.connector
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


from urllib.parse import urlparse, unquote

def conectar():
    mysql_url = os.getenv("MYSQL_URL")

    if not mysql_url:
        raise ValueError("No existe la variable MYSQL_URL")

    url = urlparse(mysql_url)

    return mysql.connector.connect(
        host=url.hostname,
        user=unquote(url.username or ""),
        password=unquote(url.password or ""),
        database=url.path.lstrip("/"),
        port=url.port or 3306
    )

@app.route("/")
def inicio():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM aprendices")
    aprendices = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("index.html", aprendices=aprendices)


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


@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM aprendices WHERE id = %s",
        (id,)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=False
    )
