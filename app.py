#************** IMPORTAMOS *************************************************************#
from flask import Flask                                                                                    #* PASO 1 *#
from flask import render_template                                                                          #* PASO 2 *#
from flask import request, redirect                                                                        #* PASO 3 *#
from flaskext.mysql import MySQL                                                                           #* PASO 4 *#
from dotenv import load_dotenv                                                                             #* PASO 4 * FALTA SOLUCIONAR EL ACCESO A BD EN ADELANTE#
import os
#from flask import session
#from datetime import datetime
#import os
#from flask import send_from_directorys


#************** CONFIG HEAD ************************************************************#
app = Flask(__name__)

#************** CONFIG BD ************************************************************#
#PASO 4 --> CONECTAR BASE DE DATOS

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Site2022Lock'
app.config['MYSQL_DATABASE_DB'] = 'sist_admin'

mysql.init_app(app)

#************** SITE *******************************************************************#

@app.route('/')
def index():
    return render_template('site/index.html')

@app.route('/dir_medico')
def dir_medico():
    return render_template('site/dir_medico.html')

#************** ADMIN *******************************************************************#

#PASO 1 --> PARA INICIAR LA APP, RUTAS Y PRUEBAS#
@app.route('/admin')
def login():
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('/admin/login.html')

@app.route('/admin/dir_medico')
def admin_dir_medico():
    #conexion = mysql.connect()   #--> Conex real, usaré más abajo
    #print(conexion)             --> Así probé inicialmente para ver si conectaba
    return render_template('/admin/dir_medico.html')



#REGISTRO DE DATA
@app.route('/admin/dir_medico/new', methods=['POST'])
def admin_dir_medico_new():
    #print(request.form['dir_med_nombre']) --> Así probé inicialmente

    nombre = request.form['dir_med_nombre']                                                                                           #* PASO 4 *
    especialidad = request.form['dir_med_especialidad']
    imagen = request.files['dir_med_imagen']
    link = request.form['dir_med_descarga']

    sql = "INSERT INTO doc_registro (id,nombre,especialidad,imagen,boton) VALUES (NULL,%s,%s,%s,%s);"                                  #* PASO 4 *
    values = (nombre, especialidad, imagen, link)

    conexion = mysql.connect()                                                                                                         #* PASO 4 *
    cursor = conexion.cursor()
    cursor.execute(sql,values)
    conexion.commit()

    #print(nombre,especialidad,imagen,link) #--> Así pruebo si pasa los datos
    return redirect ('/admin/dir_medico')



#**************** Instanciamos **********************************************************#
if __name__ == '__main__':
    app.run(debug=True) 