import sqlite3
import datetime

# Iniciar conexão com a base de dados 'hotel.db'
conn = sqlite3.connect("hotel.db")
cursor = conn.cursor()

# Criação das tabelas: Cliente, Quartos, Reservas e Pagamentos
def criar_tabelas():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    telefone TEXT NOT NULL,
    numero_identificacao TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quartos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    preco_noite TEXT NOT NULL,
    status TEXT NOT NULL
        )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reservas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    quarto_id INTEGER NOT NULL,
    data_check_in DATE NOT NULL,
    data_check_out DATE NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (quarto_id) REFERENCES quartos(id)
        )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pagamentos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reserva_id INTEGER NOT NULL,
    valor REAL NOT NULL,
    data_pagamento DATE NOT NULL,
    metodo TEXT NOT NULL,
    FOREIGN KEY (reserva_id) REFERENCES reservas(id)
        )
    ''')

conn.commit()

def inserir_cliente(nome, email, telefone, numero_identificacao):
    """Função para inserir novos clientes."""
    cursor.execute('INSERT INTO clientes(nome, email, telefone, numero_identificacao) VALUES (?, ?, ?, ?)',
                   (nome, email, telefone, numero_identificacao))
    conn.commit()

def inserir_quarto(tipo, preco_noite, status):
    """Função para inserir novos quartos."""
    cursor.execute('INSERT INTO quartos(tipo, preco_noite, status) VALUES (?, ?, ?)',
                   (tipo, preco_noite, status))
    conn.commit()

def inserir_reserva(data_check_in, data_check_out, status):
    """Função para inserir novas reservas."""
    # Seleciona o último cliente inserido
    cursor.execute('SELECT id FROM clientes ORDER BY id DESC')
    cliente_id = cursor.fetchone()[0]

    # Seleciona o último quarto inserido
    cursor.execute('SELECT id FROM quartos ORDER BY id DESC')
    quarto_id = cursor.fetchone()[0]

    # Converte data_check_in e data_check_out para string no formato ISO 8601
    data_check_in_str = data_check_in.strftime('%Y-%m-%d')
    data_check_out_str = data_check_out.strftime('%Y-%m-%d')

    # Insere a nova reserva com o cliente e quarto selecionados
    cursor.execute(
        'INSERT INTO reservas(cliente_id, quarto_id, data_check_in, data_check_out, status) VALUES (?, ?, ?, ?, ?)',
        (cliente_id, quarto_id, data_check_in_str, data_check_out_str, status))
    conn.commit()

def inserir_pagamento(valor, data_pagamento, metodo):
    """Função para inserir novos pagamentos."""
    # Seleciona a última reserva inserida usando ORDENAR por id DESCENDENTE
    cursor.execute('SELECT id FROM reservas ORDER BY id DESC')
    reserva_id = cursor.fetchone()[0]

    data_pagamento_str = data_pagamento.strftime('%Y-%m-%d')

    cursor.execute('INSERT INTO pagamentos(reserva_id, valor, data_pagamento, metodo) VALUES (?, ?, ?, ?)',
                   (reserva_id, valor, data_pagamento_str, metodo))

    conn.commit()

def inserir_dados():
    """Função que insere os dados."""
    print("\nInserir dados do cliente\n-------------------")

    nome = input("Insira o nome do cliente: ").capitalize()
    while True:
        email = input("Insira o email: ")
        if email.count("@") != 1 or "." not in email:
            print("Insira um email válido. (Com  @ e .)")
        else:
            break

    while True:
        telefone = input("Insira o número de telefone: ")
        if len(telefone) == 9:
            break
        else:
            print("\nInsira um número de telefone válido. (9 dígitos)")

    while True:
        numero_identificacao = input("Insira o NIF: ")
        if len(numero_identificacao) == 9:
            break
        else:
            print("\nInsira um NIF válido. (9 dígitos)")

    print("\nInserir dados do quarto\n-------------------")

    tipos = ["Individual", "Duplo", "Suite"]
    print("Os tipos de quarto são: ", tipos)

    while True:
        tipo_index = int(input(
            "Qual é o tipo de quarto desejado pelo cliente?\n[0] - Individual\n[1] - Duplo\n[2] - Suite\nInsira um valor: "))
        if tipo_index in [0, 1, 2]:
            tipo = tipos[tipo_index]
            break
        else:
            print("\nTipo de quarto inserido inválido! Por favor, insira um tipo de quarto válido.")

    estado = ["Disponível", "Ocupado", "Em Manutenção"]
    print("\nOs status de quarto são: ", estado)

    while True:
        status_quarto = int(input(
            "Insira o status do quarto:\n[0] - Disponivel\n[1] - Ocupado\n[2] - Em Manutenção\nInsira um valor: "))
        if status_quarto in [0, 1, 2]:
            status_quarto = estado[status_quarto]
            break
        else:
            print("\nMetodo inserido inválido! Por favor, insira um metodo válido.\n")

    print("\nInserir dados da reserva\n-------------------")

    # 'formato' é usado para especificar o formato em que as datas devem ser inseridas dia/mês/ano.
    formato = "%d/%m/%Y"
    while True:
        try:
            data_check_in = input("Insira a data do check-in (dd/mm/yyyy): ")
            data_check_in_as_dt = datetime.datetime.strptime(data_check_in, formato)
            data_check_out = input("Insira a data do check-out (dd/mm/yyyy): ")
            data_check_out_as_dt = datetime.datetime.strptime(data_check_out, formato)
            break
        except ValueError:
            print("Formato de data inválido! Por favor, insira no formato dd/mm/yyyy.")

    print("\nInserir dados do pagamento\n-------------------")

    preco_noite = 0
    noite = (data_check_out_as_dt - data_check_in_as_dt).days

    if tipo == "Individual":
        preco_noite = 87
    elif tipo == "Duplo":
        preco_noite = 120
    elif tipo == "Suite":
        preco_noite = 175

    preco_total = preco_noite * noite

    # Print usado para ajudar com o cálcula do preço total da estadia.
    print(f"O valor total a pagar por {noite} noites é de {preco_total}€.")

    while True:
        try:
            valor = float(input("Insira o valor do pagamento: "))
            break
        except ValueError:
            print("Valor inserido inválido! Por favor, insira um valor válido.")

    # Se o valor pago for inferior ao preço total da estadia, a reserva fica pendente, caso contrário, fica confirmada.
    if valor < preco_total:
        status = "Pendente"
    else:
        status = "Confirmada"

    while True:
        try:
            data_pagamento = input("Insira a data do pagamento (dd/mm/yyyy): ")
            data_pagamento_as_dt = datetime.datetime.strptime(data_pagamento, formato)
            break
        except ValueError:
            print("Formato de data inválido! Por favor, insira no formato dd/mm/yyyy.")

    metodos = ["Numerário", "Cartão de Crédito", "Transferência Bancária"]
    print("\nOs métodos de pagamento são", metodos)

    while True:
        metodo = int(input(
            "Qual metodo de pagamento deseja usar?\n[0] - Numerário\n[1] - Cartão de Crédito\n[2] - Transferência bancária\nInsira um valor: "))
        if metodo in [0, 1, 2]:
            metodo = metodos[metodo]
            break
        else:
            print("\nMetodo inserido inválido! Por favor, insira um metodo válido.\n")

    inserir_cliente(nome, email, telefone, numero_identificacao)
    inserir_quarto(tipo, preco_noite, status_quarto)
    inserir_reserva(data_check_in_as_dt, data_check_out_as_dt, status)
    inserir_pagamento(valor, data_pagamento_as_dt, metodo)
    conn.commit()

def listar_dados():
    """Função que lista os dados."""
    print("\nLista de Clientes:\n--------------")
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    for cliente in clientes:
        print(cliente)

    print("\nLista de Quartos:\n--------------")
    cursor.execute('SELECT * FROM quartos')
    quartos = cursor.fetchall()
    for quarto in quartos:
        print(quarto)

    print("\nLista de Reservas:\n--------------")
    cursor.execute('SELECT * FROM reservas')
    reservas = cursor.fetchall()
    for reserva in reservas:
        print(reserva)

    print("\nLista de Pagamentos:\n--------------")
    cursor.execute('SELECT * FROM pagamentos')
    pagamentos = cursor.fetchall()
    for pagamento in pagamentos:
        print(pagamento)

def apagar_dados():
    """Função que apaga todas as tabelas e as cria de novo."""
    # Apaga-se todas as tabelas
    cursor.execute('DROP TABLE clientes')
    cursor.execute('DROP TABLE quartos')
    cursor.execute('DROP TABLE reservas')
    cursor.execute('DROP TABLE pagamentos')
    criar_tabelas()  # Cria-se novas tabelas
    conn.commit()

def main():
    # Chama a função 'criar_tabelas' caso não existam.
    criar_tabelas()
    while True:
        inp = int(input(
            "\nO que quer fazer na base de dados? \n[1] - Inserir dados\n[2] - Apagar dados\n[3] - Enunciado\n[0] - Sair e listar dados\n "))

        if inp == 1:
            # Execução da função inserir dados.
            inserir_dados()

        elif inp == 2:
            # Execução da função apagar dados.
            apagar_dados()

        elif inp == 0:
            listar_dados()
            break  # Encerra o laço para sair do programa.
        elif inp == 3:
            # Criamos um loop para o enunciado até que o usuário decida sair
            while True:
                inp2 = input(
                    "Qual exercício deseja consultar?\n[0] Listar reservas ativas\n[1] Listar quartos disponiveis\n[2] Consultar reservas de um cliente especifico\n[3] Listar pagamentos pendentes\n[4] Voltar ao menu principal\n")
                if inp2 == '0':
                    listar_reservas_ativas()
                elif inp2 == '1':
                    listar_quartos_disponiveis()
                elif inp2 == '2':
                    reserva_id = int(input("Insira o ID da reserva: "))
                    consultar_reserva(reserva_id)
                elif inp2 == '3':
                    listar_pagamentos_pendentes()
                elif inp2 == '4':
                    break  # Se escolher 4, sai do loop do enunciado e volta ao menu principal
                else:
                    print("\nOpção inválida! Tente novamente.\n")

# Listar todas as reservas ativas (reservas confirmadas) e respetivos clientes e quartos.
def listar_reservas_ativas():
    cursor.execute('''
        SELECT reservas.id, clientes.nome, quartos.tipo, reservas.data_check_in, reservas.data_check_out
        FROM reservas
        JOIN clientes ON reservas.cliente_id = clientes.id
        JOIN quartos ON reservas.quarto_id = quartos.id
        WHERE reservas.status = 'Confirmada'
    ''')

    print(
        "\n\nListagem de todas as reservas ativas (reservas confirmadas) e respetivos clientes e quartos:\n--------------------------")

    reservas = cursor.fetchall()
    for reserva in reservas:
        print(
            f'Reserva ID: {reserva[0]}, Cliente: {reserva[1]}, Quarto: {reserva[2]}, Check-in: {reserva[3]}, Check-out: {reserva[4]}')

# Listar todos os quartos disponíveis.
def listar_quartos_disponiveis():
    print("\nListagem de todos os quartos disponíveis:\n--------------------------")
    cursor.execute('''
        SELECT * FROM quartos
        WHERE status = 'Disponível'
        ''')

    quartos = cursor.fetchall()
    for quarto in quartos:
        print(quarto)

# Consultar todas as reservas de um cliente específico.
def consultar_reserva(reserva_id):
    cursor.execute('SELECT * FROM reservas WHERE id = (?)', (reserva_id,))
    reserva_cliente = cursor.fetchall()
    conn.commit()
    print(f'\nAs reservas do cliente {reserva_id} são:', reserva_cliente)

# Listar todos os pagamentos pendentes.
def listar_pagamentos_pendentes():
    print("\nListagem de todos os pagamentos pendentes\n--------------------------")
    cursor.execute('''SELECT * FROM reservas
                    WHERE status = 'Pendente'
                    ''')

    pagamentos = cursor.fetchall()
    for pagamento in pagamentos:
        print(pagamento)


# Chama o menu principal e corre o programa. - Sem isto não acontece nada!!
main()

conn.close()