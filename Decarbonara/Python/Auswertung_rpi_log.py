#from typing import Collection
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
    
aktuelle_zeit = datetime.now().strftime('%Y%m%d-%H%M%S')  
                            # Format = 20211109-131856

i_fenster = tk.Tk()
i_fenster.title('Eingaben für die Auswertungsgrafik')
i_fenster.geometry('1210x570+10+10')

def button_action():

    p_server_name = p1.get()
    p_etage = p2.get()
    p_raum = p3.get()
    p_name_des_wertes = p4.get()

    if p_server_name == '':
        fehler.set('Bitte wählen Sie einen gültigen Server aus.')
    elif p_etage == '':
        fehler.set('Bitte wählen Sie einen gültige Etage aus.')
    elif p_raum == '':
        fehler.set('Bitte wählen Sie einen gültigen Raum aus.')
    else:
        fehler.set('')
        x_grafik = graf_erzeugen(p_server_name, p_etage, p_raum, p_name_des_wertes)
        n_grafik = ImageTk.PhotoImage(Image.open(x_grafik))
        l_grafik .configure(image=n_grafik)
        l_grafik.image = n_grafik

        #i_fenster.destroy()


def graf_erzeugen(p_server_name, p_etage, p_raum, p_name_des_wertes):

    db_verbindung = mysql.connector.connect(database='DeCarbonara',
                                                user='root',
                                            password='DeCarbonaras#2021') 
                                            #password=getpass("Enter password: "))
    cursor = db_verbindung.cursor()

    try:
        sql_anweisung = """SELECT * FROM import_messwerte 
                        WHERE server_name = %s AND etage = %s AND raum = %s AND name_des_wertes = %s
                        ORDER BY log_datum_vom"""
        sql_werte = (p_server_name, p_etage, p_raum, p_name_des_wertes)
             
        cursor.execute(sql_anweisung, sql_werte)
        sql_ergebnis = cursor.fetchall()
        cursor.close()
    
        xwerte_init = []
        ywerte_init = []
        xwerte = []
        ywerte = []
        for daten in sql_ergebnis:
            xwerte_init = [daten[1]]
            xwerte.append(xwerte_init)
            ywerte_init = [daten[7]]
            ywerte.append(ywerte_init)
            #print('Zeit: ' + str(daten[1]))
            #print('wert_num: ' + str(daten[7]))

    except mysql.connector.Error as error:
        print("Fehler beim Lesen der Tabelle import_messwerte: {}".format(error))

    plt.plot(xwerte, ywerte) #, color='green', marker='o', linestyle='dashed', linewidth=2, markersize=12)
    #plt.bar(xwerte, ywerte)
    plt.xlabel('Zeit-Achse')
    plt.ylabel('Temperatur')
    s_grafik = aktuelle_zeit + '_' + p_server_name + '_' + p_etage + '_' + p_raum + '.png'
    plt.savefig(s_grafik)
    #plt.show()
    return s_grafik


l_server_name = Label(i_fenster, text="Server: ", anchor='w').place(x=20, y=50, width=50, height=24)
l_etage = Label(i_fenster, text="Etage: ", anchor='w').place(x=20, y=80, width=50, height=24)
l_raum = Label(i_fenster, text="Raum: ", anchor='w').place(x=20, y=110, width=50, height=24)
l_name_des_wertes = Label(i_fenster, text="Wert: ", anchor='w').place(x=20, y=140, width=50, height=24)
fehler = tk.StringVar()
l_fehlerzeile = Label(i_fenster, text="hier", fg='red', textvariable=fehler, anchor='w').place(x=20, y=260, width=400, height=24)

s_grafik= ImageTk.PhotoImage(Image.open("leer_grafik.png"))
l_grafik = Label(i_fenster, image=s_grafik)
l_grafik.place(x=530, y=50)

p1 = tk.StringVar()
cb_server_name = ttk.Combobox(i_fenster, width=20, height=25, textvariable=p1)
cb_server_name['values'] = ('PI001',
                            'PI002',
                            'PI003')
cb_server_name.place(x=250, y=50)
#cb_server_name.current(0)

p2 = tk.StringVar()
cb_etage = ttk.Combobox(i_fenster, width=20, height=25, textvariable=p2)
cb_etage['values'] = ('KG',
                      'EG',
                      'OG1',
                      'DG')
cb_etage.place(x=250, y=80)
#cb_etage.current(0)

p3 = tk.StringVar()
cb_raum = ttk.Combobox(i_fenster, width=20, height=25, textvariable=p3)
cb_raum['values'] = ('Bad',
                     'Gäste_WC',
                     'Schlafzimmer',
                     'Wohnzimmer',
                     'Balkon',
                     'Arbeitszimmmer',
                     'Esszimmer',
                     'Küche',
                     'Büro_DG')
cb_raum.place(x=250, y=110)
#cb_raum.current(0)

p4 = tk.StringVar()
cb_name_des_wertes = ttk.Combobox(i_fenster, width=20, height=25, textvariable=p4)
cb_name_des_wertes['values'] = ('ACTUAL_TEMPERATURE',
                                'HUMIDITY', 'CURRENT_ILLUMINATION', 'MOTION')
cb_name_des_wertes.place(x=250, y=140)
cb_name_des_wertes.current(0)

ok_button = Button(i_fenster, text="Auswertungsgrafik erzeugen", command=button_action).place(x=20, y=200)
quit_button = Button(i_fenster, text="Beenden", command=i_fenster.destroy).place(x=370, y=200)

i_fenster.mainloop()
