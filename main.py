# Api da aplicação utilizando a biblioteca Flask em linguagem Python
# 

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
def cadastro():

    # Recebendo email e senha do usuário
    email = request.form['email']
    password = request.form['password']

    # Inicialiazação dos parâmetros para o banco de dados
    mycursor = db.cursor()
    # Insere um usuário novo no banco de dados
    sql_command = "INSERT INTO users (email, senha, tipo_usuario, nome) VALUES (%s, %s, %s, %s)"
    values = (email, password, 'Aluno', 'name')
    mycursor.execute(sql_command, values)
    # Salvas as alterações feitas no banco de dados
    db.commit()

    print(email)
    print(password)
    # Retorna um valor para o frontend
    return jsonify({'cadastro': 'OK'})







@app.route('/login', methods=['POST'])
def login():

    # Recebendo email e senha do usuário
    email = request.form['email']
    password = request.form['password']
    
    # Inicialiazação dos parâmetros para o banco de dados
    mycursor = db.cursor()

    # Procura no banco de dados um usuário com o email que foi passado
    sql_command = "SELECT email, senha FROM users Where email = %s"
    value = (email,)
    mycursor.execute(sql_command, value)
    email_res = mycursor.fetchone()

    # Verefica se o retorno não foi nulo e se a senha inserida é igual a cadastrada
    if email_res is not None:
        senha_encontrada = email_res[1] #posicao da coluna da tabela do banco de dado
        if senha_encontrada == password:
            tipo_user = email_res[2]
            print("Logado com sucesso")
            return jsonify({'acesso': 'OK', 'tipo_usuario': tipo_user})
        else:
            print("Senha incorreta")
    else:
        print("Email nao encontrado")

    return jsonify({'acesso': 'false'})





@app.route('/teste_tdd', methods=['POST'])
def teste_tdd():

    #TESTE AUTOMATIZADO
    #Verefica a existencia de um login

    # Recebendo email e senha do usuário
    email = request.json.get('email')
    password = request.json.get('password')

    # Inicialiazação dos parâmetros para o banco de dados
    mycursor = db.cursor()

    # Procura no banco de dados um usuário com o email que foi passado
    sql_command = "SELECT email, senha FROM usuarios Where email = %s"
    value = (email,)
    mycursor.execute(sql_command, value)
    email_res = mycursor.fetchone()
    if email_res is not None:
        senha_encontrada = email_res[1]
        if senha_encontrada == password:
            print("Logado com sucesso")
            return jsonify({'acesso': 'true'})
    else:
        return jsonify({'acesso': 'false'})
    


    
    
@app.route('/criar_treinamento', methods=['POST'])
def treinamento():
    nome_comercial = request.json.get('nome_comercial')
    codigo_curso = request.json.get('codigo_curso')
    descricao = request.json.get('descricao')
    carga_horaria = request.json.get('carga_horaria')
    inicio_inscricoes = request.json.get('inicio_inscricoes')
    final_inscricoes = request.json.get('final_inscricoes')
    inicio_treinamentos = request.json.get('inicio_treinamentos')
    final_treinamentos = request.json.get('final_treinamentos')
    qnt_min = request.json.get('qnt_min') ##ISSO DAQUI É UM INT %d
    qnt_max = request.json.get('qnt_max') ##ISSO DAQUI É UM INT %d
    qnt_atual = request.json.get('qnt_atual') ##ISSO DAQUI É UM INT %d

    mycursor = db.cursor()
    sql_command = "INSERT INTO treinamentos (Nome_Comercial, Codigo_curso, Descricao, Carga_horaria, Inicio_inscricoes, Final_inscricoes, Inicio_treinamentos, Final_treinamentos, qntd_min, qntd_max, qntd_atual) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %d, %d, %d)"
    values = (nome_comercial, codigo_curso, descricao, carga_horaria, inicio_inscricoes, final_inscricoes, inicio_treinamentos, final_treinamentos, qnt_min, qnt_max, qnt_atual)
    mycursor.execute(sql_command, values)
    db.commit()
    
    treinamento = {
        'Nome Comercial': nome_comercial,
        'Código do Curso': codigo_curso,
        'Descricao': descricao,
        'Carga Horária': carga_horaria,
        'Início das incricoes': inicio_inscricoes,
        'Final das inscricoes': final_inscricoes,
        'Início dos treinamentos': inicio_treinamentos,
        'Final dos treinamentos': final_treinamentos,
        'Quantidade mínima de alunos': qnt_min,
        'Quantidade máxima de alunos': qnt_max,
        'Quantidade atual de alunos': qnt_atual
    }

    return jsonify({'Treinamento': treinamento})


@app.route('/entrar_treinamento', methods=['POST'])
def entrar_treinamento():
    email = request.json.get('email') #pega o email do usuario
    codigo_treinamento = request.json.get('codigo_curso') #pega o curso desejado

    mycursor = db.cursor()

    sql_command = "SELECT qntd_max, qntd_atual FROM treinamentos Where codigo_curso = %s" #pega a quantidade maxima e atual do curso desejado
    value = (codigo_treinamento,)
    mycursor.execute(sql_command, value)
    qnt_max_min = mycursor.fetchone()

    if qnt_max_min is not None: #se o valor nao for nulo
        qnt_atual = qnt_max_min[1] #qnt_atual recebe a quantidade atual do curso desejado
        qnt_max = qnt_max_min[0] #qnt_max recebe a quantidade maxima do curso desejado

        if qnt_atual >= qnt_max: #se o curso esta cheio
            print("Curso cheio")
            return jsonify({'registro_treinamento': False})
        else: #se ainda há vagas disponíveis
            sql_command = "UPDATE treinamentos where codigo_curso = %s SET qntd_atual = qntd_atual + 1" #incrementa em 1 a quantidade atual no curso desejado
            value = (codigo_treinamento,)
            mycursor.execute(sql_command, value)
            db.commit()
            print("%s Registrado com sucesso no curso %s", email, codigo_treinamento)
            return jsonify({'registro_treinamento': True}) #retorna True para o flutter

    else:
        return 'Quantidade máxima ou mínima nulas' #se for nulo

@app.route('/Criar_Teste', methods=['POST'])
def Criar_Teste():

    mycursor = db.cursor()
    Nome_teste = request.json.get('nome_teste')
    Codigo_curso = request.json.get('codigo_curso')
    num_questao = request.json.get('num_questao')
    quantidade_questoes = 5
    quantidade_alternativas = 3

    Questao: request.json.get('Questao')
    Alternativa_1: request.json.get('Q1_A')
    Alternativa_2: request.json.get('Q2_A')
    Alternativa_3: request.json.get('Q3_A')
    Resposta_Q: request.json.get('Q_R')


    sql_command = "INSERT INTO questoes (nome_teste, codigo_curso, num_questao, q_enunciado, A1, A2, A3, Resp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    value = (Nome_teste, Codigo_curso, num_questao, Questao, Alternativa_1, Alternativa_2, Alternativa_3, Resposta_Q)
    mycursor.execute(sql_command, value)
    db.commit()

    return 0




@app.route('/vaga_emprego', methods=['POST'])
def vaga_emprego():

    codigo_vaga = request.json.get('codigo_vaga')
    titulo_vaga = request.json.get('titulo_vaga')
    empresa_oferece = request.json.get('empresa_oferece')
    descricao_vaga = request.json.get('descricao_vaga')
    pre_requisitos = request.json.get('pre_requisitos')
    salario = request.json.get('salario')

    mycursor = db.cursor()
    sql_command = "Insert into vaga_emprego (Titulo_vaga, Empresa_oferece, Descricao_vaga, Pre_requisito, Salario) VALUES (%s, %s, %s, %s,  %d)"
    values = (titulo_vaga, empresa_oferece, descricao_vaga, pre_requisitos, salario)
    mycursor.execute(sql_command, values)
    db.commit()


    vaga_emprego = {
        'titulo_vaga': titulo_vaga,
        'titulo_vaga': titulo_vaga,
        'descricao_vaga': descricao_vaga,
        'pre_requisitos': pre_requisitos,
        'salario': salario,
    }


    return jsonify({'vaga_emprego': vaga_emprego})

app.run()

