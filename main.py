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
    """Função para inserir novos clientes"""
    cursor.execute('INSERT INTO clientes(nome, email, telefone, numero_identificacao) VALUES (?, ?, ?, ?)',
                   (nome, email, telefone, numero_identificacao))
    conn.commit()


def inserir_quarto(tipo, preco_noite, status):
    """Função para inserir novos quartos"""
    cursor.execute('INSERT INTO quartos(tipo, preco_noite, status) VALUES (?, ?, ?)',
                   (tipo, preco_noite, status))
    conn.commit()


def inserir_reserva(data_check_in, data_check_out, status):
    """Função para inserir novas reservas"""
    # Seleciona o último cliente inserido
    cursor.execute('SELECT id FROM clientes ORDER BY id DESC')
    cliente = cursor.fetchone()
    if not cliente:
        print("Erro: Nenhum cliente registrado. Por favor, insira os dados de um cliente primeiro.")
        return

    cliente_id = cliente[0]

    # Seleciona o último quarto inserido
    cursor.execute('SELECT id FROM quartos ORDER BY id DESC')
    quarto = cursor.fetchone()
    if not quarto:
        print("Erro: Nenhum quarto registrado. Por favor, insira os dados de um quarto primeiro.")
        return

    quarto_id = quarto[0]

    # Insere a nova reserva
    data_check_in_str = data_check_in.strftime('%Y-%m-%d')
    data_check_out_str = data_check_out.strftime('%Y-%m-%d')
    cursor.execute(
        'INSERT INTO reservas(cliente_id, quarto_id, data_check_in, data_check_out, status) VALUES (?, ?, ?, ?, ?)',
        (cliente_id, quarto_id, data_check_in_str, data_check_out_str, status)
    )
    conn.commit()

def inserir_pagamento(valor, data_pagamento, metodo):
    """Função para inserir novos pagamentos"""
    # Seleciona a última reserva inserida usando ORDENAR por id DESCENDENTE
    cursor.execute('SELECT id FROM reservas ORDER BY id DESC')
    reserva_id = cursor.fetchone()[0]

    data_pagamento_str = data_pagamento.strftime('%Y-%m-%d')

    cursor.execute('INSERT INTO pagamentos(reserva_id, valor, data_pagamento, metodo) VALUES (?, ?, ?, ?)',
                   (reserva_id, valor, data_pagamento_str, metodo))

    conn.commit()


def inserir_dados():
    print("\nInserir dados do cliente\n-------------------")

    nome = input("Insira o nome do cliente: ").capitalize()
    email = input("Insira o email: ")

    while True:
        telefone = input("Insira o telefone: ")
        if len(telefone) == 9:
            break
        else:
            print("\nInsira um número de telefone válido.")

    while True:
        numero_identificacao = input("Insira o NIF: ")
        if len(numero_identificacao) == 9:
            break
        else:
            print("\nInsira um NIF válido.")

    print("\nInserir dados do quarto\n-------------------")

    tipos = ["Individual", "Duplo", "Suite"]
    print("Os tipos de quarto são", tipos)

    while True:
        tipo_index = int(input("\nQual é o tipo de quarto desejado pelo cliente?\n[0] - Individual\n[1] - Duplo\n[2] - Suite\n"))
        if tipo_index in [0, 1, 2]:
            tipo = tipos[tipo_index]
            break
        else:
            print("\nTipo de quarto inserido inválido! Por favor, insira um tipo de quarto válido.")

    statuses = ["Disponível", "Ocupado", "Em Manutenção"]
    print("\nOs status de quarto são: ", statuses)

    while True:
        status_quarto = int(input("Insira o status do quarto:\n[0] - Disponivel\n[1] - Ocupado\n[2] - Em Manutenção\n"))
        if status_quarto in [0, 1, 2]:
            status_quarto = statuses[status_quarto]
            break
        else:
            print("\nMetodo inserido inválido! Por favor, insira um metodo válido.\n")

    print("\nInserir dados da reserva\n-------------------")
    format = "%d/%m/%Y"

    while True:
        try:
            data_check_in = input("Insira a data do check-in (dd/mm/yyyy): ")
            data_check_in_as_dt = datetime.datetime.strptime(data_check_in, format)
            data_check_out = input("Insira a data do check-out (dd/mm/yyyy): ")
            data_check_out_as_dt = datetime.datetime.strptime(data_check_out, format)
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
    print(f"O valor total a pagar por {noite} noites é de {preco_total}")

    while True:
        try:
            valor = float(input("Insira o valor do pagamento: "))
            break
        except ValueError:
            print("Valor inserido inválido! Por favor, insira um valor válido.")

    if valor < preco_total:
        status = "Pendente"
    else:
        status = "Confirmada"


    while True:
        try:
            data_pagamento = input("Insira a data do pagamento (dd/mm/yyyy): ")
            data_pagamento_as_dt = datetime.datetime.strptime(data_pagamento, format)
            break
        except ValueError:
            print("Formato de data inválido! Por favor, insira no formato dd/mm/yyyy.")

    metodos = ["Numerário", "Cartão de Crédito", "Transferência Bancária"]
    print("\nOs métodos de pagamento são", metodos)

    while True:
        metodo = int(input(
            "Qual metodo de pagamento deseja usar?\n[0] - Numerário\n[1] - Cartão de Crédito\n[2] - Transferência bancária\n"))
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
    print("\nLista de Clientes:\n--------------")
    cursor.execute('SELECT * FROM clientes')
    resultado = cursor.fetchall()
    for cliente in resultado:
        print(cliente)

    print("\nLista de Quartos:\n--------------")
    cursor.execute('SELECT * FROM quartos')
    resultado = cursor.fetchall()
    for quarto in resultado:
        print(quarto)

    print("\nLista de Reservas:\n--------------")
    cursor.execute('SELECT * FROM reservas')
    resultado = cursor.fetchall()
    for reserva in resultado:
        print(reserva)

    print("\nLista de Pagamentos:\n--------------")
    cursor.execute('SELECT * FROM pagamentos')
    resultado = cursor.fetchall()
    for pagamento in resultado:
        print(pagamento)


def apagar_dados():
    # print("\nApagar dados do cliente\n-------------------")
    # cliente_id = int(input("Insira o ID do cliente a ser apagado: "))
    # cursor.execute('DELETE FROM clientes WHERE id = (?)', (cliente_id,))
    # conn.commit()
    # print(f"Cliente com ID {cliente_id} apagado com sucesso!")

    cursor.execute('DROP TABLE clientes')
    cursor.execute('DROP TABLE quartos')
    cursor.execute('DROP TABLE reservas')
    cursor.execute('DROP TABLE pagamentos')
    criar_tabelas()
    conn.commit()

# Listar todas as reservas ativas (reservas confirmadas) e respetivos clientes e quartos
def listar_reservas_ativas():

    cursor.execute('''
            SELECT reservas.id, clientes.nome, quartos.tipo, reservas.data_check_in, reservas.data_check_out
            FROM reservas
            JOIN clientes ON reservas.cliente_id = clientes.id
            JOIN quartos ON reservas.quarto_id = quartos.id
            WHERE reservas.status = 'Confirmada'
        ''')
    resultado = cursor.fetchall()
    if resultado:
        print("\nListagem de todas as reservas ativas (reservas confirmadas):\n--------------------------")
        for reserva in resultado:
            print(
                f'Reserva ID: {reserva[0]}, Cliente: {reserva[1]}, Quarto: {reserva[2]}, Check-in: {reserva[3]}, Check-out: {reserva[4]}'
            )
    else:
        print("\nNão há reservas confirmadas.")

# Listar todos os quartos disponíveis.
def listar_quartos_disponiveis():

    cursor.execute('''
        SELECT * FROM quartos
        WHERE status = 'Disponível'
        ''')

    resultado = cursor.fetchall()
    if resultado:
        print("\nListagem de todos os quartos disponíveis:\n--------------------------")
        for quarto in resultado:
            print(quarto)
    else:
        print("\nNão há quartos disponíveis.")


# Consultar todas as reservas de um cliente específico
def consultar_reserva(reserva_id):
    cursor.execute('SELECT * FROM reservas WHERE id = (?)', (reserva_id,))
    reserva_cliente = cursor.fetchall()
    conn.commit()
    print(f'\nAs reservas do cliente {reserva_id} são:', reserva_cliente)


# Listar todos os pagamentos pendentes
def listar_pagamentos_pendentes():
    print("\nListagem de todos os pagamentos pendentes\n--------------------------")
    cursor.execute('''SELECT * FROM reservas
                    WHERE status = 'Pendente'
                    ''')

    pagamentos = cursor.fetchall()
    if not pagamentos:
        print("Não há pagamentos pendentes.")
    else:
        for pagamento in pagamentos:
            print(pagamento)

def main():
    # Faz a criação das tabelas na base de dados para evitar erros
    criar_tabelas()

    while True:
        try:
            inp = int(input(
                "\nO que quer fazer na base de dados? \n[1] - Inserir dados\n[2] - Apagar dados\n[3] - Enunciado\n[0] - Sair e listar dados\n "))
        except ValueError:
            print("Valor inserído inválido. Tente novamente.")
            continue

        if inp == 1:
            # Execução da função inserir dados
            inserir_dados()

        elif inp == 2:
            apagar_dados()

        elif inp == 0:
            listar_dados()
            inp = int(input(
                "\nDeseja sair?\n[1] - Sim\n[2] - Não\n"
            ))

            if inp == 1:
                print("Saindo...")
                break # Encerra o laço para sair do programa
            elif inp == 2:
                continue

        elif inp == 3:

            cursor.execute("SELECT COUNT(*) FROM clientes")

            if cursor.fetchone()[0] == 0:

                print("\nNenhum dado encontrado. Por favor, insira dados antes de continuar.\n")

                continue



            while True:
                try:
                    inp2 = int(input(
                    "\nQual exercício deseja consultar?\n[1] - Listar reservas ativas\n[2] - Listar quartos disponiveis\n[3] - Consultar reservas de um cliente especifico\n[4] - Listar pagamentos pendentes\n[0] - Voltar\n "))
                except ValueError:
                    print("Valor inserído inválido. Tente novamente.")
                    continue
                if inp2 == 1:
                    listar_reservas_ativas()
                elif inp2 == 2:
                    listar_quartos_disponiveis()
                elif inp2 == 3:
                    reserva_id = int(input("Insira o ID da reserva: "))
                    consultar_reserva(reserva_id)
                elif inp2 == 4:
                    listar_pagamentos_pendentes()
                elif inp2 == 0:
                    break
                else:
                    print("\nOpção inválida. Tente novamente.")

        else:
            print("\nOpção inválida. Tente novamente.")


# Chama o menu principal
main()

# Fecha a conexão com a base de daos
conn.close()
