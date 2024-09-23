from flask import Flask, render_template, request
import sqlparse

app = Flask(__name__)

def analizar_consulta(sql):
    parsed = sqlparse.parse(sql)
    query = parsed[0]
    
    sugerencias = []
    
    if "SELECT *" in str(query).upper():
        sugerencias.append("Evita usar 'SELECT *', especifica solo las columnas necesarias.")
    
    if "WHERE" not in str(query).upper():
        sugerencias.append("Añade cláusulas WHERE para reducir la cantidad de datos procesados.")
    else:
        if any(func in str(query).upper() for func in ["UPPER(", "LOWER(", "SUBSTR(", "LENGTH(", "TRIM("]):
            sugerencias.append("Evita usar funciones en las condiciones del WHERE, ya que pueden evitar el uso de índices.")
        
        if "OR" in str(query).upper():
            sugerencias.append("El uso de 'OR' en el WHERE puede afectar el uso de índices. Considera separar las condiciones.")
    
    if "JOIN" in str(query).upper():
        sugerencias.append("Revisa los índices de las columnas usadas en los JOINs para evitar operaciones costosas.")
    
    if "ORDER BY" in str(query).upper():
        sugerencias.append("Asegúrate de que las columnas en 'ORDER BY' estén indexadas para mejorar el rendimiento.")
    
    if "GROUP BY" in str(query).upper():
        sugerencias.append("Revisa los índices de las columnas utilizadas en 'GROUP BY'.")
    
    if "SELECT" in str(query).upper() and "FROM (" in str(query).upper():
        sugerencias.append("Considera utilizar JOINs en lugar de subconsultas para mejorar el rendimiento.")
    
    if "LIMIT" not in str(query).upper():
        sugerencias.append("Considera usar LIMIT para limitar el número de filas devueltas, especialmente en consultas grandes.")

    if "DISTINCT" in str(query).upper():
        sugerencias.append("Revisa si el uso de DISTINCT es necesario, ya que puede afectar el rendimiento.")
    
    if any(keyword in str(query).upper() for keyword in ["INSERT", "UPDATE", "DELETE"]):
        sugerencias.append("Asegúrate de usar transacciones para garantizar la integridad de los datos.")

    return sugerencias

@app.route('/', methods=['GET', 'POST'])
def index():
    sugerencias = []
    consulta_sql = ""
    
    if request.method == 'POST':
        consulta_sql = request.form['consulta']
        sugerencias = analizar_consulta(consulta_sql)
        
    return render_template('index.html', consulta=consulta_sql, sugerencias=sugerencias)
if __name__ == '__main__':
    app.run(debug=True)
