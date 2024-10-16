import psycopg2
from tkinter import *
from tkinter import messagebox

# Conectar ao banco de dados PostgreSQL
conn = psycopg2.connect(
    dbname="Petshop",
    user="postgres",
    password="pabd",
    host="localhost"
)
cursor = conn.cursor()

# Função para registrar novo usuário
def registrar_usuario(login, senha):
    cursor.execute("INSERT INTO usuario (login, senha) VALUES (%s, %s)", (login, senha))
    conn.commit()

# Função para a tela de login
def tela_login():
    def tentar_login():
        login = entry_login.get()
        senha = entry_senha.get()

        if login and senha:
            cursor.execute("SELECT * FROM usuario WHERE login = %s", (login,))
            user = cursor.fetchone()
            if user:
                cursor.execute("SELECT * FROM usuario WHERE login = %s AND senha = %s", (login, senha))
                user = cursor.fetchone()
                if user:
                    janela_login.destroy()
                    tela_cadastro_dono()  
                else:
                    Label(janela_login, text="Senha incorreta!", fg="red").grid(row=4, column=0, columnspan=2, padx=10, pady=10)
            else:
                Label(janela_login, text="Login não cadastrado. Deseja registrar?", fg="red").grid(row=4, column=0, columnspan=2, padx=10, pady=10)
                Button(janela_login, text="Registrar", command=lambda: registrar_usuario(login, senha)).grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        else:
            Label(janela_login, text="Por favor, preencha todos os campos!", fg="red").grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    janela_login = Tk()
    janela_login.title("Login")

    Label(janela_login, text="Login").grid(row=0, column=0, padx=10, pady=10)
    entry_login = Entry(janela_login)
    entry_login.grid(row=0, column=1, padx=10, pady=10)

    Label(janela_login, text="Senha").grid(row=1, column=0, padx=10, pady=10)
    entry_senha = Entry(janela_login, show="*")
    entry_senha.grid(row=1, column=1, padx=10, pady=10)

    Button(janela_login, text="Entrar", command=tentar_login).grid(row=2, column=0, columnspan=2, padx=10, pady=10)


    janela_login.mainloop()
    
# Função para cadastrar Dono
def tela_cadastro_dono():
    janela_dono = Tk()
    janela_dono.title("Cadastro de Dono")
    
    def cadastrar_dono():
        frame_cadastro = Frame(janela_dono)
        frame_cadastro.grid(row=8, column=0, padx=10, pady=10)
        
        Label(frame_cadastro, text="Nome do dono").grid(row=0, column=0, padx=10, pady=10)
        entry_nome = Entry(frame_cadastro)
        entry_nome.grid(row=0, column=1, padx=10, pady=10)
        
        Label(frame_cadastro, text="CPF").grid(row=3, column=0, padx=10, pady=10)
        entry_cpf = Entry(frame_cadastro)
        entry_cpf.grid(row=3, column=1, padx=10, pady=10)

        Label(frame_cadastro, text="Endereço").grid(row=1, column=0, padx=10, pady=10)
        entry_endereco = Entry(frame_cadastro)
        entry_endereco.grid(row=1, column=1, padx=10, pady=10)

        Label(frame_cadastro, text="Telefone").grid(row=2, column=0, padx=10, pady=10)
        entry_telefone = Entry(frame_cadastro)
        entry_telefone.grid(row=2, column=1, padx=10, pady=10)

        def cadastrar():
            nome = entry_nome.get()
            endereco = entry_endereco.get()
            telefone = entry_telefone.get()
            cpf = entry_cpf.get()

            try:
                cursor.execute("INSERT INTO dono (nome, endereco, telefone, cpf) VALUES (%s, %s, %s, %s)", (nome, endereco, telefone, cpf))
                conn.commit()
                Label(frame_cadastro, text="Dono cadastrado com sucesso!", fg="green").grid(row=5, column=0, columnspan=2, padx=10, pady=10)
            except psycopg2.Error as e:
                Label(frame_cadastro, text=f"Erro ao cadastrar dono: {e}", fg="red").grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        Button(frame_cadastro, text="Cadastrar", command=cadastrar).grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        
    def atualizar_dono():
        frame_atualizar = Frame(janela_dono)
        frame_atualizar.grid(row=8, column=0, padx=10, pady=10)

        Label(frame_atualizar, text="CPF do dono").grid(row=0, column=0, padx=10, pady=10)
        entry_cpf = Entry(frame_atualizar)
        entry_cpf.grid(row=0, column=1, padx=10, pady=10)

        def confirmar_cpf():
            cpf = entry_cpf.get()
            cursor.execute("SELECT * FROM dono WHERE cpf = %s", (cpf,))
            resultado = cursor.fetchone()
            if resultado:
                frame_atualizar.destroy()
                atualizar_dados(cpf)
            else:
                Label(frame_atualizar, text="CPF não encontrado!", fg="red").grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        Button(frame_atualizar, text="Confirmar", command=confirmar_cpf).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        def atualizar_dados(cpf):
            frame_atualizar = Frame(janela_dono)
            frame_atualizar.grid(row=8, column=0, padx=10, pady=10)

            Label(frame_atualizar, text="Nome do dono").grid(row=0, column=0, padx=10, pady=10)
            entry_nome = Entry(frame_atualizar)
            entry_nome.grid(row=0, column=1, padx=10, pady=10)

            Label(frame_atualizar, text="Endereço").grid(row=1, column=0, padx=10, pady=10)
            entry_endereco = Entry(frame_atualizar)
            entry_endereco.grid(row=1, column=1, padx=10, pady=10)

            Label(frame_atualizar, text="Telefone").grid(row=2, column=0, padx=10, pady=10)
            entry_telefone = Entry(frame_atualizar)
            entry_telefone.grid(row=2, column=1, padx=10, pady=10)

            def atualizar():
                nome = entry_nome.get()
                endereco = entry_endereco.get()
                telefone = entry_telefone.get()

                cursor.execute("UPDATE dono SET nome = %s, endereco = %s, telefone = %s WHERE cpf = %s", (nome, endereco, telefone, cpf))
                conn.commit()
                Label(frame_atualizar, text="Dono atualizado com sucesso!", fg="green").grid(row=3, column=0, columnspan=2, padx=10, pady=10)

            Button(frame_atualizar, text="Atualizar", command=atualizar).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def ler_dono():
        frame_ler = Frame(janela_dono)
        frame_ler.grid(row=8, column=0, padx=10, pady=10)

        Label(frame_ler, text="CPF do dono").grid(row=0, column=0, padx=10, pady=10)
        entry_cpf = Entry(frame_ler)
        entry_cpf.grid(row=0, column=1, padx=10, pady=10)

        def ler():
            cpf = entry_cpf.get()
            cursor.execute("SELECT * FROM dono WHERE cpf = %s", (cpf,))
            resultado = cursor.fetchone()
            if resultado:
                Label(frame_ler, text=f"CPF: {resultado[0]}").grid(row=1, column=0, columnspan=2, padx=10, pady=2)
                Label(frame_ler, text=f"Nome: {resultado[1]}").grid(row=2, column=0, columnspan=2, padx=10, pady=2)
                Label(frame_ler, text=f"Endereço: {resultado[2]}").grid(row=3, column=0, columnspan=2, padx=10, pady=2)
                Label(frame_ler, text=f"Telefone: {resultado[3]}").grid(row=4, column=0, columnspan=2, padx=10, pady=2)
            else:
                Label(frame_ler, text="Dono não encontrado!").grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        Button(frame_ler, text="Ler", command=ler).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def deletar_dono():
        frame_deletar = Frame(janela_dono)
        frame_deletar.grid(row=8, column=0, padx=10, pady=10)

        Label(frame_deletar, text="CPF do dono").grid(row=0, column=0, padx=10, pady=10)
        entry_cpf = Entry(frame_deletar)
        entry_cpf.grid(row=0, column=1, padx=10, pady=10)

        def deletar():
            cpf = entry_cpf.get()
            cursor.execute("DELETE FROM pets WHERE cpf_dono = %s", (cpf,))
            conn.commit()
            cursor.execute("DELETE FROM dono WHERE cpf = %s", (cpf,))
            conn.commit()
            Label(frame_deletar, text="Dono deletado com sucesso!").grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        Button(frame_deletar, text="Deletar", command=deletar).grid(row=2, column=0, columnspan=2, padx=10, pady=10)
            
    def executar_opcao():
        opcao = entry_opcao.get()
        if opcao == "1":
            cadastrar_dono()
        elif opcao == "2":
            ler_dono()
        elif opcao == "3":
            atualizar_dono()
        elif opcao == "4":
            deletar_dono()
        elif opcao == "5":
            janela_dono.destroy()
            tela_cadastro_pet()
        elif opcao == "6":
            janela_dono.destroy()
            tela_login()
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

    Label(janela_dono, text="CRUD do dono:").grid(row=0, column=0, padx=10, pady=10)
    entry_opcao = Entry(janela_dono)
    entry_opcao.grid(row=10, column=0, padx=10, pady=10)

    Button(janela_dono, text="Executar", command=executar_opcao).grid(row=11, column=0, columnspan=2, padx=10, pady=10)
    
    Label(janela_dono, text="1. Cadastrar dono").grid(row=2, column=0, padx=10, pady=10)
    Label(janela_dono, text="2.Ler dados do dono").grid(row=3, column=0, padx=10, pady=10)
    Label(janela_dono, text="3. Atualizar dados do dono ").grid(row=4, column=0, padx=10, pady=10)
    Label(janela_dono, text="4. Deletar Dono").grid(row=5, column=0, padx=10, pady=10)
    Label(janela_dono, text="5. Entrar no CRUD do Pet").grid(row=6, column=0, padx=10, pady=10)
    Label(janela_dono, text="6. Voltar para a tela de login").grid(row=7, column=0, padx=10, pady=10)
    
    Label(janela_dono, text="Escolha uma opção:").grid(row=9, column=0, padx=10, pady=10)

    janela_dono.mainloop()
    

# Função para cadastrar Pet
def tela_cadastro_pet():
    janela_pet = Tk()
    janela_pet.title("Cadastro do Pet")
    def cadastrar_pet():
        frame_cadastro = Frame(janela_pet)
        frame_cadastro.grid(row=8, column=0, padx=10, pady=10)
        Label(frame_cadastro, text="Nome do pet").grid(row=0, column=0, padx=10, pady=10)
        entry_nome = Entry(frame_cadastro)
        entry_nome.grid(row=0, column=1, padx=10, pady=10)

        Label(frame_cadastro, text="Raça").grid(row=1, column=0, padx=10, pady=10)
        entry_raca = Entry(frame_cadastro)
        entry_raca.grid(row=1, column=1, padx=10, pady=10)

        Label(frame_cadastro, text="Idade").grid(row=2, column=0, padx=10, pady=10)
        entry_idade = Entry(frame_cadastro)
        entry_idade.grid(row=2, column=1, padx=10, pady=10)

        Label(frame_cadastro, text="CPF do dono").grid(row=3, column=0, padx=10, pady=10)
        entry_cpf_dono = Entry(frame_cadastro)
        entry_cpf_dono.grid(row=3, column=1, padx=10, pady=10)

        def cadastrar():
            nome = entry_nome.get()
            raca = entry_raca.get()
            idade = entry_idade.get()
            cpf_dono = entry_cpf_dono.get()

            cursor.execute("INSERT INTO pets (nome, raca, idade, cpf_dono) VALUES (%s, %s, %s, %s)", (nome, raca, idade, cpf_dono))
            conn.commit()
            cursor.execute("SELECT id FROM pets ORDER BY id DESC LIMIT 1")
            id_pet = cursor.fetchone()[0]
            Label(frame_cadastro, text=f"Pet cadastrado com sucesso! O seu ID é: {id_pet}").grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        Button(frame_cadastro, text="Cadastrar", command=cadastrar).grid(row=5, column=0, columnspan=2, padx=10, pady=10)


    def atualizar_pet():
        frame_atualizar = Frame(janela_pet)
        frame_atualizar.grid(row=8, column=0, padx=10, pady=10)

        Label(frame_atualizar, text="Nome do pet").grid(row=1, column=0, padx=10, pady=10)
        entry_nome = Entry(frame_atualizar)
        entry_nome.grid(row=1, column=1, padx=10, pady=10)

        Label(frame_atualizar, text="Raça").grid(row=2, column=0, padx=10, pady=10)
        entry_raca = Entry(frame_atualizar)
        entry_raca.grid(row=2, column=1, padx=10, pady=10)

        Label(frame_atualizar, text="Idade").grid(row=3, column=0, padx=10, pady=10)
        entry_idade = Entry(frame_atualizar)
        entry_idade.grid(row=3, column=1, padx=10, pady=10)

        def atualizar():
            nome = entry_nome.get()
            raca = entry_raca.get()
            idade = entry_idade.get()

            cursor.execute("UPDATE pets SET nome = %s, raca = %s, idade = %s WHERE id = %s", (nome, raca, idade, id))
            conn.commit()
            Label(frame_atualizar, text="Pet atualizado com sucesso!").grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        Button(frame_atualizar, text="Atualizar", command=atualizar).grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def ler_pet():
        frame_ler = Frame(janela_pet)
        frame_ler.grid(row=8, column=0, padx=10, pady=10)

        Label(frame_ler, text="ID do pet").grid(row=0, column=0, padx=10, pady=10)
        entry_id_pet = Entry(frame_ler)
        entry_id_pet.grid(row=0, column=1, padx=10, pady=10)

        def ler():
            id_pet = entry_id_pet.get()
            cursor.execute("SELECT * FROM pets WHERE id = %s", (id_pet,))
            resultado = cursor.fetchone()
            if resultado:
                cursor.execute("SELECT * FROM dono WHERE cpf = %s", (resultado[4],))
                dono = cursor.fetchone()
                Label(frame_ler, text=f"Nome do pet: {resultado[1]}").grid(row=1, column=0, columnspan=2, padx=10, pady=10)
                Label(frame_ler, text=f"Raça: {resultado[2]}").grid(row=2, column=0, columnspan=2, padx=10, pady=10)
                Label(frame_ler, text=f"Idade: {resultado[3]}").grid(row=3, column=0, columnspan=2, padx=10, pady=10)
                Label(frame_ler, text=f"CPF do dono: {resultado[4]}").grid(row=4, column=0, columnspan=2, padx=10, pady=10)
                Label(frame_ler, text=f"Nome do dono: {dono[1]}").grid(row=5, column=0, columnspan=2, padx=10, pady=10)
                Label(frame_ler, text=f"Endereço do dono: {dono[2]}").grid(row=6, column=0, columnspan=2, padx=10, pady=10)
                Label(frame_ler, text=f"Telefone do dono: {dono[3]}").grid(row=7, column=0, columnspan=2, padx=10, pady=10)
            else:
                Label(frame_ler, text="Pet não encontrado!").grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        Button(frame_ler, text="Ler", command=ler).grid(row=8, column=0, columnspan=2, padx=10, pady= 10)

    def deletar_pet():
        frame_deletar = Frame(janela_pet)
        frame_deletar.grid(row=8, column=0, padx=10, pady=10)

        Label(frame_deletar, text="ID do pet").grid(row=0, column=0, padx=10, pady=10)
        entry_id_pet = Entry(frame_deletar)
        entry_id_pet.grid(row=0, column=1, padx=10, pady=10)

        def deletar():
            id_pet = entry_id_pet.get()
            cursor.execute("DELETE FROM consulta WHERE id_pet = %s", (id_pet,))
            conn.commit()
            cursor.execute("DELETE FROM pets WHERE id = %s", (id_pet,))
            conn.commit()
            Label(frame_deletar, text="Pet deletado com sucesso!").grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        Button(frame_deletar, text="Deletar", command=deletar).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def executar_opcao():
        opcao = entry_opcao.get()
        if opcao == "1":
            cadastrar_pet()
        elif opcao == "2":
            ler_pet()
        elif opcao == "3":
            atualizar_pet()
        elif opcao == "4":
            deletar_pet()
        elif opcao == "5":
            janela_pet.destroy()
            tela_cadastro_consulta()
        elif opcao == "6":
            janela_pet.destroy()
            tela_cadastro_dono()
        elif opcao == "7":
            janela_pet.destroy()
            tela_login()
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

    Label(janela_pet, text="CRUD do pet:").grid(row=0, column=0, padx=10, pady=10)
    entry_opcao = Entry(janela_pet)
    entry_opcao.grid(row=10, column=0, padx=10, pady=10)

    Button(janela_pet, text="Executar", command=executar_opcao).grid(row=11, column=0, columnspan=2, padx=10, pady=10)
    
    Label(janela_pet, text="1. Cadastrar pet").grid(row=2, column=0, padx=10, pady=10)
    Label(janela_pet, text="2. Ler dados do pet ").grid(row=3, column=0, padx=10, pady=10)
    Label(janela_pet, text="3. Atualizar dados do pet").grid(row=4, column=0, padx=10, pady=10)
    Label(janela_pet, text="4. Deletar pet").grid(row=5, column=0, padx=10, pady=10)
    Label(janela_pet, text="5. Entrar no CRUD das consultas").grid(row=6, column=0, padx=10, pady=10)
    Label(janela_pet, text="6. Voltar para o CRUD do dono").grid(row=7, column=0, padx=10, pady=10)
    Label(janela_pet, text="7. Voltar para a tela de login").grid(row=8, column=0, padx=10, pady=10)
    
    Label(janela_pet, text="Escolha uma opção:").grid(row=9, column=0, padx=10, pady=10)

    janela_pet.mainloop()

# Função para cadastrar as consultas 
def tela_cadastro_consulta():
    janela_consulta = Tk()
    janela_consulta.title("Cadastro de Consulta")
    
    def cadastrar_consulta():
        frame_cadastro = Frame(janela_consulta)
        frame_cadastro.grid(row=8, column=0, padx=10, pady=10)
        
        Label(frame_cadastro, text="Data da Consulta").grid(row=0, column=0, padx=10, pady=10)
        entry_data = Entry(frame_cadastro)
        entry_data.grid(row=0, column=1, padx=10, pady=10)
        
        Label(frame_cadastro, text="Hora da Consulta").grid(row=1, column=0, padx=10, pady=10)
        entry_hora = Entry(frame_cadastro)
        entry_hora.grid(row=1, column=1, padx=10, pady=10)
        
        Label(frame_cadastro, text="Principal Sintoma ").grid(row=2, column=0, padx=10, pady=10)
        entry_principal_sintoma = Entry(frame_cadastro)
        entry_principal_sintoma.grid(row=2, column=1, padx=10, pady=10)
        
        Label(frame_cadastro, text="ID do Pet").grid(row=3, column=0, padx=10, pady=10)
        entry_id_pet = Entry(frame_cadastro)
        entry_id_pet.grid(row=3, column=1, padx=10, pady=10)

        def cadastrar():
            try:
                id_pet = entry_id_pet.get()
                data = entry_data.get()
                hora = entry_hora.get()
                principal_sintoma = entry_principal_sintoma.get()
                
                cursor.execute("INSERT INTO consulta (data, hora, principal_sintoma, id_pet) VALUES (%s, %s, %s, %s)", (data, hora, principal_sintoma, id_pet))
                conn.commit()
                cursor.execute("SELECT MAX(ficha_consulta) FROM consulta")
                ficha_consulta = cursor.fetchone()[0]
                Label(frame_cadastro, text=f"Consulta cadastrada com sucesso! A ficha da consulta é: {ficha_consulta}").grid(row=5, column=0, columnspan=2, padx=10, pady=10)
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Erro ao cadastrar consulta: {e}")

        Button(frame_cadastro, text="Cadastrar", command=cadastrar).grid(row=5, column=0, columnspan=2, padx=10, pady=10)
    
    def atualizar_consulta():
        frame_atualizar = Frame(janela_consulta)
        frame_atualizar.grid(row=8, column=0, padx=10, pady=10)

        Label(frame_atualizar, text="Ficha da Consulta").grid(row=0, column=0, padx=10, pady=10)
        entry_ficha_consulta = Entry(frame_atualizar)
        entry_ficha_consulta.grid(row=0, column=1, padx=10, pady=10)

        def confirmar_ficha_consulta():
            ficha_consulta = entry_ficha_consulta.get()
            cursor.execute("SELECT * FROM consulta WHERE ficha_consulta = %s", (ficha_consulta,))
            resultado = cursor.fetchone()
            if resultado:
                frame_atualizar.destroy()
                atualizar_dados(ficha_consulta)
            else:
                Label(frame_atualizar, text="Consulta não encontrada!", fg="red").grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        Button(frame_atualizar, text="Confirmar", command=confirmar_ficha_consulta).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def atualizar_dados(ficha_consulta):
        frame_atualizar = Frame(janela_consulta)
        frame_atualizar.grid(row=8, column=0, padx=10, pady=10)

        Label(frame_atualizar, text="Data da Consulta").grid(row=0, column=0, padx=10, pady=10)
        entry_data = Entry(frame_atualizar)
        entry_data.grid(row=0, column=1, padx=10, pady=10)

        Label(frame_atualizar, text="Hora da Consulta").grid(row=1, column=0, padx=10, pady=10)
        entry_hora = Entry(frame_atualizar)
        entry_hora.grid(row=1, column=1, padx=10, pady=10)

        Label(frame_atualizar, text="Principal Sintoma ").grid(row=2, column=0, padx=10, pady=10)
        entry_principal_sintoma = Entry(frame_atualizar)
        entry_principal_sintoma.grid(row=2, column=1, padx=10, pady=10)

        def atualizar():
            data = entry_data.get()
            hora = entry_hora.get()
            principal_sintoma = entry_principal_sintoma.get()

            cursor.execute("UPDATE consulta SET data = %s, hora = %s, principal_sintoma = %s WHERE ficha_consulta = %s", (data, hora, principal_sintoma, ficha_consulta))
            conn.commit()
            Label(frame_atualizar, text="Consulta atualizada com sucesso!", fg="green").grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        Button(frame_atualizar, text="Atualizar", command=atualizar).grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        
    def ler_consulta():
        frame_ler = Frame(janela_consulta)
        frame_ler.grid(row=8, column=0, padx=10, pady=10)

        Label(frame_ler, text="Ficha da Consulta").grid(row=0, column=0, padx=10, pady=10)
        entry_ficha_da_consulta = Entry(frame_ler)
        entry_ficha_da_consulta.grid(row=0, column=1, padx=10, pady=10)

        def ler():
            ficha_da_consulta = entry_ficha_da_consulta.get()

            cursor.execute('''
                SELECT 
                    c.ficha_consulta, 
                    c.data, 
                    c.hora, 
                    c.principal_sintoma, 
                    p.nome, 
                    p.raca, 
                    p.idade, 
                    d.nome AS nome_dono, 
                    d.cpf AS cpf_dono, 
                    d.endereco AS endereco_dono, 
                    d.telefone AS telefone_dono
                FROM 
                    consulta c
                JOIN 
                    pets p ON c.id_pet = p.id
                JOIN 
                    dono d ON p.cpf_dono = d.cpf
                WHERE 
                    c.ficha_consulta = %s
            ''', (ficha_da_consulta,))

            resultado_consulta = cursor.fetchone()

            if resultado_consulta:
                Label(frame_ler, text=f"Ficha da Consulta: {resultado_consulta[0]}").grid(row=1, column=0, columnspan=2, padx=10, pady=1)
                Label(frame_ler, text=f"Data da Consulta: {resultado_consulta[1]}").grid(row=2, column=0, columnspan=2, padx=10, pady=1)
                Label(frame_ler, text=f"Hora da Consulta: {resultado_consulta[2]}").grid(row=3, column=0, columnspan=2, padx=10, pady=1)
                Label(frame_ler, text=f"Sintoma Principal: {resultado_consulta[3]}").grid(row=4, column=0, columnspan=2, padx=10, pady=1)
                Label(frame_ler, text=f"Nome do Pet: {resultado_consulta[4]}").grid(row=5, column=0, columnspan=2, padx=10, pady=1)
                Label(frame_ler, text=f"Raça do Pet: {resultado_consulta[5]}").grid(row=6, column=0, columnspan=2, padx=10, pady=1)
                Label(frame_ler, text=f"Idade do Pet: {resultado_consulta[6]}").grid(row=7, column=0, columnspan=2, padx=10, pady=1)
                Label(frame_ler, text=f"Nome do Dono: {resultado_consulta[7]}").grid(row=8, column=0, columnspan=2, padx=10, pady=1)
                Label(frame_ler, text=f"CPF do Dono: {resultado_consulta[8]}").grid(row=9, column=0, columnspan=2, padx=10, pady=1)
                Label(frame_ler, text=f"Endereço do Dono: {resultado_consulta[9]}").grid(row=10, column=0, columnspan=2, padx=10, pady=1)
                Label(frame_ler, text=f"Telefone do Dono: {resultado_consulta[10]}").grid(row=11, column=0, columnspan=2, padx=10, pady=1)
            else:
                Label(frame_ler, text="Consulta não encontrada!").grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        Button(frame_ler, text="Ler", command=ler).grid(row=12, column=0, columnspan=2, padx=10, pady=10)

    def deletar_consulta():
        frame_deletar = Frame(janela_consulta)
        frame_deletar.grid(row=8, column=0, padx=10, pady=10)

        Label(frame_deletar, text="Ficha da consulta").grid(row=0, column=0, padx=10, pady=10)
        entry_ficha_consulta = Entry(frame_deletar)
        entry_ficha_consulta.grid(row=0, column=1, padx=10, pady=10)

        def deletar():
            ficha_consulta = entry_ficha_consulta.get()
            cursor.execute("DELETE FROM consulta WHERE ficha_consulta = %s", (ficha_consulta,))
            conn.commit()
            Label(frame_deletar, text="Consulta deletada com sucesso!").grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        Button(frame_deletar, text="Deletar", command=deletar).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        Button(frame_deletar, text="Deletar", command=deletar).grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    def executar_opcao():
        opcao = entry_opcao.get()
        if opcao == "1":
            cadastrar_consulta()
        elif opcao == "2":
            ler_consulta()
        elif opcao == "3":
            atualizar_consulta()
        elif opcao == "4":
            deletar_consulta()
        elif opcao == "5":
            janela_consulta.destroy()
            tela_cadastro_pet()
        elif opcao == "6":
            janela_consulta.destroy()
            tela_cadastro_dono()
        elif opcao == "7":
            janela_consulta.destroy()
            tela_login()
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

    Label(janela_consulta, text="CRUD da Consulta:").grid(row=0, column=0, padx=10, pady=10)
    entry_opcao = Entry(janela_consulta)
    entry_opcao.grid(row=10, column=0, padx=10, pady=10)

    Button(janela_consulta, text="Executar", command=executar_opcao).grid(row=11, column=0, columnspan=2, padx=10, pady=10)
    
    Label(janela_consulta, text="1. Cadastrar consulta").grid(row=2, column=0, padx=10, pady=10)
    Label(janela_consulta, text="2. Ler dados da consulta ").grid(row=3, column=0, padx=10, pady=10)
    Label(janela_consulta, text="3. Atualizar dados da consulta ").grid(row=4, column=0, padx=10, pady=10)
    Label(janela_consulta, text="4. Deletar consulta").grid(row=5, column=0, padx=10, pady=10)
    Label(janela_consulta, text="5. Entrar no CRUD do Pet").grid(row=6, column=0, padx=10, pady=10)
    Label(janela_consulta, text="6. Entrar no CRUD do Dono").grid(row=7, column=0, padx=10, pady=10)
    Label(janela_consulta, text="7. Voltar para a tela de login").grid(row=8, column=0, padx=10, pady=10)
    
    Label(janela_consulta, text="Escolha uma opção:").grid(row=9, column=0, padx=10, pady=10)

    janela_consulta.mainloop()
        
# Iniciar o sistema
tela_login()