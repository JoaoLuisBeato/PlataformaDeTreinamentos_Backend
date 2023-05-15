from flask import Flask, request, jsonify
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="dkv79122",
  database="usuario"
)

app = Flask(__name__)

@app.route('/cadastro', methods=['POST'])
def hello():
    email = request.form['email']
    password = request.form['password']

    mycursor = db.cursor()

    sql_command = "INSERT INTO usuarios (email, senha, tipo_usuario) VALUES (%s, %s, %s)"
    values = (email, password, 'Aluno')

    mycursor.execute(sql_command, values)
    db.commit()

    print(email)
    print(password)

    return 'Chegou a api'

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    mycursor = db.cursor()

    sql_command = "SELECT email, senha FROM usuarios Where email = %s"
    value = (email,)
    mycursor.execute(sql_command, value)
    email_res = mycursor.fetchone()
    if email_res is not None:
        senha_encontrada = email_res[1]
        if senha_encontrada == password:
            print("Logado com sucesso")
            return jsonify({'acesso': 'True'})
        else:
            print("Senha incorreta")

    else:
        print("Email nao encontrado")

    return 'x'
app.run()
    

