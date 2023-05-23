# Api da aplicação utilizando a biblioteca Flask em linguagem Python
# 

from flask import Flask, request, jsonify
import mysql.connector
import random

db = mysql.connector.connect(
    host='containers-us-west-115.railway.app',
    port='7206',
    user='root',
    password='K0Ea2j0sUxkpZa9wQhiU',
    database='railway'
)

app = Flask(__name__)

@app.route('/cadastro', methods=['POST'])
def cadastro():

    # Recebendo email e senha do usuário
    email = request.form['email']
    password = request.form['password']
    tipo_usuario = request.form['tipo_usuario']
    nome = request.form['nome']

    # Inicialiazação dos parâmetros para o banco de dados
    mycursor = db.cursor()
    # Insere um usuário novo no banco de dados
    sql_command = "INSERT INTO usuarios (email, senha, tipo_usuario, nome) VALUES (%s, %s, %s, %s)"
    values = (email, password, tipo_usuario, nome)
    try:
        mycursor.execute(sql_command, values)
    except:
        return jsonify({'cadastro': 'error'})
        
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
    sql_command = "SELECT email, senha FROM usuarios Where email = %s"
    value = (email,)
    mycursor.execute(sql_command, value)
    email_res = mycursor.fetchone()

    # Verefica se o retorno não foi nulo e se a senha inserida é igual a cadastrada
    if email_res is not None:
        senha_encontrada = email_res[1] #posicao da coluna da tabela do banco de dado
        if senha_encontrada == password:

            print("Logado com sucesso")
            return jsonify({'acesso': 'OK'})
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

    nome_comercial = request.form['nome_comercial'] #nomeComercial
    codigo_curso = request.form['codigo_curso'] #id_treinamento
    descricao = request.form['descricao'] #descricao
    carga_horaria = request.form['carga_horaria'] #cargaHoraria
    inicio_inscricoes = request.form['inicio_inscricoes'] #dataInicioInscricao
    final_inscricoes = request.form['final_inscricoes'] #dataFinalInscricao
    inicio_treinamentos = request.form['inicio_treinamentos'] #dataInicioTreinamento
    final_treinamentos = request.form['final_treinamentos'] #dataFinalTreinamento
    qnt_min = request.form['qnt_min'] ##ISSO DAQUI É UM INT %d minCandidatos
    qnt_max = request.form['qnt_max'] ##ISSO DAQUI É UM INT %d maxCandidatos
    qnt_atual = 0

    print(nome_comercial)

    mycursor = db.cursor()
    sql_command = "INSERT INTO treinamentos (Nome_Comercial, Codigo_curso, Descricao, Carga_horaria, Inicio_inscricoes, Final_inscricoes, Inicio_treinamentos, Final_treinamentos, qntd_min, qntd_max, qntd_atual) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
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
        #'Quantidade atual de alunos': qnt_atual
    }
    
    return jsonify({'Treinamento': treinamento})


@app.route('/entrar_treinamento', methods=['POST'])
def entrar_treinamento():
    email = request.form('email') #pega o email do usuario
    codigo_treinamento = request.form('codigo_curso') #pega o curso desejado

    mycursor = db.cursor()

    sql_command = "SELECT qntd_max, qntd_atual FROM treinamentos Where Codigo_curso = %s" #pega a quantidade maxima e atual do curso desejado
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
            sql_command = "UPDATE treinamentos where Codigo_curso = %s SET qntd_atual = qntd_atual + 1" #incrementa em 1 a quantidade atual no curso desejado
            value = (codigo_treinamento,)
            mycursor.execute(sql_command, value)
            db.commit()
            sql_command = "INSERT into treinamentos_alunos (email, codigo_treinamento, status) VALUES (%s, %s, %s)"
            value = (email, codigo_treinamento, 'Em andamento')
            mycursor.execute(sql_command, value)
            db.commit()
            print("%s Registrado com sucesso no curso %s", email, codigo_treinamento)
            return jsonify({'registro_treinamento': True}) #retorna True para o flutter

    else:
        return 'Quantidade máxima ou mínima nulas' #se for nulo

class Answers:
    def __init__(self, questao, pergunta, respostaDaAlternativaA, alternativaA, respostaDaAlternativaB, alternativaB, respostaDaAlternativaC, alternativaC):
        self.questao = questao
        self.pergunta = pergunta
        self.respostaDaAlternativaA = respostaDaAlternativaA
        self.alternativaA = alternativaA
        self.respostaDaAlternativaB = respostaDaAlternativaB
        self.alternativaB = alternativaB
        self.respostaDaAlternativaC = respostaDaAlternativaC
        self.alternativaC = alternativaC

@app.route('/criar_questao', methods=['POST'])
def criar_questao():
    mycursor = db.cursor()

         
    id_teste = request.form['id_treinamento_quiz']
    n_questao = request.form['questao']
    t_pergunta = request.form['pergunta']
    resposta_a = request.form['respostaDaAlternativaA']
    alternativa_a = request.form['alternativaA']
    resposta_b = request.form['respostaDaAlternativaB']
    alternativa_b = request.form['alternativaB']
    resposta_c = request.form['respostaDaAlternativaC']
    alternativa_c = request.form['alternativaC']      
                
    sql_command = "INSERT INTO questoes (id_teste, numero_questao, questao, resposta_a, resposta_b, resposta_c, alternativa_a, alternativa_b, alternativa_c) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (id_teste, n_questao, t_pergunta, resposta_a, resposta_b, resposta_c, alternativa_a, alternativa_b, alternativa_c)
    mycursor.execute(sql_command, values)
    db.commit()
                
    #resposta = {id_teste, n_questao, t_pergunta, resposta_a, alternativa_a, resposta_b, alternativa_b, resposta_c, alternativa_c}
        
    return jsonify({'message': 'Lista de objetos recebida com sucesso!'})

@app.route('/Corrigir_teste', methods=['POST'])
def Corrigir_Teste():
    respostas_corretas = 0 #numero de respostas corretas
    id_teste = 213023
    resp_list = [] #lista com as respostas do aluno
    email = request.form('email')
    mycursor = db.cursor()

    for i in resp_list:
        sql_command = "SELECT %s FROM questoes WHERE id_teste = %d and numero_questao = Questao %d"
        value = (resp_list[i], id_teste, i+1)
        mycursor.execute(sql_command, value)
        res = mycursor.fetchone()
        if res == True:
            respostas_corretas+=1
    if respostas_corretas >= (resp_list.len)/2:
        sql_command = "UPDATE treinamento_alunos SET status = %s"
        value = ('Aprovado',)
        mycursor.execute(sql_command, value)
        db.commit()
        return jsonify({'status': 'Aprovado'})
    else:
        sql_command = "UPDATE treinamento_alunos SET status = %s, justificativa = %s"
        value = ('Reprovado', 'Acertos insuficientes')
        mycursor.execute(sql_command, value)
        db.commit()

@app.route('/vaga_emprego', methods=['POST'])
def vaga_emprego():

    ##codigo_vaga = request.json.get('codigo_vaga') <-- ser gerado aqui
    titulo_vaga = request.form['titulo_vaga']
    empresa_oferece = request.form['empresa_oferece']
    descricao_vaga = request.form['descricao_vaga']
    pre_requisitos = request.form['pre_requisitos']
    salario_minimo = int(request.form['salario_minimo'])
    salario_maximo = int(request.form['salario_maximo'])
    

    print(titulo_vaga)
    print(empresa_oferece)
    print(descricao_vaga)
    print(pre_requisitos)
    print(salario_minimo)
    print(salario_maximo)

    mycursor = db.cursor()
    sql_command = "INSERT into vaga_emprego (Titulo_vaga, Empresa_oferece, Descricao_vaga, Pre_requisito, Salario_minimo, Salario_maximo) VALUES (%s, %s, %s, %s,  %s, %s)"
    values = (titulo_vaga, empresa_oferece, descricao_vaga, pre_requisitos, salario_minimo, salario_maximo)
    mycursor.execute(sql_command, values)
    db.commit()

    vaga_emprego = {
        'titulo_vaga': titulo_vaga,
        'empresa_oferece': empresa_oferece,
        'descricao_vaga': descricao_vaga,
        'pre_requisitos': pre_requisitos,
        'salario_minimo': salario_minimo,
        'salario_maximo': salario_maximo
    }
    return jsonify({'vaga_emprego': vaga_emprego})



@app.route('/entrar_vaga_emprego', methods=['POST'])
def entrar_vaga_emprego():

    #tabela que contém a relação entre a vaga e quem se inscreveu nela (por email)
    titulo_vaga = request.form('titulo_vaga')
    email = request.form('email')

    mycursor = db.cursor()
    sql_command = "Insert into vaga_emprego_candidatos (titulo_vaga, email) VALUES (%s, %s)"
    values = (titulo_vaga, email)
    mycursor.execute(sql_command, values)
    db.commit()

    return jsonify({'entrar_emprego_status': True})

@app.route('/Listar_inscritos_vaga', methods=['POST'])
def Listar_inscritos_vaga():
    titulo_vaga = request.form('titulo_vaga')
    mycursor = db.cursor()
    sql_command = "SELECT * from vaga_emprego_candidatos WHERE titulo_vaga = %s"
    values = (titulo_vaga,)
    mycursor.execute(sql_command, values)
    listar_inscritos_vaga = mycursor.fetchall()
    return jsonify({'listar_inscritos_vaga': listar_inscritos_vaga})


@app.route('/Historico_aluno', methods=['POST'])
def historico():
    email = request.form('email')
    mycursor = db.cursor()
    sql_command = "SELECT * from treinamentos_alunos WHERE email = %s" ##treinamento_alunos = (email (varchar), codigo_curso (varchar), status (varchar), justificativa (varchar))
    values = (email,)
    mycursor.execute(sql_command, values)
    historico = mycursor.fetchall()
    return jsonify({'Historico_aluno': historico})



@app.route('/Update_treinamentos', methods=['POST'])
def Update_treinamentos():
    mycursor = db.cursor()
    nome_comercial = request.form('nome_comercial')
    codigo_curso = request.form('codigo_curso')
    descricao = request.form('descricao')
    carga_horaria = request.form('carga_horaria')
    inicio_inscricoes = request.form('inicio_inscricoes')
    final_inscricoes = request.form('final_inscricoes')
    inicio_treinamentos = request.form('inicio_treinamentos')
    final_treinamentos = request.form('final_treinamentos')
    qnt_min = request.form('qnt_min') ##ISSO DAQUI É UM INT %d
    qnt_max = request.form('qnt_max') ##ISSO DAQUI É UM INT %d

    sql_command = "UPDATE treinamentos SET Nome_comercial = %s, Codigo_curso = %s, Descricao = %s, Carga_horaria = %s, Inicio_inscricoes = %s, Final_inscricoes = %s, Inicio_treinamento = %s, Final_treinamento = %s, qnt_min = %s, qnt_max = %s"
    values = (nome_comercial, codigo_curso, descricao, carga_horaria, inicio_inscricoes, final_inscricoes, inicio_treinamentos, final_treinamentos, qnt_min, qnt_max)
    mycursor.execute(sql_command, values)
    db.commit()




    return 'penes'

@app.route('/Delete_treinamentos', methods=['POST'])
def Delete_treinamentos():
    mycursor = db.cursor()
    codigo_curso = request.form('codigo_curso')
    sql_command = "DELETE * FROM treinamentos WHERE Codigo_curso = %s"
    values = (codigo_curso,)
    mycursor.execute(sql_command, values)
    db.commit()
    return 'penes'

app.run()

