#************** IMPORTAMOS *************************************************************#
from flask import Flask                                                                                    #* FLASK
from flask import render_template, redirect                                                                #* SITIO NORMAL
from flask import request                                                                                  #* BASE DE DATOS
from flaskext.mysql import MySQL                                                                           #* BASE DE DATOS
from dotenv import load_dotenv                                                                             #* VARIABLES DE ENTORNO
#import os                                                                                                 #* ...
#from flask import session
#from datetime import datetime
#from flask import send_from_directorys


#************** CONFIG HEAD ************************************************************#
app = Flask(__name__)

#************** CONFIG BD ************************************************************#

#CONECTAR BASE DE DATOS CON FORMULARIOS DE REGISTRO

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Site2022Lock'
app.config['MYSQL_DATABASE_DB'] = 'sist_admin'

mysql.init_app(app)

#************** SITE *******************************************************************#

#DEFINIR RUTA NORMALES DEL SITIO Y QUE PUEDAN VERSE
@app.route('/')
def index():
    return render_template('site/index.html')

@app.route('/dir_medico')
def dir_medico():
    return render_template('site/dir_medico.html')

#************** ADMIN *******************************************************************#


#DEFINIR RUTA NORMALES DEL SITIO Y QUE PUEDAN VERSE
@app.route('/admin')
def login():
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('/admin/login.html')



#AQUÍ SE LISTAN TODOS LOS DATOS DE LA BD QUE HE GUARDADO
@app.route('/admin/dir_medico')
def admin_dir_medico():

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM doc_registro")
    registro=cursor.fetchall()
    conexion.commit()
    #print(conexion)             #--> Así probé inicialmente para ver si conectaba
    print(registro)

    return render_template('/admin/dir_medico.html', registro=registro)



#CAPTACIÓN Y REGISTRO DE DATA / FORMULARIO / BD
@app.route('/admin/dir_medico/new', methods=['POST'])
def admin_dir_medico_new():
    #print(request.form['dir_med_nombre']) --> Así probé inicialmente

    doc_nombre = request.form['dir_med_nombre']
    doc_especialidad = request.form['dir_med_especialidad']
    doc_imagen = request.files['dir_med_imagen']
    doc_link = request.form['dir_med_descarga']

    sql = "INSERT INTO doc_registro (id,nombre,especialidad,imagen,boton) VALUES (NULL,%s,%s,%s,%s);"
    values = (doc_nombre, doc_especialidad, doc_imagen, doc_link)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,values)
    conexion.commit()

    #print(nombre,especialidad,imagen,link) #--> Así pruebo si pasa los datos
    return redirect ('/admin/dir_medico')



#ELIMINO REGISTRO DE BD
@app.route('/admin/dir_medico/delete', methods=['POST'])
def admin_dir_medico_delete():

    doc_id = request.form['dir_med_id']
    print(doc_id)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM doc_registro WHERE id=%s",(doc_id))
    conexion.commit()

    return redirect ('/admin/dir_medico')


#**************** Instanciamos **********************************************************#
if __name__ == '__main__':
    app.run(debug=True) 