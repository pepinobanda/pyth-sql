
from tkinter import *
from tkinter import ttk
from countries import *
from tkinter import messagebox
import pyodbc
import pandas as pd


class Ventana(Frame):
    
    regis = Countries()
        
    def __init__(self, master=None):
        super().__init__(master,width=1360, height=520)
        self.master = master
        self.pack()
        self.create_widgets()
        self.llenaDatos()
        self.habilitarCajas("disabled")  
        self.habilitarBtnOper("normal")
        self.habilitarBtnGuardar("disabled")  
        self.id=-1      
                   
    #Métodos 
    def habilitarCajas(self,estado):
        self.txtAlegre.configure(state=estado)
        self.txtTriste.configure(state=estado)
        self.txtExtrovertido.configure(state=estado)
        self.txtIntrovertido.configure(state=estado)
        self.txtAmable.configure(state=estado)
        self.txtDocil.configure(state=estado)
        self.txtEnojon.configure(state=estado)
        self.txtEmpatico.configure(state=estado)
        self.txtSociable.configure(state=estado)
        self.txtPenoso.configure(state=estado)
        
        
    def habilitarBtnOper(self,estado):
        self.btnNuevo.configure(state=estado)                
        self.btnModificar.configure(state=estado)
        self.btnEliminar.configure(state=estado)
        self.btnExportar.configure(state=estado)
        self.btnPDF.configure(state=estado)
        
    def habilitarBtnGuardar(self,estado):
        self.btnGuardar.configure(state=estado)                
        self.btnCancelar.configure(state=estado)                
        
    def limpiarCajas(self):
        self.txtAlegre.delete(0,END)
        self.txtTriste.delete(0,END)
        self.txtExtrovertido.delete(0,END)
        self.txtIntrovertido.delete(0,END)
        self.txtAmable.delete(0,END)
        self.txtDocil.delete(0,END)
        self.txtEnojon.delete(0,END)
        self.txtEmpatico.delete(0,END)
        self.txtSociable.delete(0,END)
        self.txtPenoso.delete(0,END)
        
    def limpiaGrid(self):
        for item in self.grid.get_children():
            self.grid.delete(item)
                
    def llenaDatos(self):
        datos = self.regis.consulta_r()        
        for row in datos:            
            self.grid.insert("",END,text=row[0], values=(row[1],row[2], row[3],row[4],row[5],
                                                         row[6],row[7],row[8],row[9],row[10]))
        
        if len(self.grid.get_children()) > 0:
            self.grid.selection_set( self.grid.get_children()[0] )
            
    def fNuevo(self):         
        self.habilitarCajas("normal")  
        self.habilitarBtnOper("disabled")
        self.habilitarBtnGuardar("normal")
        self.limpiarCajas()        
        self.txtAlegre.focus()
    
    def fGuardar(self): 
        if self.id ==-1:       
            self.regis.inserta_r(self.txtAlegre.get(),self.txtTriste.get(),self.txtExtrovertido.get(),self.txtIntrovertido.get(),
                                 self.txtAmable.get(),self.txtDocil.get(),self.txtEnojon.get(),self.txtEmpatico.get(),
                                 self.txtSociable.get(),self.txtPenoso.get())            
            messagebox.showinfo("Insertar", 'Elemento insertado correctamente.')
        else:
            self.regis.modifica_r(self.id,
                                 self.txtAlegre.get(),self.txtTriste.get(),self.txtExtrovertido.get(),self.txtIntrovertido.get(),
                                 self.txtAmable.get(),self.txtDocil.get(),self.txtEnojon.get(),self.txtEmpatico.get(),
                                 self.txtSociable.get(),self.txtPenoso.get())
            messagebox.showinfo("Modificar", 'Elemento modificado correctamente.')
            self.id = -1            
        self.limpiaGrid()
        self.llenaDatos() 
        self.limpiarCajas() 
        self.habilitarBtnGuardar("disabled")      
        self.habilitarBtnOper("normal")
        self.habilitarCajas("disabled")
                    
    def fModificar(self):        
        selected = self.grid.focus()                               
        clave = self.grid.item(selected,'text')        
        if clave == '':
            messagebox.showwarning("Modificar", 'Debes seleccionar un elemento.')            
        else:            
            self.id= clave  
            self.habilitarCajas("normal")                         
            valores = self.grid.item(selected,'values')
            self.limpiarCajas()                  
            self.txtAlegre.insert(0,valores[0])
            self.txtTriste.insert(0,valores[1])
            self.txtExtrovertido.insert(0,valores[2])
            self.txtIntrovertido.insert(0,valores[3]) 
            self.txtAmable.insert(0,valores[4]) 
            self.txtDocil.insert(0,valores[5]) 
            self.txtEnojon.insert(0,valores[6]) 
            self.txtEmpatico.insert(0,valores[7]) 
            self.txtSociable.insert(0,valores[8]) 
            self.txtPenoso.insert(0,valores[9]) 
            
            self.habilitarBtnOper("disabled")
            self.habilitarBtnGuardar("normal")
            self.txtAlegre.focus()
                                        
    def fEliminar(self):
        selected = self.grid.focus()                               
        clave = self.grid.item(selected,'text')        
        if clave == '':
            messagebox.showwarning("Eliminar", 'Debes seleccionar un elemento.')            
        else:                           
            data = str(clave)
            r = messagebox.askquestion("Eliminar", "Deseas eliminar el registro seleccionado?\n" + data)            
            if r == messagebox.YES:
                n = self.regis.elimina_r(clave)
                if n == 1:
                    messagebox.showinfo("Eliminar", 'Elemento eliminado correctamente.')
                    self.limpiaGrid()
                    self.llenaDatos()
                else:
                    messagebox.showwarning("Eliminar", 'No fue posible eliminar el elemento.')
                            
    def fCancelar(self):
        r = messagebox.askquestion("Calcelar", "Esta seguro que desea cancelar la operación actual")
        if r == messagebox.YES:
            self.limpiarCajas() 
            self.habilitarBtnGuardar("disabled")      
            self.habilitarBtnOper("normal")
            self.habilitarCajas("disabled")
            
    #Metodo exportar SQL a CSV
    def sqlTcsv(self):
        conn = mysql.connector.connect(host="localhost", user="root", 
        passwd="", database="signos")
        
        sql_query = pd.read_sql_query('''
                              SELECT * FROM registros
                              ''', conn) 
        df = pd.DataFrame(sql_query)
        df.to_csv (r'../Python-CRUD-Tkinter5/Resultados/datos.csv', index = False)
        messagebox.showinfo("Exportar datos de SQL a CSV", 'Los elementos se han exportado de manera exitosa.')
            
        
            
    def resultados(self):
        import kmeans as km
        messagebox.showinfo("Método K-Means", 'El método K-Means se ha ejecutado de manera exitosa en los datos.')
        
            
    #Crear ventana gráfica
    def create_widgets(self):
        frame1 = Frame(self, bg="#bfdaff")
        frame1.place(x=0,y=0,width=93, height=259)    
        #Botones CRUD
        self.btnNuevo=Button(frame1,text="Nuevo", command=self.fNuevo, bg="blue", fg="white")
        self.btnNuevo.place(x=5,y=50,width=80, height=30 )        
        self.btnModificar=Button(frame1,text="Modificar", command=self.fModificar, bg="blue", fg="white")
        self.btnModificar.place(x=5,y=90,width=80, height=30)                
        self.btnEliminar=Button(frame1,text="Eliminar", command=self.fEliminar, bg="blue", fg="white")
        self.btnEliminar.place(x=5,y=130,width=80, height=30)
        
        #Boton SQL a CSV
        self.btnExportar=Button(frame1,text="SQL-A-CSV", command=self.sqlTcsv, bg="blue", fg="white")
        self.btnExportar.place(x=5,y=170,width=80, height=30 )
        
        #Boton plots a PDF
        self.btnPDF=Button(frame1,text="Aplicar K-Means", command=self.resultados, bg="blue", fg="white")
        self.btnPDF.place(x=5,y=210,width=80, height=30 ) 
        
        
        frame2 = Frame(self,bg="#d3dde3" )
        frame2.place(x=95,y=0,width=400, height=600)                        
        lbl1 = Label(frame2,text="Alegre: ")
        lbl1.place(x=3,y=5)        
        self.txtAlegre=Entry(frame2)
        self.txtAlegre.place(x=3,y=25,width=140, height=20)
        lbl2 = Label(frame2,text="Triste: ")
        lbl2.place(x=3,y=55)        
        self.txtTriste=Entry(frame2)
        self.txtTriste.place(x=3,y=75,width=140, height=20)        
        lbl3 = Label(frame2,text="Extrovertido ")
        lbl3.place(x=3,y=105)        
        self.txtExtrovertido=Entry(frame2)
        self.txtExtrovertido.place(x=3,y=125,width=140, height=20)        
        lbl4 = Label(frame2,text="Introvertido: ")
        lbl4.place(x=3,y=155)        
        self.txtIntrovertido=Entry(frame2)
        self.txtIntrovertido.place(x=3,y=175,width=140, height=20) 
        
        lbl5 = Label(frame2,text="Amable: ")
        lbl5.place(x=3,y=205)        
        self.txtAmable=Entry(frame2)
        self.txtAmable.place(x=3,y=225,width=140, height=20)
        lbl6 = Label(frame2,text="Docil: ")
        lbl6.place(x=3,y=255)        
        self.txtDocil=Entry(frame2)
        self.txtDocil.place(x=3,y=275,width=140, height=20) 
        lbl7 = Label(frame2,text="Enojon: ")
        lbl7.place(x=3,y=305)        
        self.txtEnojon=Entry(frame2)
        self.txtEnojon.place(x=3,y=325,width=140, height=20) 
        lbl8 = Label(frame2,text="Empatico: ")
        lbl8.place(x=3,y=355)        
        self.txtEmpatico=Entry(frame2)
        self.txtEmpatico.place(x=3,y=375,width=140, height=20) 
        lbl9 = Label(frame2,text="Sociable: ")
        lbl9.place(x=3,y=405)        
        self.txtSociable=Entry(frame2)
        self.txtSociable.place(x=3,y=425,width=140, height=20) 
        lbl10 = Label(frame2,text="Penoso: ")
        lbl10.place(x=3,y=455)        
        self.txtPenoso=Entry(frame2)
        self.txtPenoso.place(x=3,y=475,width=140, height=20) 
        
        self.btnGuardar=Button(frame2,text="Guardar", command=self.fGuardar, bg="green", fg="white")
        self.btnGuardar.place(x=170,y=475,width=60, height=30)
        self.btnCancelar=Button(frame2,text="Cancelar", command=self.fCancelar, bg="red", fg="white")
        self.btnCancelar.place(x=290,y=475,width=60, height=30)         
        frame3 = Frame(self,bg="yellow" )
        frame3.place(x=280,y=0,width=920, height=259)                      
        self.grid = ttk.Treeview(frame3, columns=("col1","col2","col3","col4","col5","col6","col7","col8","col9","col10"))        
        self.grid.column("#0",width=60)
        self.grid.column("col1",width=70, anchor=CENTER)
        self.grid.column("col2",width=90, anchor=CENTER)
        self.grid.column("col3",width=90, anchor=CENTER)
        self.grid.column("col4",width=90, anchor=CENTER)
        self.grid.column("col5",width=90, anchor=CENTER)
        self.grid.column("col6",width=70, anchor=CENTER)
        self.grid.column("col7",width=90, anchor=CENTER)
        self.grid.column("col8",width=90, anchor=CENTER)
        self.grid.column("col9",width=90, anchor=CENTER)
        self.grid.column("col10",width=90, anchor=CENTER) 
          
        self.grid.heading("#0", text="Id", anchor=CENTER)
        self.grid.heading("col1", text="Alegre", anchor=CENTER)
        self.grid.heading("col2", text="Triste", anchor=CENTER)
        self.grid.heading("col3", text="Extrovertido", anchor=CENTER)
        self.grid.heading("col4", text="Introvertido", anchor=CENTER)
        self.grid.heading("col5", text="Amable", anchor=CENTER)
        self.grid.heading("col6", text="Dócil", anchor=CENTER)
        self.grid.heading("col7", text="Enojón", anchor=CENTER)
        self.grid.heading("col8", text="Empático", anchor=CENTER)
        self.grid.heading("col9", text="Socialble", anchor=CENTER)
        self.grid.heading("col10", text="Penoso", anchor=CENTER)  
                
        self.grid.pack(side=LEFT,fill = Y)        
        sb = Scrollbar(frame3, orient=VERTICAL)
        sb.pack(side=RIGHT, fill = Y)
        self.grid.config(yscrollcommand=sb.set)
        sb.config(command=self.grid.yview)
        self.grid['selectmode']='browse'        