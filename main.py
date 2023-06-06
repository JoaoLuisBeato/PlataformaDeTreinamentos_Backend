# Api da aplicação utilizando a biblioteca Flask em linguagem Python
from flask import Flask, request, jsonify
import mysql.connector
import ast;

#Rotas e parâmetros de acesso ao nosso banco de dados - MySQL
#hospedado na plataforma railway
db = mysql.connector.connect(
    host='containers-us-west-115.railway.app',
    port='7206',
    user='root',
    password='K0Ea2j0sUxkpZa9wQhiU',
    database='railway'
)

app = Flask(__name__)


#Rota padrão para teste da api
@app.route('/')
def home():
    return '<h1> Hello World <h1>'





#Essa Rota tem como função cadastrar o usuario no app
# e passar as suas informações para o banco de dados
@app.route('/cadastro', methods=['POST'])
def cadastro():

    # Recebendo email, senha do usuário, tipo e nome
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
    # Retorna 'OK' para o frontend
    return jsonify({'cadastro': 'OK'})





#Essa Rota tem como função logar o usuario no app
# e passar as suas informações do banco de dados
# para o frontend
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
            sql_command = "SELECT tipo_usuario from usuarios WHERE email = %s"
            value = (email,)
            mycursor.execute(sql_command, value)
            tipo_user = mycursor.fetchone()

            return jsonify({'acesso': 'OK', 'Tipo_aluno': tipo_user, 'email': email})
        else:
            print("Senha incorreta")
    else:
        print("Email nao encontrado")

    return jsonify({'acesso': 'false', 'Tipo_aluno': 'Null'})





# Essa rota serve foi utilizada para fazer teste automatizado
# o teste feito se baseia em testar a busca de um login no 
# banco de daos
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

    # Se retornar um linha vazia significa que não encontrou nenhum email correspondente
    if email_res is not None:
        #Compara a senha enviada com a senha armazenada no banco
        senha_encontrada = email_res[1]
        if senha_encontrada == password:
            print("Logado com sucesso")
            return jsonify({'acesso': 'true'})
    else:
        return jsonify({'acesso': 'false'})





#Essa rota serve para criar um treinamento/curso nova no banco de dados
@app.route('/criar_treinamento', methods=['POST'])
def treinamento():

    #Leitura de todos os parâmetros passados do frontend
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
    curso_ini = request.form['curso_inicial']
    curso_av = request.form['curso_avancado']
    qnt_atual = 0

    #print(nome_comercial) #- print para debug

    # Execução dos comando no banco de dados
    # Vai inserir na tabela de treinamentos um novo treinamento 
    #  com os dados que forma passados
    mycursor = db.cursor()
    sql_command = "INSERT INTO treinamentos (Nome_Comercial, Codigo_curso, Descricao, Carga_horaria, Inicio_inscricoes, Final_inscricoes, Inicio_treinamentos, Final_treinamentos, qntd_min, qntd_max, qntd_atual, ci, ca) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (nome_comercial, codigo_curso, descricao, carga_horaria, inicio_inscricoes, final_inscricoes, inicio_treinamentos, final_treinamentos, qnt_min, qnt_max, qnt_atual, curso_ini, curso_av)
    mycursor.execute(sql_command, values)
    db.commit()
    
    #Json formatado com os parâmetros recebidos
    #Json opcional, utilizado para testar passagem
    # de parâmetros do backend para o frontend
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





# Essa rota serve para mostrar ao usuário todos os treinamentos/cursos
# Disponíveis. Faz a busca na tabela treinamentos do banco de dados
@app.route('/listar_treinamentos', methods=['POST'])
def Lista_treinamento():

    #Executa o comando de busca de trinamentos no banco
    # Seleciona todos os treinamentos para serem mostrados para o aluno no frontend
    mycursor = db.cursor()
    sql_command = "SELECT * FROM treinamentos"
    mycursor.execute(sql_command)
    treinamentos = mycursor.fetchall()
    
    # Analisamos quantas linhas são retornadas para criarmos
    #  um dicionário para retorno para o frontend
    tamanho = len(treinamentos)
    data = []

    # Faz uma lista de Jsons com os parâmetros recebidos do banco de dados
    # Retornando um dicionário para o front end
    for i in range(tamanho):
        treinamento = {
        'Nome Comercial': treinamentos[i][0],
        'Código do Curso': treinamentos[i][1],
        'Descricao': treinamentos[i][2],
        'Carga Horária': treinamentos[i][3],
        'Início das incricoes': treinamentos[i][4],
        'Final das inscricoes': treinamentos[i][5],
        'Início dos treinamentos': treinamentos[i][6],
        'Final dos treinamentos': treinamentos[i][7],
        'Quantidade mínima de alunos': treinamentos[i][8],
        'Quantidade máxima de alunos': treinamentos[i][9],
        'Quantidade atual de alunos': treinamentos[i][10]
        }

        data.append(treinamento)
        
    #Retorno da lista de treinamentos para o frontend
    return jsonify(data)





#Essa rota serve para vincular um usuário a um treinamento/curso
@app.route('/entrar_treinamento', methods=['POST'])
def entrar_treinamento():

    #Recebendo dos parâmetros passados do frontend
    email = request.form['email'] #pega o email do usuario
    codigo_treinamento = request.form['codigo_curso'] #pega o curso desejado

    # Busca na tabela treinamento de ainda há vagas disponíveis para que o aluno possa entrar
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

            # É feito um update na tabela de treinamento onde a quantidade atual de alunos
            #  inscritos é atualizada
            sql_command = "UPDATE treinamentos SET qntd_atual = qntd_atual + 1 WHERE Codigo_curso = %s" #incrementa em 1 a quantidade atual no curso desejado
            value = (codigo_treinamento,)
            mycursor.execute(sql_command, value)
            db.commit()

            # Na tabela de treinamento_alunos, é feita a inserção do aluno com o treinamento
            #  mostrando que a relação foi feita, e além disso, recebe o status como "Em andamento"
            status = "Em andamento"
            sql_command = "INSERT INTO treinamento_alunos (email, codigo_treinamento, status, nota_1, nota_2, nota_3) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (email, codigo_treinamento, status, 0, 0, 0)
            mycursor.execute(sql_command, values)
            db.commit()

            print("%s Registrado com sucesso no curso %s", email, codigo_treinamento) #Print de debug
            return jsonify({'registro_treinamento': True}) #retorna True para o flutter

    else:
        return jsonify({'registro_treinamento': False}) #se for nulo





#Essa rota serve para desvincular um aluno de um treinamento/curso
@app.route('/sair_treinamento', methods=['POST'])
def sair_treinamento():
    #Recebendo dos parâmetros passados do frontend
    email = request.form['email'] #pega o email do usuario
    codigo_treinamento = request.form['codigo_curso'] #pega o curso desejado

    #Execução dos comandos no banco de dados
    # Faz a deleção na tabela de treinamento_alunos com base no email e no codigo do curso
    mycursor = db.cursor()
    sql_command = "DELETE FROM treinamento_alunos WHERE email = %s AND codigo_treinamento = %s"
    value = (email, codigo_treinamento)
    mycursor.execute(sql_command, value)
    db.commit()
    
    #Execução dos comandos no banco de dados
    # Diminui um na contagem de quantidade da alunos no treinamento
    sql_command = "UPDATE treinamentos SET qntd_atual = qntd_atual -1 WHERE Codigo_curso = %s"
    value = (codigo_treinamento,)
    mycursor.execute(sql_command, value)
    db.commit()

    return jsonify({'status_delete' : 'Deletado com sucesso!'})





# Essa rota serve para mostrar aqueles alunos que estão inscritos 
@app.route('/Listar_inscritos_treinamento', methods=['POST'])
def Listar_inscritos_treinamento():

    # Recebe o parâmetro do código do curso 
    id_treinamento = request.form['codigo_curso']

    # Faz a busca na tabela de treinamento_alunos, de todos os alunos
    #  que estão vinculados a esse treinamento
    mycursor = db.cursor()
    
    sql_command = "SELECT nome FROM usuarios WHERE email in (SELECT email from treinamento_alunos WHERE codigo_treinamento = %s)"
    values = (id_treinamento,)
    mycursor.execute(sql_command, values)
    listar_inscritos_treinamento = mycursor.fetchall()

    # Faz o arranjo de todos os usuários vinculados naquele treinamento
    #  e rotar essa listas com os nomes 
    lista_arr = []
    tamanho = len(listar_inscritos_treinamento)

    for i in range(tamanho):
        # possivel troca de 'email' para 'nome'
        vaga = {
            'email': listar_inscritos_treinamento[i][0],
        }
        lista_arr.append(vaga)
        print(lista_arr)
    
    return jsonify(lista_arr)





#Essa Rota serve para que seja criado as questões 
# do formulário de aptidao de cada treinamento
@app.route('/criar_questao_aptidao', methods=['POST'])
def criar_questao_aptidao():
    
    #Recebendo dos parâmetros passados do frontend para fazer o teste de aptidao

    id_teste = request.form['id_treinamento_quiz']
    n_questao = request.form['questao']
    t_pergunta = request.form['pergunta']
    resposta_a = request.form['respostaDaAlternativaA']
    alternativa_a = request.form['alternativaA']
    resposta_b = request.form['respostaDaAlternativaB']
    alternativa_b = request.form['alternativaB']
    resposta_c = request.form['respostaDaAlternativaC']
    alternativa_c = request.form['alternativaC']

    #Execução dos comandos no banco de dados
    # Faz a inserção na tabela de questões_apidao mantendo o vinculo com o trenamento pelo id
    mycursor = db.cursor()  
    sql_command = "INSERT INTO questoes_aptidao (id_teste, numero_questao, questao, resposta_a, resposta_b, resposta_c, alternativa_a, alternativa_b, alternativa_c) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (id_teste, n_questao, t_pergunta, resposta_a, resposta_b, resposta_c, alternativa_a, alternativa_b, alternativa_c)
    mycursor.execute(sql_command, values)
    db.commit()
                
    #resposta = {id_teste, n_questao, t_pergunta, resposta_a, alternativa_a, resposta_b, alternativa_b, resposta_c, alternativa_c}
    return jsonify({'message': 'Lista de objetos recebida com sucesso!'})





#Essa Rota serve para que seja criado as questões 
# do formulário de prova 1 de cada treinamento
@app.route('/criar_questao_prova1', methods=['POST'])
def criar_questao_prova1():
    
    #Recebendo dos parâmetros passados do frontend
    id_teste = request.form['id_treinamento_quiz']
    n_questao = request.form['questao']
    t_pergunta = request.form['pergunta']
    resposta_a = request.form['respostaDaAlternativaA']
    alternativa_a = request.form['alternativaA']
    resposta_b = request.form['respostaDaAlternativaB']
    alternativa_b = request.form['alternativaB']
    resposta_c = request.form['respostaDaAlternativaC']
    alternativa_c = request.form['alternativaC']

    #Execução dos comandos no banco de dados
    # Faz a inserção na tabela de questões_prova1 mantendo o vinculo com o trenamento pelo id
    mycursor = db.cursor()  
    sql_command = "INSERT INTO questoes_prova1 (id_teste, numero_questao, questao, resposta_a, resposta_b, resposta_c, alternativa_a, alternativa_b, alternativa_c) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (id_teste, n_questao, t_pergunta, resposta_a, resposta_b, resposta_c, alternativa_a, alternativa_b, alternativa_c)
    mycursor.execute(sql_command, values)
    db.commit()
                
    #resposta = {id_teste, n_questao, t_pergunta, resposta_a, alternativa_a, resposta_b, alternativa_b, resposta_c, alternativa_c}
    return jsonify({'message': 'Lista de objetos recebida com sucesso!'})





#Essa Rota serve para que seja criado as questões 
# do formulário de prova 2 de cada treinamento
@app.route('/criar_questao_prova2', methods=['POST'])
def criar_questao_prova2():
    
    #Recebendo dos parâmetros passados do frontend
    id_teste = request.form['id_treinamento_quiz']
    n_questao = request.form['questao']
    t_pergunta = request.form['pergunta']
    resposta_a = request.form['respostaDaAlternativaA']
    alternativa_a = request.form['alternativaA']
    resposta_b = request.form['respostaDaAlternativaB']
    alternativa_b = request.form['alternativaB']
    resposta_c = request.form['respostaDaAlternativaC']
    alternativa_c = request.form['alternativaC']

    #Execução dos comandos no banco de dados
    mycursor = db.cursor()  
    sql_command = "INSERT INTO questoes_prova2 (id_teste, numero_questao, questao, resposta_a, resposta_b, resposta_c, alternativa_a, alternativa_b, alternativa_c) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (id_teste, n_questao, t_pergunta, resposta_a, resposta_b, resposta_c, alternativa_a, alternativa_b, alternativa_c)
    mycursor.execute(sql_command, values)
    db.commit()
                
    #resposta = {id_teste, n_questao, t_pergunta, resposta_a, alternativa_a, resposta_b, alternativa_b, resposta_c, alternativa_c}
    return jsonify({'message': 'Lista de objetos recebida com sucesso!'})





# Essa rota tem o objetivo de corrigir o teste de aptidao feito pelo usuário
@app.route('/Corrigir_teste_aptidao', methods=['POST'])
def Corrigir_Teste_aptidao():
    respostas_corretas = 0 #numero de respostas corretas
    id_teste = request.form['id'] # id do teste para ser analisado
    resp_list = request.form['lista_respostas'] #lista com as respostas do aluno
    email = request.form['email'] 

    # Realiaza a correção da lista que é passada pelo frontend
    resp_list = resp_list.replace("[", "")
    resp_list = resp_list.replace("]", "")
    resp_list = resp_list.replace('"', "")
    lista = resp_list.split(",")

    print(lista) # Print de debug

    mycursor = db.cursor()

    # Passa pelas questões da tabela de questoes_aptidao, contando os acertos do usuário
    for index, item in enumerate(lista):

        if index < (len(lista)):

            questao = 'Questão ' + str(index + 1)
            # Seleciona a alternativa para comparar como falor armazenado
            sql_command = "SELECT " + item + " FROM questoes_aptidao WHERE id_teste = %s and numero_questao = %s"
            value = (id_teste, questao)
            mycursor.execute(sql_command, value)
            res = mycursor.fetchone()
            print(res[0])
            if res[0] == "true":
                respostas_corretas += 1

    # Se o resultado for maior que 70% das questões o usuário está aprovado
    if respostas_corretas >= (len(lista)) * 0.7:
        print(respostas_corretas) # print de debug

        # Atualiza o a nota do usuário na tabela treinamento_alunos
        sql_command = "UPDATE treinamento_alunos SET status = %s, nota_1 = %s WHERE email = %s"
        value = ('Aprovado', respostas_corretas, email)
        mycursor.execute(sql_command, value)
        db.commit()

        return jsonify({'status': 'Aprovado'})
    
    else:
        print(respostas_corretas)
        # Atualiza o a nota do usuário na tabela treinamento_alunos
        sql_command = "UPDATE treinamento_alunos SET status = %s, nota_1 = %s WHERE email = %s" #, justificativa = %s
        value = ('Reprovado, acertos insuficientes', respostas_corretas, email) #, 'Acertos insuficientes'
        mycursor.execute(sql_command, value)
        db.commit()

        return jsonify({'status': 'Reprovado'})





# Essa rota tem o objetivo de corrigir a prova 1 feita pelo usuário
@app.route('/Corrigir_teste_prova1', methods=['POST'])
def Corrigir_Teste_prova1():
    respostas_corretas = 0 #numero de respostas corretas
    id_teste = request.form['id']
    resp_list = request.form['lista_respostas'] #lista com as respostas do aluno

    resp_list = resp_list.replace("[", "")
    resp_list = resp_list.replace("]", "")
    resp_list = resp_list.replace('"', "")

    lista = resp_list.split(",")

    print(lista)

    email = request.form['email'] 
    mycursor = db.cursor()

    for index, item in enumerate(lista):

        if index < (len(lista)):

            questao = 'Questão ' + str(index + 1)
        
            sql_command = "SELECT " + item + " FROM questoes_prova1 WHERE id_teste = %s and numero_questao = %s"
            value = (id_teste, questao)
            mycursor.execute(sql_command, value)
            res = mycursor.fetchone()
            print(res[0])
            if res[0] == "true":
                respostas_corretas += 1

    if respostas_corretas >= (len(lista)) * 0.7:
        print(respostas_corretas)
        sql_command = "UPDATE treinamento_alunos SET status = %s, nota_1 = %s WHERE email = %s"
        value = ('Aprovado', respostas_corretas, email)
        mycursor.execute(sql_command, value)
        db.commit()
        return jsonify({'status': 'Aprovado'})
    else:
        print(respostas_corretas)
        sql_command = "UPDATE treinamento_alunos SET status = %s, nota_1 = %s WHERE email = %s" #, justificativa = %s
        value = ('Reprovado, acertos insuficientes', respostas_corretas, email) #, 'Acertos insuficientes'
        mycursor.execute(sql_command, value)
        db.commit()
        return jsonify({'status': 'Reprovado'})





# Essa rota tem o objetivo de corrigir a prova 1 feita pelo usuário
@app.route('/Corrigir_teste_prova2', methods=['POST'])
def Corrigir_Teste_prova2():
    respostas_corretas = 0 #numero de respostas corretas
    id_teste = request.form['id']
    resp_list = request.form['lista_respostas'] #lista com as respostas do aluno

    resp_list = resp_list.replace("[", "")
    resp_list = resp_list.replace("]", "")
    resp_list = resp_list.replace('"', "")

    lista = resp_list.split(",")

    print(lista)

    email = request.form['email'] 
    mycursor = db.cursor()

    for index, item in enumerate(lista):

        if index < (len(lista)):

            questao = 'Questão ' + str(index + 1)
        
            sql_command = "SELECT " + item + " FROM questoes_prova2 WHERE id_teste = %s and numero_questao = %s"
            value = (id_teste, questao)
            mycursor.execute(sql_command, value)
            res = mycursor.fetchone()
            print(res[0])
            if res[0] == "true":
                respostas_corretas += 1

    if respostas_corretas >= (len(lista)) * 0.7:
        print(respostas_corretas)
        sql_command = "UPDATE treinamento_alunos SET status = %s, nota_1 = %s WHERE email = %s"
        value = ('Aprovado', respostas_corretas, email)
        mycursor.execute(sql_command, value)
        db.commit()
        return jsonify({'status': 'Aprovado'})
    else:
        print(respostas_corretas)
        sql_command = "UPDATE treinamento_alunos SET status = %s, nota_1 = %s WHERE email = %s" #, justificativa = %s
        value = ('Reprovado, acertos insuficientes', respostas_corretas, email) #, 'Acertos insuficientes'
        mycursor.execute(sql_command, value)
        db.commit()
        return jsonify({'status': 'Reprovado'})





#Essa rota serve para que seja criada um nova vaga de emprego
@app.route('/vaga_emprego', methods=['POST'])
def vaga_emprego():

    #Recebendo os parâmetros passados do frontend
    id_vaga = request.form['id_vaga']
    titulo_vaga = request.form['titulo_vaga']
    empresa_oferece = request.form['empresa_oferece']
    descricao_vaga = request.form['descricao_vaga']
    pre_requisitos = request.form['pre_requisitos']
    salario_minimo = int(request.form['salario_minimo'])
    salario_maximo = int(request.form['salario_maximo'])

    #Execução dos comandos no banco de dados
    # Faz a inserção na tabela de vaga_emprego de uma nova vaga disponibilizada 
    mycursor = db.cursor()
    sql_command = "INSERT into vaga_emprego (id_vaga, Titulo_vaga, Empresa_oferece, Descricao_vaga, Pre_requisito, Salario_minimo, Salario_maximo) VALUES (%s, %s, %s, %s, %s,  %s, %s)"
    values = (id_vaga, titulo_vaga, empresa_oferece, descricao_vaga, pre_requisitos, salario_minimo, salario_maximo)
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


# Essa rota serve para buscar todas vagas criadas busca 
#  as informações de todas as vagas armazenadas no banco
#  e passa as informações para o frontend
@app.route('/listar_vaga_emprego', methods=['POST'])
def listar_vagas():

    #Execução dos comandos no banco de dados
    # Seleciona todas as vagas disponiveis no vaga_emprego
    mycursor = db.cursor()
    sql_command = "SELECT * FROM vaga_emprego"
    mycursor.execute(sql_command)
    vagas_emprego = mycursor.fetchall()
    
    tamanho = len(vagas_emprego)
    listaVagas = []

    # Faz uma lista de Jasons com os parâmetros recebidos do banco de dados
    # Retornando um dicionário para o frontend
    for i in range(tamanho):
        vaga = {
        'id': vagas_emprego[i][0],
        'Titulo da vaga': vagas_emprego[i][1],
        'Empresa': vagas_emprego[i][2],
        'Descricao':vagas_emprego[i][3],
        'Pré Requisito': vagas_emprego[i][4],
        'Salário mínimo': vagas_emprego[i][5],
        'Salário máximo': vagas_emprego[i][6],
        }
        listaVagas.append(vaga)
        
    print(listaVagas)
    #Rertona ao frontend a lista de vagas do banco de dados
    return jsonify(listaVagas)


#Essa rota serve para vincular um usuário a uma vaga de emprego
@app.route('/entrar_vaga_emprego', methods=['POST'])
def entrar_vaga_emprego():
    #tabela que contém a relação entre a vaga e quem se inscreveu nela (por email)
    mycursor = db.cursor()
    id_vaga = request.form['id_vaga']
    email = request.form['email']
    sql_command = "SELECT email FROM usuario_vaga WHERE id_vaga = %s and email = %s"
    values = (id_vaga, email)
    
    mycursor.execute(sql_command, values)
    email_check = mycursor.fetchone()
    if email_check is not None:
        print("ja esta inscrito nessa vaga!")
        return jsonify({'status': False})
    # colocar que o mano vai entrar
    
    status = 'Em andamento'
    sql_command = "Insert into usuario_vaga (email, id_vaga, situacao) values (%s, %s, %s)"
    values = (email, id_vaga, status)
    mycursor.execute(sql_command, values)
    db.commit()
    return jsonify({'status': True})



@app.route('/sair_vaga_emprego', methods=['POST'])
def sair_vaga_emprego():

    id_vaga = request.form['id_vaga']
    email = request.form['email']
    
    mycursor = db.cursor()
    sql_command = "SELECT * FROM usuario_vaga WHERE id_vaga = %s and email = %s"
    values = (id_vaga, email)
    mycursor.execute(sql_command, values)
    email_check = mycursor.fetchone()

    if email_check is not None:

        sql_command = "DELETE FROM usuario_vaga WHERE id_vaga = %s AND email = %s"
        values = (id_vaga, email)
        mycursor.execute(sql_command, values)
        db.commit()
        return jsonify({'sair_emprego_status': 'True'})
    else:
        return jsonify({'sair_emprego_status': 'False'})


#Essa rota serve para buscar os usuários inscritos
# em uma determinada vaga
@app.route('/Listar_inscritos_vaga', methods=['POST'])
def Listar_inscritos_vaga():
    id_vaga = request.form['id']
    mycursor = db.cursor()
    sql_command = "SELECT email from usuario_vaga WHERE id_vaga = %s"
    values = (id_vaga,)
    mycursor.execute(sql_command, values)
    listar_inscritos_vaga = mycursor.fetchall()
    lista_arr = []
    tamanho = len(listar_inscritos_vaga)
    for i in range(tamanho):
        vaga = {
            'email': listar_inscritos_vaga[i][0],
        }
        lista_arr.append(vaga)
        print(lista_arr)
    return jsonify(lista_arr)


@app.route('/Historico_aluno', methods=['POST'])
def historico():
    email = request.form['email']
    mycursor = db.cursor()
    sql_command = "SELECT * from treinamento_alunos WHERE email = %s" ##treinamento_alunos = (email (varchar), codigo_curso (varchar), status (varchar), justificativa (varchar))
    values = (email,)
    mycursor.execute(sql_command, values)
    historico = mycursor.fetchall()
    historico_list = []
    tamanho = len(historico)
    for i in range(tamanho):
        historico_env = {
            'email': historico[i][0],
            'Codigo do curso': historico[i][1],
            'Status': historico[i][2],
            'Nota': historico[i][3]
        }
        historico_list.append(historico_env)
    return jsonify(historico_list)


# Essa rota serve para que possam ser feitas atualizações
# dos treinamentos criados
@app.route('/Update_treinamentos', methods=['POST'])
def Update_treinamentos():
    
    #Recebendo os parâmetros passados do frontend
    nome_comercial = request.form['nome_comercial']
    codigo_curso = request.form['codigo_curso']
    descricao = request.form['descricao']
    carga_horaria = request.form['carga_horaria']
    inicio_inscricoes = request.form['inicio_inscricoes']
    final_inscricoes = request.form['final_inscricoes']
    inicio_treinamentos = request.form['inicio_treinamentos']
    final_treinamentos = request.form['final_treinamentos']
    qnt_min = request.form['qnt_min'] ##ISSO DAQUI É UM INT %d
    qnt_max = request.form['qnt_max'] ##ISSO DAQUI É UM INT %d

    #Execução dos comandos no banco de dados
    mycursor = db.cursor()
    sql_command = "UPDATE treinamentos SET Nome_comercial = %s, Descricao = %s, Carga_horaria = %s, Inicio_inscricoes = %s, Final_inscricoes = %s, Inicio_treinamentos = %s, Final_treinamentos = %s, qntd_min = %s, qntd_max = %s where Codigo_curso = %s"
    values = (nome_comercial, descricao, carga_horaria, inicio_inscricoes, final_inscricoes, inicio_treinamentos, final_treinamentos, qnt_min, qnt_max, codigo_curso)
    mycursor.execute(sql_command, values)
    db.commit()

    return jsonify({'Update_treinamento': 'Update com sucesso'})


# Essa rota serve para que os trienamentos possam ser deletados
@app.route('/Delete_treinamentos', methods=['POST'])
def Delete_treinamentos():

    #Recebe o parâmetro passado do frontend
    codigo_curso = int(request.form['codigo_curso'])
    print(codigo_curso)

    #Execução dos comandos no banco de dados
    mycursor = db.cursor()
    sql_command = "DELETE FROM treinamentos WHERE Codigo_curso = %s"
    values = (codigo_curso,)
    mycursor.execute(sql_command, values)
    db.commit()
    return jsonify('Deletado com sucesso!')


@app.route('/Update_vaga', methods=['POST'])
def update_vaga():
    #Recebe o parâmetro passado do frontend
    id_vaga = int(request.form['id'])
    titulo_vaga = request.form['titulo_vaga']
    empresa_oferece = request.form['empresa_oferece']
    descricao_vaga = request.form['descricao_vaga']
    pre_requisitos = request.form['pre_requisitos']
    salario_minimo = int(request.form['salario_minimo'])
    salario_maximo = int(request.form['salario_maximo'])

    #Execução dos comandos no banco de dados
    mycursor = db.cursor()
    sql_command = "UPDATE vaga_emprego SET Titulo_vaga = %s, Empresa_oferece = %s, Descricao_vaga = %s, Pre_requisito = %s, Salario_minimo = %s, Salario_maximo = %s where id = %s"
    values = (titulo_vaga, empresa_oferece, descricao_vaga, pre_requisitos, salario_minimo, salario_maximo, id_vaga)
    mycursor.execute(sql_command, values)
    db.commit()
    
    return jsonify({'Update_vaga': 'Update com sucesso'})

# Essa rota serve para deletar um vaga de emprego
@app.route('/Delete_vagas', methods=['POST'])
def Delete_vagas():


    #Execução dos comandos no banco de dados
    codigo_vagas = request.form['codigo_vaga']

    mycursor = db.cursor()
    sql_command = "DELETE FROM vaga_emprego WHERE id_vaga = %s"
    values = (codigo_vagas,)
    mycursor.execute(sql_command, values)
    db.commit()

    mycursor = db.cursor()
    sql_command = "DELETE FROM treinamentos WHERE Codigo_curso = %s"
    values = (codigo_vagas,)
    mycursor.execute(sql_command, values)
    db.commit()

    
    sql_command = "DELETE FROM questoes WHERE id_teste = %s"
    values = (codigo_vagas,)
    mycursor.execute(sql_command, values)
    db.commit()


    return jsonify({'Delete_vaga': 'Delete com sucesso'})




@app.route('/Listar_teste', methods=['POST'])
def Listar_teste():

    id = request.form['id']

    #mycursor = db.cursor()  
    #sql_command = "SELECT Codigo_curso from treinamentos where Nome_Comercial = %s"
    #value = (Nome_comercial,)
    #mycursor.execute(sql_command, value)
    #id = mycursor.fetchone()
    #id = int(id)
    

    mycursor = db.cursor() 
    sql_command = "SELECT * FROM questoes_aptidao where id_teste = %s"
    value = (id,)
    mycursor.execute(sql_command, value)
    questoes = mycursor.fetchall()
    tamanho_questoes = len(questoes)

    formulario = []

    for i in range(tamanho_questoes):
        listar_teste = {
            'id_teste': questoes[i][0],
            'numero_questao': questoes[i][1],
            'questao': questoes[i][2],
            'resposta_a': questoes[i][3],
            'resposta_b': questoes[i][4],
            'resposta_c': questoes[i][5],
            'alternativa_a': questoes[i][6],
            'alternativa_b': questoes[i][7],
            'alternativa_c': questoes[i][8]
        }

        formulario.append(listar_teste)

    print(formulario)
    
    return jsonify(formulario)


@app.route('/Listar_teste_prova1', methods=['POST'])
def Listar_teste_prova1():

    id = request.form['id']

    #mycursor = db.cursor()  
    #sql_command = "SELECT Codigo_curso from treinamentos where Nome_Comercial = %s"
    #value = (Nome_comercial,)
    #mycursor.execute(sql_command, value)
    #id = mycursor.fetchone()
    #id = int(id)
    

    mycursor = db.cursor() 
    sql_command = "SELECT * FROM questoes_prova1 where id_teste = %s"
    value = (id,)
    mycursor.execute(sql_command, value)
    questoes = mycursor.fetchall()
    tamanho_questoes = len(questoes)

    formulario = []

    for i in range(tamanho_questoes):
        listar_teste = {
            'id_teste': questoes[i][0],
            'numero_questao': questoes[i][1],
            'questao': questoes[i][2],
            'resposta_a': questoes[i][3],
            'resposta_b': questoes[i][4],
            'resposta_c': questoes[i][5],
            'alternativa_a': questoes[i][6],
            'alternativa_b': questoes[i][7],
            'alternativa_c': questoes[i][8]
        }

        formulario.append(listar_teste)
    
    return jsonify(formulario)


@app.route('/Listar_teste_prova2', methods=['POST'])
def Listar_teste_prova2():

    id = request.form['id']

    #mycursor = db.cursor()  
    #sql_command = "SELECT Codigo_curso from treinamentos where Nome_Comercial = %s"
    #value = (Nome_comercial,)
    #mycursor.execute(sql_command, value)
    #id = mycursor.fetchone()
    #id = int(id)
    

    mycursor = db.cursor() 
    sql_command = "SELECT * FROM questoes_prova2 where id_teste = %s"
    value = (id,)
    mycursor.execute(sql_command, value)
    questoes = mycursor.fetchall()
    tamanho_questoes = len(questoes)

    formulario = []

    for i in range(tamanho_questoes):
        listar_teste = {
            'id_teste': questoes[i][0],
            'numero_questao': questoes[i][1],
            'questao': questoes[i][2],
            'resposta_a': questoes[i][3],
            'resposta_b': questoes[i][4],
            'resposta_c': questoes[i][5],
            'alternativa_a': questoes[i][6],
            'alternativa_b': questoes[i][7],
            'alternativa_c': questoes[i][8]
        }

        formulario.append(listar_teste)
    
    return jsonify(formulario)


@app.route('/Listar_vaga_aluno', methods=['POST'])
def Listar_vaga_alunos():
    mycursor = db.cursor() 
    email = request.form['email']

    status = 'Aprovado'
    sql_command = "SELECT * FROM vaga_emprego where id_vaga in (SELECT codigo_treinamento FROM treinamento_alunos where email = %s AND status = %s)"
    value = (email, status)
    mycursor.execute(sql_command, value)
    res_list = mycursor.fetchall()
    tamanho = len(res_list)
    lista_res = []

    for i in range(tamanho):
        listagem_vaga = {
            'id': res_list[i][0],
            'Titulo da vaga': res_list[i][1],
            'Empresa': res_list[i][2],
            'Descricao':res_list[i][3],
            'Pré Requisito': res_list[i][4],
            'Salário mínimo': res_list[i][5],
            'Salário máximo': res_list[i][6],
        }

        lista_res.append(listagem_vaga)
    print(lista_res)
    return jsonify(lista_res)

@app.route('/Listar_treinamentos_id', methods=['POST'])
def Listar_treinamentos_id():
    mycursor = db.cursor()
    sql_command = "SELECT Nome_Comercial, Codigo_curso FROM treinamentos"
    mycursor.execute(sql_command)
    res_list = mycursor.fetchall()

    lista_treinamento = []

    tamanho = len(res_list)
    for i in range(tamanho):
        treinamento_id = {
            'Nome Comercial': res_list[i][0],
            'Código do Curso': res_list[i][1],
        }
        lista_treinamento.append(treinamento_id)

    print(lista_treinamento)
    return jsonify(lista_treinamento)

@app.route('/Listar_usuarios_para_mentor', methods=['POST'])
def Listar_usuarios_para_mentor():
    mycursor = db.cursor()
    sql_command = "SELECT email FROM usuarios where tipo_usuario = 'Aluno'"
    mycursor.execute(sql_command)
    res_list = mycursor.fetchall()

    lista_usuarios = []

    tamanho = len(res_list)
    for i in range(tamanho):
        usuarios = {
            'email': res_list[i][0],
        }
        lista_usuarios.append(usuarios)

    print(lista_usuarios)
    return jsonify(lista_usuarios)


@app.route('/vaga_empresa_criar', methods=['POST'])
def vaga_empresa_criar():
    mycursor = db.cursor()
    id_empresa = request.form['id_empresa']
    email_empresa = request.form['email_empresa']
    sql_command = "INSERT into vaga_empresa (email, id_vaga) values (%s, %s)"
    values = (email_empresa, id_empresa)
    mycursor.execute(sql_command, values)
    db.commit()
    return jsonify({'status': 'OK'})



@app.route('/vaga_empresa_listar', methods=['POST'])
def vaga_empresa_listar():
    mycursor = db.cursor()
    email_empresa = request.form['email_empresa']
    sql_command = "SELECT * from treinamento_alunos WHERE codigo_treinamento in (Select id_vaga FROM vaga_empresa WHERE email = %s)"
    values = (email_empresa,)
    mycursor.execute(sql_command, values)
    lista_res = mycursor.fetchall()
    
    lista_enviar = []
    tamanho = len(lista_res)
    

    for i in range(tamanho):
        lista_vaga_empresa = {
            'email': lista_res[i][0],
            'Codigo do curso': lista_res[i][1],
            'Status': lista_res[i][2],
            'Nota': lista_res[i][3]
        }
        lista_enviar.append(lista_vaga_empresa)
    
    
    return jsonify(lista_enviar)

@app.route('/curso_introdutorio_treinamentos', methods=['POST'])
def Curso_introdutorio_treinamento():

    id = request.form['id']

    mycursor = db.cursor()
    sql_command = "SELECT ci FROM treinamentos where Codigo_curso = %s"
    values = (id,)
    mycursor.execute(sql_command, values)
    ci_treinamentos = mycursor.fetchone()
    
    lista_enviar = []
    tamanho = len(ci_treinamentos)
    

    for i in range(tamanho):
        ci_treinamento = {
            'ci': ci_treinamentos[i],
        }
        lista_enviar.append(ci_treinamento)
    
    
    return jsonify(lista_enviar)


@app.route('/curso_avancado_treinamentos', methods=['POST'])
def Curso_avancado_treinamento():

    id = request.form['id']

    mycursor = db.cursor()
    sql_command = "SELECT ca FROM treinamentos where Codigo_curso = %s"
    values = (id,)
    mycursor.execute(sql_command, values)
    ci_treinamentos = mycursor.fetchone()
    
    lista_enviar = []
    tamanho = len(ci_treinamentos)
    

    for i in range(tamanho):
        ci_treinamento = {
            'ca': ci_treinamentos[i],
        }
        lista_enviar.append(ci_treinamento)
    
    
    return jsonify(lista_enviar)

if __name__ == '__main__':
    app.run()

