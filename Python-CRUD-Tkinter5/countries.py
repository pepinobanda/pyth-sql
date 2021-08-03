import mysql.connector

class Countries:

    def __init__(self):
        self.cnn = mysql.connector.connect(host="localhost", user="root", 
        passwd="", database="signos")

    def __str__(self):
        datos=self.consulta_r()        
        aux=""
        for row in datos:
            aux=aux + str(row) + "\n"
        return aux
        
    def consulta_r(self):
        cur = self.cnn.cursor()
        cur.execute("SELECT * FROM registros")
        datos = cur.fetchall()
        cur.close()    
        return datos

    def buscar_r(self, Id):
        cur = self.cnn.cursor()
        sql= "SELECT * FROM registros WHERE Id = {}".format(Id)
        cur.execute(sql)
        datos = cur.fetchone()
        cur.close()    
        return datos
    
    def inserta_r(self,Alegre, Triste, Extrovertido, Introvertido, Amable, Docil, Enojon,
                  Empatico, Sociable, Penoso):
        cur = self.cnn.cursor()
        sql='''INSERT INTO registros (Alegre, Triste, Extrovertido, Introvertido, Amable, Docil, Enojon,
                  Empatico, Sociable, Penoso) 
        VALUES('{}', '{}', '{}', '{}','{}', '{}', '{}', '{}','{}', '{}')'''.format(Alegre, Triste, Extrovertido, Introvertido, Amable, Docil, Enojon,
                  Empatico, Sociable, Penoso)
        cur.execute(sql)
        n=cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n    

    def elimina_r(self,Id):
        cur = self.cnn.cursor()
        sql='''DELETE FROM registros WHERE Id = {}'''.format(Id)
        cur.execute(sql)
        n=cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n   

    def modifica_r(self,Id, Alegre, Triste, Extrovertido, Introvertido, Amable, Docil, Enojon,
                  Empatico, Sociable, Penoso):
        cur = self.cnn.cursor()
        sql='''UPDATE registros SET Alegre='{}', Triste='{}', Extrovertido='{}',
        Introvertido='{}', Amable='{}', Docil='{}', Enojon='{}',
        Empatico='{}',Sociable='{}', Penoso='{}' WHERE Id={}'''.format(Alegre, Triste, Extrovertido, Introvertido, Amable, Docil, Enojon,
                  Empatico, Sociable, Penoso,Id)
        cur.execute(sql)
        n=cur.rowcount
        self.cnn.commit()    
        cur.close()
        return n   
     
