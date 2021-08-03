# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 09:44:40 2021

@author: criss
"""

#Clustering con el método k-means
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from IPython import get_ipython
from PaPDF import PaPDF
import sklearn

get_ipython().run_line_magic('matplotlib', 'inline')

#Importamos los datos
datos=pd.read_csv('../Python-CRUD-Tkinter5/Resultados/datos.csv',engine='python')

#Vemos las características del objeto datos
datos.info()

#Le pedimos que despliegue sus primeras filas
datos.head()

#Borrar dato
datos_variables=datos.drop({'Id'}, axis=1)

#Obtener datos estadísticos Descriptivos de vinos
datos_variables.describe()

#Normalizamos los valores de las características
datos_norm=(datos_variables-datos_variables.min())/(datos_variables.max()-datos_variables.min())
datos_norm
datos_norm.describe()

#Busqueda de la cantidad optima de clusteres
#Calculando que tan similares son los individuos dentro de los clusters
wcss = []

for i in range(1, 11):
    kmeans = KMeans(n_clusters = i, max_iter = 300)
    kmeans.fit(datos_norm)     #Aplicamos K-Means a la base de datos
    wcss.append(kmeans.inertia_)
    
#Graficando los resultados del WCSS para formar el Codo de Jambú
plt.plot(range(1,11), wcss)
plt.title("Codo de Jambú")
plt.xlabel('Número de Clusters')
plt.ylabel('WCSS') #WCSS. Es un indicador de que tan similares son los individuos dentro de los clusters
plt.savefig('../Python-CRUD-Tkinter5/Resultados/img/codo.png')
plt.show()

#Aplicando el método K-Means a la base de datos
clustering = KMeans(n_clusters = 12, max_iter = 300) #Crea el modelo
clustering.fit(datos_norm)  #Aplica el modelo a la base de datos

#Agregando la calsificación al archivo original
datos['KMeans_Clusters'] = clustering.labels_ #Los resultados del clustering se guardan el labels_ dentro del modelo
datos.head()
#Visualizando los clusters que se formaron

#Aplicarémos el análisis de componentes principales para darnos una idea de como se formaron los clusters
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
pca_datos = pca.fit_transform(datos_norm)
pca_datos_dif = pd.DataFrame(data = pca_datos, columns = ['Componente_1', 'Componente_2'])
pca_nombres_datos = pd.concat([pca_datos_dif, datos[['KMeans_Clusters']]], axis=1)

pca_nombres_datos

#Graficamos el resultado
fig = plt.figure(figsize = (6,6))

ax = fig.add_subplot(1,1,1)
ax.set_xlabel('Componente 1', fontsize = 15)
ax.set_ylabel('Componente 2', fontsize = 15)
ax.set_title('Componentes principales', fontsize = 20)

color_theme = np.array(["blue", "green", "orange", "black", "gray","red", "purple", "pink", "yellow", "brown",
                        "#3CFA64","#FF00C9"])
ax.scatter(x = pca_nombres_datos.Componente_1, y = pca_nombres_datos.Componente_2,
           c = color_theme[pca_nombres_datos.KMeans_Clusters], s =100)

plt.show()

#Grabamos los clusters (exportamos)

exportar = datos.to_csv('../Python-CRUD-Tkinter5/Resultados/ResultadosCSV.csv')

#Grabar plots en png
fig.savefig('../Python-CRUD-Tkinter5/Resultados/img/kms.png')


#Crear PDF
def crear_pdf(archivo):
    #Esta función creará el PDF
    with PaPDF(archivo) as pdf:
        # (x, y) son nuestras coordenadas para agregar los elementos al PDF
        pdf.addText(85, 290, "Método K-Means") #Agregamos texto plano al PDF
        # Agregar plot del resultado
        pdf.addImage('../Python-CRUD-Tkinter5/Resultados/img/kms.png', 30, 130, 150, 150)
        pdf.addText(20, 280, "Resultado de la aplicación del método K-Means")
        #Agregar fuente al PDF
        
        text = ""
        pdf.setLineThickness(0.5)
        pdf.setFontSize(8)
        w = pdf.getTextWidth(text)
        
        pdf.addPage()
        pdf.addText(95, 290, "Rasgos pt1")
        #Descripciones
        pdf.addLine(0, 275, 220, 275)
        text = "Rasgos De Acuario:"
        text2 = "Fortalezas: Progresista, original, independiente, humanitaria."
        text3 = "Debilidades: Huye de la expresión emocional, temperamental, intransigente, distante."
        text4 = "Gustos: divertirse con amigos, negocios arriesgados, luchar por causas, conversaciones intelectuales."
        text5 = "Disgustos: Limitaciones, promesas incumplidas, situaciones de soledad, aburridas o aburridas."
        pdf.addText(85, 270, text)
        pdf.addText(3, 265, text2)
        pdf.addText(3, 260, text3)
        pdf.addText(3, 255, text4)
        pdf.addText(3, 250, text5)
        pdf.addLine(0, 245, 220, 245)
        
        text6 = "Rasgos De Piscis:"
        text7 = "Fortalezas: compasivo, artístico, intuitivo, gentil, sabio, musical."
        text8 = "Debilidades: Temeroso, demasiado confiado, triste, deseo de escapar de la realidad, víctima o mártir."
        text9 = "Gustos: estar solo, amar, dormir, la música, el romance, la natación, los temas espirituales."
        text10 = "Disgustos: Sabelotodo, ser criticado, el pasado regresa para perseguirlo, crueldad de cualquier tipo."
        pdf.addText(85, 240, text6)
        pdf.addText(3, 235, text7)
        pdf.addText(3, 230, text8)
        pdf.addText(3, 225, text9)
        pdf.addText(3, 220, text10)
        pdf.addLine(0, 215, 220, 215)
        
        text11 = "Rasgos De Aries:"
        text12 = "Fortalezas: Valiente, decidido, seguro, entusiasta, optimista, honesto, apasionado."
        text13 = "Debilidades: impaciente, temperamental, de mal genio, impulsivo, agresivo."
        text14 = "Gustos: Ropa cómoda, asumir roles de liderazgo, desafíos físicos, deportes individuales."
        text15 = "Disgustos: Inactividad, retrasos, trabajo que no usa los talentos."
        pdf.addText(85, 210, text11)
        pdf.addText(3, 205, text12)
        pdf.addText(3, 200, text13)
        pdf.addText(3, 195, text14)
        pdf.addText(3, 190, text15)
        pdf.addLine(0, 185, 220, 185)
        
        text16 = "Rasgos De Tauro:"
        text17 = "Fortalezas: Confiable, paciente, práctico, dedicado, responsable, estable."
        text18 = "Debilidades: terco, posesivo, intransigente."
        text19 = "Gustos: la jardinería, la cocina, la música, el romance, ropa alta calidad, trabajar con las manos."
        text20 = "Disgustos: cambios repentinos, complicaciones, inseguridad de cualquier tipo, tejidos sintéticos."
        pdf.addText(85, 180, text16)
        pdf.addText(3, 175, text17)
        pdf.addText(3, 170, text18)
        pdf.addText(3, 165, text19)
        pdf.addText(3, 160, text20)
        pdf.addLine(0, 155, 220, 155)
        
        text21 = "Rasgos De Géminis:"
        text22 = "Fortalezas: Amable, cariñoso, curioso, adaptable, aprende rápidamente e intercambiar ideas."
        text23 = "Debilidades: Nervioso, inconsistente, indeciso."
        text24 = "Gustos: Música, libros, revistas, charlas con casi cualquier persona, viajes cortos por la ciudad."
        text25 = "Disgustos: estar solo, estar confinado, la repetición y la rutina."
        pdf.addText(85, 150, text21)
        pdf.addText(3, 145, text22)
        pdf.addText(3, 140, text23)
        pdf.addText(3, 135, text24)
        pdf.addText(3, 130, text25)
        pdf.addLine(0, 125, 220, 125)
        
        text26 = "Rasgos De Cáncer:"
        text27 = "Fortalezas: Tenaz, muy imaginativo, leal, emocional, comprensivo, persuasivo."
        text28 = "Debilidades: malhumorado, pesimista, suspicaz, manipulador, inseguro."
        text29 = "Gustos: el arte, los pasatiempos hogareños, relajarse cerca del agua o en el agua."
        text30 = "Disgustos: extraños, cualquier crítica a mamá, revelación de la vida personal."
        pdf.addText(85, 120, text26)
        pdf.addText(3, 115, text27)
        pdf.addText(3, 110, text28)
        pdf.addText(3, 105, text29)
        pdf.addText(3, 100, text30)
        pdf.addLine(0, 95, 220, 95)
        
        text31 = "Rasgos De Leo:"
        text32 = "Fortalezas: Creativo, apasionado, generoso, afectuoso, alegre, gracioso."
        text33 = "Debilidades: Arrogante, terco, egocéntrico, perezoso, inflexible."
        text34 = "Gustos: teatro, vacaciones, ser admirado, cosas caras, colores brillantes, divertirse con amigos"
        text35 = "Disgustos: ser ignorado, enfrentarse a una realidad difícil, no ser tratado como un rey o una reina."
        pdf.addText(85, 90, text31)
        pdf.addText(3, 85, text32)
        pdf.addText(3, 80, text33)
        pdf.addText(3, 75, text34)
        pdf.addText(3, 70, text35)
        pdf.addLine(0, 65, 220, 65)
        
        text36 = "Rasgos De Virgo:"
        text37 = "Fortalezas: Leal, analítico, amable, trabajador, práctico."
        text38 = "Debilidades: timidez, preocupación, demasiado crítico consigo mismo y con los demás."
        text39 = "Gustos: los animales, la comida sana, los libros, la naturaleza, la limpieza."
        text40 = "Disgustos: Descortesía, pedir ayuda, ocupar un lugar central."
        pdf.addText(85, 60, text36)
        pdf.addText(3, 55, text37)
        pdf.addText(3, 50, text38)
        pdf.addText(3, 45, text39)
        pdf.addText(3, 40, text40)
        pdf.addLine(0, 35, 220, 35)
        
        text41 = "Rasgos De Libra:"
        text42 = "Fortalezas: Lcooperativa, diplomática, cortés, imparcial, social."
        text43 = "Debilidades: Indeciso, evita confrontaciones, guarda rencor, autocompasión."
        text44 = "Gustos: la armonía, la gentileza, compartir con los demás, el aire libre."
        text45 = "Disgustos: la violencia, la injusticia, los bocazas, la conformidad."
        pdf.addText(85, 30, text41)
        pdf.addText(3, 25, text42)
        pdf.addText(3, 20, text43)
        pdf.addText(3, 15, text44)
        pdf.addText(3, 10, text45)
        pdf.addLine(0, 5, 220, 5)
        
        #Página3
        pdf.addPage()
        pdf.addText(95, 290, "Rasgos pt2")
        #Descripciones pt2
        pdf.addLine(0, 275, 220, 275)
        text46 = "Rasgos De Escorpio:"
        text47 = "Fortalezas: Ingenioso, poderoso, valiente, apasionado, un verdadero amigo."
        text48 = "Debilidades: Desconfianza, celos, manipuladores, violentos."
        text49 = "Gustos: la verdad, los hechos, tener razón, los talentos, las burlas, la pasión."
        text50 = "Disgustos: Deshonestidad, revelar secretos, superficialidad, charlas triviales."
        pdf.addText(85, 270, text46)
        pdf.addText(3, 265, text47)
        pdf.addText(3, 260, text48)
        pdf.addText(3, 255, text49)
        pdf.addText(3, 250, text50)
        pdf.addLine(0, 245, 220, 245)
        
        text46 = "Rasgos De Escorpio:"
        text47 = "Fortalezas: Ingenioso, poderoso, valiente, apasionado, un verdadero amigo."
        text48 = "Debilidades: Desconfianza, celos, manipuladores, violentos."
        text49 = "Gustos: la verdad, los hechos, tener razón, los talentos, las burlas, la pasión."
        text50 = "Disgustos: Deshonestidad, revelar secretos, superficialidad, charlas triviales."
        pdf.addText(85, 240, text46)
        pdf.addText(3, 235, text47)
        pdf.addText(3, 230, text48)
        pdf.addText(3, 225, text49)
        pdf.addText(3, 220, text50)
        pdf.addLine(0, 215, 220, 215)
        
        text51 = "Rasgos De Sagitario:"
        text52 = "Fortalezas: Generoso, idealista, gran sentido del humor."
        text53 = "Debilidades: Promete más de lo que puede cumplir, muy impaciente."
        text54 = "Gustos: Libertad, viajar, filosofía, estar al aire libre."
        text55 = "Disgustos: las personas pegajosas, limitaciones, teorías extravagantes, detalles."
        pdf.addText(85, 210, text51)
        pdf.addText(3, 205, text52)
        pdf.addText(3, 200, text53)
        pdf.addText(3, 195, text54)
        pdf.addText(3, 190, text55)
        pdf.addLine(0, 185, 220, 185)
        
        text56 = "Rasgos De Sagitario:"
        text57 = "Fortalezas: Responsable, disciplinado, autocontrol, buenos gerentes."
        text58 = "Debilidades: Sabelotodo, implacable, condescendiente, esperando lo peor."
        text59 = "Gustos: la familia, la tradición, la música, el estatus discreto, la artesanía de calidad."
        text60 = "Disgustos: casi todo en algún momento."
        pdf.addText(85, 180, text56)
        pdf.addText(3, 175, text57)
        pdf.addText(3, 170, text58)
        pdf.addText(3, 165, text59)
        pdf.addText(3, 160, text60)
        pdf.addLine(0, 155, 220, 155)
        
crear_pdf("../Python-CRUD-Tkinter5/Resultados/ResultadosPDF.pdf")