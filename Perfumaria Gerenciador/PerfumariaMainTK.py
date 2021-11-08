import sqlite3
from tkinter import *
from tkinter import ttk
import pyautogui as py
from tkinter import tix






Janela_main = tix.Tk()


class Funcionalidades():
    def limpa_tela(self):
        self.codigo_entry.delete(0,END)
        self.produto_entry.delete(0,END)
        self.saldo_entry.delete(0,END)
        self.sldmin_entry.delete(0,END)
        self.preco_entry.delete(0,END)
        self.custo_entry.delete(0,END)
        
    
    def conecta_bd(self):
        self.conn=sqlite3.connect("Perfumaria.db")
        self.cursor = self.conn.cursor()


    def desconecta_bd(self):
        self.conn.close()
    

    def montaTabelas(self):
        self.conecta_bd(); print("Conectado ao banco de dados")
        ### Criar tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Produtos (
                Codigo INTEGER PRIMARY KEY NOT NULL,
                Nomeprd VARCHAR (50) NOT NULL,
                Saldo INTEGER,
                Sldmin INTEGER,
                Preco INTEGER,
                Custo INTEGER

                );""")
        self.conn.commit(); print("Banco de dados criado")
        self.desconecta_bd
    

    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.produto = self.produto_entry.get()
        self.saldo = self.saldo_entry.get()
        self.sldmin = self.sldmin_entry.get()
        self.preco = self.preco_entry.get()
        self.custo = self.custo_entry.get()

        try:
            self.saldo = int(self.saldo)
        except:
            self.saldo=0

        try:
            self.sldmin = int(self.sldmin)
        except:
            self.sldmin=0

        try:
            self.preco = float(self.preco)
        except:
            self.preco=0

        try:
            self.custo =float(self.custo)
        except:
            self.custo=0      
                

    def add_produto(self):
        self.variaveis()

        self.conecta_bd()
        if self.produto =="":
            py.alert("Produto não determinado, não foi possível cadastrar")
        elif self.saldo <= -1:
            py.alert("Não é possível cadastrar Saldo de Produto Menor que zero")
        elif self.sldmin <= -1:
            py.alert("Não é possível cadastrar Saldo Mínimo de Produto Menor que zero")
        else:    
            self.cursor.execute("""
            INSERT INTO  Produtos (Nomeprd, Saldo, Sldmin, Preco, Custo)
            VALUES (?,?,?,?,?)""", (self.produto, self.saldo, self.sldmin, self.preco, self.custo))
            self.conn.commit()
            self.desconecta_bd()
            self.select_lista()
            self.limpa_tela()


    def select_lista(self):
        self.listaPro.delete(*self.listaPro.get_children())
        self.conecta_bd()
        lista = self.cursor.execute("""
        SELECT Codigo, Nomeprd, Saldo, Sldmin, preco, Custo FROM Produtos
        ORDER BY Nomeprd ASC; """)
        for i in lista:
            self.listaPro.insert ("",END, values=i)
        self.desconecta_bd()


    def OnDoubleClick(self, event):
        self.limpa_tela()
        self.listaPro.selection()

        for n in self.listaPro.selection():
            col1, col2, col3, col4, col5, col6 = self.listaPro.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.produto_entry.insert(END, col2)
            self.saldo_entry.insert(END, col3)
            self.sldmin_entry.insert(END, col4)
            self.preco_entry.insert(END, col5)
            self.custo_entry.insert(END, col6)

    
    def deleta_produto(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""
        DELETE FROM Produtos WHERE Codigo =? """, (self.codigo,))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()


    def altera_produto(self):
        self.variaveis()
        self.conecta_bd()
        if self.produto =="":
            py.alert("Produto não determinado, não foi possível cadastrar")
        elif self.saldo <= -1:
            py.alert("Não é possível cadastrar Saldo de Produto Menor que zero")
        elif self.sldmin <= -1:
            py.alert("Não é possível cadastrar Saldo Mínimo de Produto Menor que zero")
        else:
            self.cursor.execute("""
            UPDATE Produtos SET Nomeprd = ?, Saldo = ?, Sldmin = ?, Preco = ?, Custo = ?
            WHERE Codigo = ?""", (self.produto, self.saldo, self.sldmin, self.preco,self.custo, self.codigo,))
            self.conn.commit()
            self.desconecta_bd()
            self.limpa_tela()
            self.select_lista()


    def busca_produto(self):

        self.conecta_bd()
        self.listaPro.delete(*self.listaPro.get_children())

        self.produto_entry.insert(END, '%')
        produto= self.produto_entry.get()
        codigo = self.codigo_entry.get()
                
        if codigo =="":

            self.cursor.execute("""
            SELECT Codigo, Nomeprd, Saldo, Sldmin, Preco, Custo FROM Produtos
            WHERE Nomeprd LIKE '%s' ORDER BY Nomeprd ASC """ %produto)
            buscaPro = self.cursor.fetchall()
            for i in buscaPro:
                self.listaPro.insert("", END, values=i)
        else:
        
            self.cursor.execute("""
            SELECT Codigo, Nomeprd, Saldo, Sldmin, Preco, Custo FROM Produtos
            WHERE Codigo LIKE '%s' """ %codigo)
            buscaPro = self.cursor.fetchall()
            for i in buscaPro:
                self.listaPro.insert("", END, values=i)

        self.limpa_tela()
        self.desconecta_bd()

    
    def ver_opcoes(self):
    
        py.alert(text="""     Opções Do Softwere

                01) Listar nome e preço de venda dos produtos em ordem alfabética pelo nome.

                02) Listar código, nome, saldo em estoque e saldo mínimo de um produto identificado pelo seu código.

                03) Listar código, nome, saldo em estoque e saldo mínimo de todos os produtos cujo saldo em estoque esteja menor que o mínimo

                04) Listar código, nome, saldo em estoque e saldo mínimo dos produtos cujo saldo em estoque seja menor que o mínimo, e que tenha preço de venda maior que zero.

                05) Listar código, nome, saldo em estoque e saldo mínimo dos produtos com saldo em estoque menor que o mínimo e preço de custo maior que zero.

                06) Listar código, nome, saldo em estoque e saldo mínimo dos produtos com saldo em estoque menor que o mínimo e preço de venda maior que zero, em ordem alfabética por nome.

                07) Listar código e nome de todos os produtos que estão com preço de venda menor ou igual a zero.

                08) Informar quantos produtos estão cadastrados.

                09) Informar quantos produtos estão com saldo em estoque zerado

                10) Informar quantos produtos estão com saldo em estoque menor que o mínimo

                11) Informar o nome do produto, saldo em estoque, preço de venda e a previsão de rentabilidade com a venda de cada produto.

                12) Acesso a funcionários

                13) Manutenção de dados (Inclusão, Alteração, Exclusão, Consulta)    

                14) Validar Administrador """)



    def opcao_1(self):
        self.conecta_bd()
        self.cursor.execute("""SELECT NomePrd, Preco FROM Produtos ORDER BY NomePrd""")
        buscaPrd = self.cursor.fetchall()
        
        for i in buscaPrd:
            self.listaPrd.insert("", END, values=i)
        self.limpa_tela()
        self.desconecta_bd()
        

    def opcao_2(self):
        self.conecta_bd()
        continuar = "OK"
        while continuar == "OK":
            self.codigo =str(py.prompt("Digite o Código que deseja consultar"))
            
            self.cursor.execute("""
            SELECT Codigo, Nomeprd, Saldo, SldMin FROM Produtos WHERE Codigo = ? """, (self.codigo,))
            buscaProd = self.cursor.fetchall()
            
            for i in buscaProd:
                self.listaProd.insert("", END, values=i)
            continuar = py.confirm("Deseja Realizar outra consulta?", buttons = ["OK", "Cancelar"] )

        self.limpa_tela()
        self.desconecta_bd()


    def opcao_3(self):
        self.conecta_bd()     
        self.cursor.execute("""SELECT Codigo, NomePrd, Saldo, SldMin FROM Produtos WHERE Saldo < SldMin""")
        buscaProd = self.cursor.fetchall()        
        for i in buscaProd:
            self.listaProd.insert("", END, values=i)        
        self.limpa_tela()
        self.desconecta_bd()

    
    def opcao_4(self):
        self.conecta_bd()     
        self.cursor.execute("""SELECT Codigo, NomePrd, Saldo, SldMin FROM Produtos WHERE Saldo < SldMin AND Preco > 0""")
        buscaProd = self.cursor.fetchall()        
        for i in buscaProd:
            self.listaProd.insert("", END, values=i)        
        self.limpa_tela()
        self.desconecta_bd()

    
    def opcao_5(self):
        self.conecta_bd()     
        self.cursor.execute("""SELECT Codigo, NomePrd, Saldo, SldMin FROM Produtos WHERE Saldo < SldMin AND Custo > 0""")
        buscaProd = self.cursor.fetchall()        
        for i in buscaProd:
            self.listaProd.insert("", END, values=i)        
        self.limpa_tela()
        self.desconecta_bd()
    
    
    def opcao_6(self):
        self.conecta_bd()     
        self.cursor.execute("""SELECT Codigo, NomePrd, Saldo, SldMin FROM Produtos WHERE Saldo < SldMin AND Preco > 0 ORDER BY NomePrd""")
        buscaProd = self.cursor.fetchall()        
        for i in buscaProd:
            self.listaProd.insert("", END, values=i)        
        self.limpa_tela()
        self.desconecta_bd()
    

    def opcao_7(self):
        self.conecta_bd()     
        self.cursor.execute("""SELECT Codigo, NomePrd FROM Produtos WHERE Preco <= 0""")
        buscaProd = self.cursor.fetchall()        
        for i in buscaProd:
            self.listaProd.insert("", END, values=i)        
        self.limpa_tela()
        self.desconecta_bd()
    

    def opcao_8(self):
        self.conecta_bd()     
        self.cursor.execute("""SELECT count(*) FROM Produtos""")
        buscaProd = self.cursor.fetchall()        
        for i in buscaProd:
            self.listaCtg.insert("", END, values=i)    
        py.alert("Total de Produtos Cadastrados")    
        self.limpa_tela()
        self.desconecta_bd()

    def opcao_9(self):
        self.conecta_bd()     
        self.cursor.execute("""SELECT count(*) FROM Produtos WHERE Saldo = 0""")
        buscaProd = self.cursor.fetchall()        
        for i in buscaProd:
            self.listaCtg.insert("", END, values=i)    
        py.alert("Total de Produtos com saldo em estoque zerado")    
        self.limpa_tela()
        self.desconecta_bd()


    def opcao_10(self):
        self.conecta_bd()     
        self.cursor.execute("""SELECT count(*) FROM Produtos WHERE Saldo > SldMin""")
        buscaProd = self.cursor.fetchall()        
        for i in buscaProd:
            self.listaCtg.insert("", END, values=i)    
        py.alert("Total de Produtos com saldo em estoque menor que o mínimo")    
        self.limpa_tela()
        self.desconecta_bd()


    def opcao_11(self):
        self.conecta_bd()     
        self.cursor.execute("""SELECT Codigo, NomePrd, Saldo, Preco, Saldo*Preco AS Rentabilidade FROM Produtos""")
        buscaProd = self.cursor.fetchall()        
        for i in buscaProd:
            self.listaCtg.insert("", END, values=i)    
        py.alert("Rentabilidade Dos Produtos Em Estoque / Código do Produto no campo Quantidade")    
        self.limpa_tela()
        self.desconecta_bd()
    
            
        

class Aplicativo(Funcionalidades):
    def __init__(self):
        self.Janela_main = Janela_main
        self.tela()
        self.frames_da_tela()
        self.widgets_frame_1()
        self.lista_frame_2()
        self.montaTabelas()
        self.select_lista()
        self.menus()
        Janela_main.mainloop()
        

    def tela(self):
        self.Janela_main.title("Perfumaria DB")
        self.Janela_main.geometry("800x700")
        self.Janela_main.resizable(True, True)
        self.Janela_main.configure(background= "blue")


    def frames_da_tela(self):
        self.frame_1 = Frame(self.Janela_main, bd= 4, bg= "gray")
        self.frame_1.place(relx=0.02 , rely=0.02, relwidth=0.96, relheight=0.45)

        self.frame_2 = Frame(self.Janela_main, bd= 4, bg= "white")
        self.frame_2.place(relx=0.02 , rely=0.5, relwidth=0.96, relheight=0.48)

        
    def widgets_frame_1(self):
        ### abas
        self.abas = ttk.Notebook(self.frame_1)
        self.aba1 = Frame(self.abas)
        self.aba2 = Frame(self.abas)

        self.aba1.configure (background="gray")
        self.aba2.configure (background="lightgray")

        self.abas.add(self.aba1, text = "Manutenção de Dados")
        self.abas.add(self.aba2, text = "Buscas Rápidas")

        self.abas.place(relx=0, rely=0,relwidth=0.98, relheight=0.98 )

        
        
        ### limpar
        self.bt_limpar = Button(self.aba1, text= "Limpar", command= self.limpa_tela)
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)

        ### buscar
        self.bt_buscar = Button(self.aba1, text= "Buscar", command= self.busca_produto)
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)

        texto_balao_buscar = "Buscar somente pelo Código OU Nome do Produto"
        self.balao_buscar = tix.Balloon(self.aba1)
        self.balao_buscar.bind_widget(self.bt_buscar, balloonmsg= texto_balao_buscar )

        ### Novo
        self.bt_novo = Button(self.aba1, text= "Novo", command=self.add_produto)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)

        ### Alterar
        self.bt_alterar = Button(self.aba1, text= "Alterar", command=self.altera_produto)
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)

        ### Apagar
        self.bt_apagar = Button(self.aba1, text= "Apagar", command=self.deleta_produto)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

        
        ## Label e entrada do codigo
        self.lb_codigo = Label(self.aba1, text="Código")
        self.lb_codigo.place(relx=0.03, rely=0.05)

        self.codigo_entry = Entry(self.aba1)
        self.codigo_entry.place(relx=0.01, rely= 0.15, relwidth=0.15, relheight=0.07)
        
        ## Label e entrada do Produto

        self.lb_produto = Label(self.aba1, text="Produto")
        self.lb_produto.place(relx=0.03, rely=0.25)

        self.produto_entry = Entry(self.aba1)
        self.produto_entry.place(relx=0.01, rely= 0.35, relwidth=0.30, relheight=0.1)

        ## Label e entrada do Saldo
        self.lb_saldo = Label(self.aba1, text="Saldo")
        self.lb_saldo.place(relx=0.03, rely=0.50)

        self.saldo_entry = Entry(self.aba1)
        self.saldo_entry.place(relx=0.01, rely= 0.60, relwidth=0.15, relheight=0.07)


        ## Label e entrada do Saldo minimo
        self.lb_sldmin = Label(self.aba1, text="Saldo Mínimo")
        self.lb_sldmin.place(relx=0.03, rely=0.75)

        self.sldmin_entry = Entry(self.aba1)
        self.sldmin_entry.place(relx=0.01, rely= 0.85, relwidth=0.15, relheight=0.07)


        ## Label e entrada do preco de venda
        self.lb_preco = Label(self.aba1, text="Preco")
        self.lb_preco.place(relx=0.38, rely=0.25)

        self.preco_entry = Entry(self.aba1)
        self.preco_entry.place(relx=0.36, rely= 0.35, relwidth=0.15, relheight=0.07)

        ## Label e entrada do custo
        self.lb_custo = Label(self.aba1, text="Custo")
        self.lb_custo.place(relx=0.55, rely=0.25)

        self.custo_entry = Entry(self.aba1)
        self.custo_entry.place(relx=0.53, rely= 0.35, relwidth=0.15, relheight=0.07)

        ### aba2

        self.bt_opcoes = Button(self.aba2, text= "Ver opções", command=self.ver_opcoes)
        self.bt_opcoes.place(relx=0.1, rely=0.15, relwidth=0.1, relheight=0.15)

        self.bt_opcao1 = Button(self.aba2, text= "opção 1", command= self.janela_op_a)
        self.bt_opcao1.place(relx=0.2, rely=0.3, relwidth=0.1, relheight=0.15)

        self.bt_opcao2 = Button(self.aba2, text= "opção 2", command=self.jaop2)
        self.bt_opcao2.place(relx=0.3, rely=0.3, relwidth=0.1, relheight=0.15)

        self.bt_opcao3 = Button(self.aba2, text= "opção 3", command= self.jaop3)
        self.bt_opcao3.place(relx=0.4, rely=0.3, relwidth=0.1, relheight=0.15)

        self.bt_opcao4 = Button(self.aba2, text= "opção 4", command=self.jaop4)
        self.bt_opcao4.place(relx=0.5, rely=0.3, relwidth=0.1, relheight=0.15)

        self.bt_opcao5 = Button(self.aba2, text= "opção 5",command= self.jaop5)
        self.bt_opcao5.place(relx=0.6, rely=0.3, relwidth=0.1, relheight=0.15)

        self.bt_opcao6 = Button(self.aba2, text= "opção 6", command=self.jaop6)
        self.bt_opcao6.place(relx=0.1, rely=0.5, relwidth=0.1, relheight=0.15)

        self.bt_opcao7 = Button(self.aba2, text= "opção 7", command= self.jaop7)
        self.bt_opcao7.place(relx=0.2, rely=0.5, relwidth=0.1, relheight=0.15)

        self.bt_opcao8 = Button(self.aba2, text= "opção 8", command= self.jaop8)
        self.bt_opcao8.place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.15)

        self.bt_opcao9 = Button(self.aba2, text= "opção 9",command=self.jaop9)
        self.bt_opcao9.place(relx=0.4, rely=0.5, relwidth=0.1, relheight=0.15)

        self.bt_opcao10 = Button(self.aba2, text= "opção 10",command= self.jaop10)
        self.bt_opcao10.place(relx=0.5, rely=0.5, relwidth=0.1, relheight=0.15)

        self.bt_opcao11 = Button(self.aba2, text= "opção 11", command= self.jaop11)
        self.bt_opcao11.place(relx=0.6, rely=0.5, relwidth=0.1, relheight=0.15)

        self.lb_opcao = Label(self.aba2, text="Funções")
        self.lb_opcao.place(relx=0.1, rely=0.3, relwidth=0.1, relheight=0.15)

        
    def jaop2(self):
        self.janela_op_b_f()
        self.opcao_2()  
    def jaop3(self):
        self.janela_op_b_f()
        self.opcao_3()  
    def jaop4(self):
        self.janela_op_b_f()
        self.opcao_4()  
    def jaop5(self):
        self.janela_op_b_f()
        self.opcao_5()  
    def jaop6(self):
        self.janela_op_b_f()
        self.opcao_6()
    def jaop7(self):
        self.janela_op_b_f()
        self.opcao_7() 
    
    def jaop8(self):
        self.janela_contagem()
        self.opcao_8()
    def jaop9(self):
        self.janela_contagem()
        self.opcao_9()
    def jaop10(self):
        self.janela_contagem()
        self.opcao_10()
    def jaop11(self):
        self.janela_contagem()
        self.opcao_11()

        

    
    def lista_frame_2(self):
        self.listaPro = ttk.Treeview(self.frame_2, height=3, columns=("col0","col1", "col2", "col3", "col4", "col5", "col6"))
        self.listaPro.heading("#0", text="")
        self.listaPro.heading("#1", text="Código")
        self.listaPro.heading("#2", text="Produto")
        self.listaPro.heading("#3", text="Saldo")
        self.listaPro.heading("#4", text="Saldo Mínimo")
        self.listaPro.heading("#5", text="Preço")
        self.listaPro.heading("#6", text="Custo")

        self.listaPro.column("#0", width=1)
        self.listaPro.column("#1", width=70)
        self.listaPro.column("#2", width=230)
        self.listaPro.column("#3", width=100)
        self.listaPro.column("#4", width=100)
        self.listaPro.column("#5", width=100)
        self.listaPro.column("#6", width=100)

        self.listaPro.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroll_lista = Scrollbar(self.frame_2, orient="vertical")
        self.listaPro.configure(yscroll=self.scroll_lista.set)
        self.scroll_lista.config(command=self.listaPro.yview)
        self.scroll_lista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)

        self.listaPro.bind("<Double-1>", self.OnDoubleClick)


    def menus(self):
        menubar = Menu(self.Janela_main)
        self.Janela_main.config(menu=menubar)
        funcionario_menu = Menu(menubar)
        funcoes_menu = Menu(menubar)

        def Quit(): self.Janela_main.destroy()

        menubar.add_cascade(label="Administração", menu= funcionario_menu)
        menubar.add_cascade(label="Sobre", menu= funcoes_menu)

        funcionario_menu.add_command(label="Sair", command=Quit)
        funcoes_menu.add_command(label="Limpar Produtos", command=self.limpa_tela)


    def janela_op_a(self):

        self.janela_2 = Toplevel()
        self.janela_2.title("Lista Com produtos e Preço Em Ordem Alfabética")
        self.janela_2.configure(background="blue")
        self.janela_2.geometry("500x800")
        self.janela_2.resizable(False, False)
        self.janela_2.transient(self.Janela_main)
        self.janela_2.focus_force()
        self.janela_2.grab_set()

        self.frame_3 = Frame(self.janela_2, bd= 4, bg= "white")
        self.frame_3.place(relx=0.02 , rely=0.05, relwidth=0.96, relheight=0.96)


        self.listaPrd = ttk.Treeview(self.frame_3, height=3, columns=("col0","col1", "col2"))
        self.listaPrd.heading("#0", text="")
        self.listaPrd.heading("#1", text="Produto")        
        self.listaPrd.heading("#2", text="Preço")
        
        self.listaPrd.column("#0", width=1)
        self.listaPrd.column("#1", width=230)        
        self.listaPrd.column("#2", width=100)

        self.listaPrd.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroll_lista2 = Scrollbar(self.frame_3, orient="vertical")
        self.listaPrd.configure(yscroll=self.scroll_lista2.set)
        self.scroll_lista2.config(command=self.listaPrd.yview)
        self.scroll_lista2.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)

        self.listaPrd.bind("<Double-1>", self.OnDoubleClick)

        self.opcao_1()


    def janela_op_b_f(self):
        self.janela_3 = Toplevel()
        self.janela_3.title("Consulta com os parametros Código, Produto, Saldo e Saldo Mínimo")
        self.janela_3.configure(background="blue")
        self.janela_3.geometry("500x800")
        self.janela_3.resizable(False, False)
        self.janela_3.transient(self.Janela_main)
        self.janela_3.focus_force()
        self.janela_3.grab_set()



        
        self.frame_4 = Frame(self.janela_3, bd= 4, bg= "white")
        self.frame_4.place(relx=0.02 , rely=0.05, relwidth=0.96, relheight=0.96)


        self.listaProd = ttk.Treeview(self.frame_4, height=3, columns=("col0","col1", "col2", "col3", "col4"))
        self.listaProd.heading("#0", text="")
        self.listaProd.heading("#1", text="Código")        
        self.listaProd.heading("#2", text="Produto")
        self.listaProd.heading("#3", text="Saldo")
        self.listaProd.heading("#4", text="Saldo Mínimo")
        
        self.listaProd.column("#0", width=1)
        self.listaProd.column("#1", width=50)        
        self.listaProd.column("#2", width=150)
        self.listaProd.column("#3", width=70)
        self.listaProd.column("#4", width=70)

        self.listaProd.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroll_lista3 = Scrollbar(self.frame_4, orient="vertical")
        self.listaProd.configure(yscroll=self.scroll_lista3.set)
        self.scroll_lista3.config(command=self.listaProd.yview)
        self.scroll_lista3.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)

        self.listaProd.bind("<Double-1>", self.OnDoubleClick)


    def janela_contagem(self):
        self.janela_4 = Toplevel()
        self.janela_4.title("Tabela De Contagem")
        self.janela_4.configure(background="blue")
        self.janela_4.geometry("600x800")
        self.janela_4.resizable(False, False)
        self.janela_4.transient(self.Janela_main)
        self.janela_4.focus_force()
        self.janela_4.grab_set()

        self.frame_5 = Frame(self.janela_4, bd= 4, bg= "white")
        self.frame_5.place(relx=0.02 , rely=0.05, relwidth=0.96, relheight=0.96)


        self.listaCtg = ttk.Treeview(self.frame_5, height=3, columns=("col0","col1", "col2", "col3", "col4", "col5"))
        self.listaCtg.heading("#0", text="")
        self.listaCtg.heading("#1", text="Quantidade")
        self.listaCtg.heading("#2", text="Produto")        
        self.listaCtg.heading("#3", text="Saldo")
        self.listaCtg.heading("#4", text="Saldo Mínimo")
        self.listaCtg.heading("#5", text="Rentabilidade")
        
        self.listaCtg.column("#0", width=1)
        self.listaCtg.column("#1", width=80)        
        self.listaCtg.column("#2", width=150)
        self.listaCtg.column("#3", width=50)
        self.listaCtg.column("#4", width=90)
        self.listaCtg.column("#5", width=100)

        self.listaCtg.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroll_lista4 = Scrollbar(self.frame_5, orient="vertical")
        self.listaCtg.configure(yscroll=self.scroll_lista4.set)
        self.scroll_lista4.config(command=self.listaCtg.yview)
        self.scroll_lista4.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)

        self.listaCtg.bind("<Double-1>", self.OnDoubleClick)
        



class Login():
    print("Login")
Aplicativo()

