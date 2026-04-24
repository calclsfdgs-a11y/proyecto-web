import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
def crear_db():
    conn = sqlite3.connect('reclamos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reclamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            problema TEXT,
            tipo TEXT
        )
    ''')
    conn.commit()
    conn.close()

crear_db()
reclamos = []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        nombre = request.form['nombre']
        problema = request.form['problema']
        tipo = request.form['tipo']

        conn = sqlite3.connect('reclamos.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO reclamos (nombre, problema, tipo) VALUES (?, ?, ?)',
               (nombre, problema, tipo))
        conn.commit()
        conn.close()

        return redirect('/')

    conn = sqlite3.connect('reclamos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nombre, problema, tipo FROM reclamos')
    reclamos = cursor.fetchall()
    conn.close()
    return render_template('index.html', reclamos=reclamos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
