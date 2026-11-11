app = Flask(__name__)
def conectar():
return mysql.connector.connect(
host=os.getenv("DB_HOST", "${{MySQL.MYSQLHOST}}"),
user=os.getenv("DB_USER", "${{MySQL.MYSQLUSER}}"),
password=os.getenv("DB_PASSWORD", "${{MySQL.MYSQLPASSWORD}}"),
database=os.getenv("DB_NAME", "${{MySQL.MYSQLDATABASE}}"),
port=int(os.getenv("DB_PORT", "${{MySQL.MYSQLPORT}}"))
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
app.run(debug=True
