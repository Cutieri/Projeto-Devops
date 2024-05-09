from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

def connect_to_database():
    conn = sqlite3.connect('inventario.db')
    return conn

def add_server(nome, endereco_ip, sistema_operacional=None, especificacoes_hardware=None):
    conn = connect_to_database()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO servidores (nome, endereco_ip, sistema_operacional, especificacoes_hardware) "
        "VALUES (?, ?, ?, ?)",
        (nome, endereco_ip, sistema_operacional, especificacoes_hardware)
    )
    
    conn.commit()
    
    conn.close()


def list_servers():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM servidores")
    servers = cursor.fetchall()
    conn.close()
    return servers

def update_server(server_id, nome, ip_address, operating_system=None):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE servidores SET nome = ?, ip_address = ?, operating_system = ? WHERE id = ?",
        (nome, ip_address, operating_system, server_id)
    )
    conn.commit()
    conn.close()

def remove_server(server_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM servidores WHERE id = ?", (server_id,))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    servers = list_servers()
    return render_template('index.html', servers=servers)
        
@app.route('/add_server', methods=['POST'])
def add_server_route():
    nome = request.form.get('nome')
    endereco_ip = request.form.get('endereco_ip')
    sistema_operacional = request.form.get('sistema_operacional', None)
    especificacoes_hardware = request.form.get('especificacoes_hardware', None)
    
    add_server(nome, endereco_ip, sistema_operacional, especificacoes_hardware)
    
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
