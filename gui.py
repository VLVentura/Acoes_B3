#!/usr/bin/env python
# coding: utf-8

# In[2]:


import tkinter as tk
from tkinter import *
import os
from tkinter import filedialog
import pandas as pd
import sqlite3
from tkcalendar import Calendar, DateEntry
from tkinter import ttk
import datetime
from datetime import date


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()
class Page1(Page):
    def load_txt2db(self):
        print(self.file)
    def Load_archive(self):
        self.file = filedialog.askopenfilenames()
        self.loadBtn.configure(text=os.path.basename(self.file[0]))
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        
        def Text_box_state():
            if self.CheckVar.get() == 0:
                self.M_entry.configure(state='disable')
            else:
                self.M_entry.configure(state='normal')
        loadLabel = Label(self, text="Ações")
        loadLabel.grid(column=0,row=0)
        
        self.loadBtn = Button(self, text="Carregar arquivo", command= self.Load_archive )
        self.loadBtn.grid(column=1,row=0)
        self.CheckVar = tk.IntVar()
        self.M_entry = Entry(self,width=10,state='disable')
        self.M_entry.grid(column=1,row=3)
        self.check = Checkbutton(self, text='Minimo volume medio de negociação',variable=self.CheckVar,command=Text_box_state)
        self.check.grid(column=0,row=2)
        
        MINMED = Label(self, text="Valor minimo medio:   ")
        MINMED.grid(column=0,row=3)
        fBtn = Button(self, text="Carregar banco de dados", command=self.load_txt2db )
        fBtn.grid(column=0,row=5,pady=(40,0))
        
        self.CheckVar2 = tk.IntVar()
        self.check2 = Checkbutton(self, text='Ignorar ações não negociadas em todas as datas',variable=self.CheckVar2,command=Text_box_state)
        self.check2.grid(column=0,row=4)

        
        
class Page2(Page): #segunda pagina, pagina de querys
    
    ## ação do botão Carregar Dados
    def load_tables(self):
        if self.CheckVar.get() == 1: ## pega a data final, caso marcado
            print(self.date_f.get_date())
        elif self.CheckVar2.get() == 1: ## pega o n de cotações caso marco
            print(self.NumCot.get())
        else: ## caso nenhum seja marcado
            pass
        
        
    ## habilita os campos baseado no check, também impede de marcar os dos ao mesmo tempo
    def Text_box_state(self): 
        if self.CheckVar.get() == 0:
            self.date_f.configure(state='disable')
        else:
            self.date_f.configure(state='normal')
        if self.CheckVar2.get() == 0:
            self.NumCot.configure(state='disable')
        else:
            self.NumCot.configure(state='normal')
        if self.CheckVar.get() == 1 and self.CheckVar2.get() == 1:
            self.date_f.configure(state='disable')
            self.NumCot.configure(state='disable')
            self.check.deselect()
            self.check2.deselect()
            
    ## inicialização do menu
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs) 
        s = ttk.Style(self)
        s.theme_use('clam')
        
        label = tk.Label(self, text="Ler dados da contação de ações")
        label.grid(column=0,row=0)
        labelDate = Label(self,text="Data inicial")
        labelDate.grid(column=0,row=1)
        
        self.date_i = DateEntry(self, selectmode="day",date_pattern='y-mm-dd') #calendario da data inicial
        self.date_i.grid(column= 1, row = 1)
        self.conn = sqlite3.connect('data_acoes.db') #conecta ao db
        
        labelDate2 = Label(self,text="Data Final")
        labelDate2.grid(column=0,row=3)
        
        self.date_f = DateEntry(self,state='disable',date_pattern='y-mm-dd') # Calendario da data final
        self.date_f.grid(column= 1, row = 3)
        self.CheckVar = tk.IntVar()
        self.check = Checkbutton(self,variable=self.CheckVar,
                                 command=self.Text_box_state) #Checkbutton que armazena o valor em CheckVar e chama Text_box_state()
        self.check.grid(column=0,row=3,padx=(0,90))
                
        label2 = Label(self,text="Nº de contações")
        label2.grid(column=0,row=4,padx=(40,0))
        
        self.CheckVar2 = tk.IntVar()
        self.check2 = Checkbutton(self,variable=self.CheckVar2,command=self.Text_box_state) #Checkbutton pra nº de cot
        self.check2.grid(column=0,row=4,padx=(0,90))
        self.NumCot = Entry(self,width=10,state="disable")
        self.NumCot.grid(column=1,row=4)
        
        fBtn = ttk.Button(self, text="Carregar dados", command = self.load_tables) # butão que inicia a função load_tables
        fBtn.grid(column=0,row=6,pady=(40,0))
        
class MainView(tk.Frame):  #inicializa as duas paginas e o as abas.
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        
        p1 = Page1(self)
        p2 = Page2(self)
        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = ttk.Button(buttonframe, text="Page 1", command=p1.lift)
        b2 = ttk.Button(buttonframe, text="Page 2", command=p2.lift)

        b1.pack(side="left")
        b2.pack(side="left")
        p1.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()

