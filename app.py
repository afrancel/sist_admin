#************** IMPORTAMOS *************************************************************#
from flask import Flask                           #* FLASK
from flask import render_template, redirect       #* SITIO NORMAL
from flask import request                         #* BASE DE DATOS
from flaskext.mysql import MySQL                  #* BASE DE DATOS
from dotenv import load_dotenv                    #* VARIABLES DE ENTORNO
from datetime import datetime                     #* CARGAR ARCHIVOS
from flask import send_from_directory             #* CARGAR IMAGENES
import os
from flask import session                         #* SESION DE USUARIOS

#************** CONFIG HEAD ************************************************************#
app = Flask(__name__)
app.secret_key="francel"

#************** CONFIG BD ************************************************************#

#CONECTAR BASE DE DATOS CON FORMULARIOS DE REGISTRO

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Site2022Lock'
app.config['MYSQL_DATABASE_DB'] = 'sist_admin'

mysql.init_app(app)

#************** SITE *************************************************************************#

#DEFINIR RUTA NORMALES DEL SITIO Y QUE PUEDAN VERSE********************************************

@app.route('/')
def index():
    return render_template('site/index.html')

@app.route('/nosotros')
def nosotros():
    return render_template('site/nosotros.html')

@app.route('/dir_medico')
def dir_medico():

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM doc_registro")
    registro=cursor.fetchall()
    conexion.commit()
    #print(conexion)             #--> Así probé inicialmente para ver si conectaba

    return render_template('site/dir_medico.html', registro=registro)

#LOGIN ***************************************************
@app.route('/login')
def login():    
    return render_template('site/login.html')

#RECIBIR DATOS DEL FORM  *********************************
@app.route('/login', methods=['POST'])
def login_post():

    #RECIBIR DATOS DEL FORM  *********************************
    login_user = request.form['login_user']
    login_pass = request.form['login_pass']
    #print(login_user, login_pass)

    #INICIAR SESION DE USUARIO *******************************
    if login_user=="admin" and login_pass=="admin":
        session['login'] = True
        session['Usuario'] = "Administrador"
        return redirect("/admin")
    
    return render_template('site/login.html', mensaje="Acceso Denegado")

#************** URLS CONFIG GRAL****************************************************************#

@app.route('/imgs/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(os.path.join('templates/imgs/'),imagen)

@app.route('/css/<archivocss>')
def css_link(archivocss):
    return send_from_directory(os.path.join('templates/css/'),archivocss)


#************** ADMIN ***************************************************************************#

#DEFINIR RUTA NORMALES DEL SITIO Y QUE PUEDAN VERSE **********************************************

@app.route('/admin')
def admin():

    return render_template('admin/index.html')


#CERRAR SESION DE USUARIO ************************************
@app.route('/admin/cerrar')
def admin_cerrar_sesion():
    session.clear()
    return redirect('/login')

#LISTAR TODOS LOS DATOS DE LA BD QUE HE GUARDADO ************************************************

@app.route('/admin/dir_medico')
def admin_dir_medico():

    if not 'login' in session:
        return redirect ('/login')

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM doc_registro")
    registro=cursor.fetchall()
    conexion.commit()
    #print(conexion)             #--> Así probé inicialmente para ver si conectaba
    print(registro)

    return render_template('/admin/dir_medico.html', registro=registro)



#GUARDAR REGISTROS CON FORMULARIO EN LA BD *******************************************************

@app.route('/admin/dir_medico/new', methods=['POST'])
def admin_dir_medico_new():
    #print(request.form['dir_med_nombre']) --> Así probé inicialmente

    #RECIBIR DATOS DEL FORM  *********************************
    doc_nombre = request.form['dir_med_nombre']
    doc_especialidad = request.form['dir_med_especialidad']
    doc_imagen = request.files['dir_med_imagen']
    doc_link = request.form['dir_med_descarga']


    #GUARDAR IMAGENES CONFIGURACIÓN **************************
    fecha = datetime.now()
    fecha_actual = fecha.strftime('%Y%H%M%S')

    if doc_imagen.filename!="":
       doc_imagen_new=fecha_actual+"_"+doc_imagen.filename
       doc_imagen.save("templates/imgs/"+doc_imagen_new) #aquí cambió el name de la img OJO


    #INSERTO EN LA BD TODA LA DATA RECIBIDA ******************
    sql = "INSERT INTO doc_registro (id,nombre,especialidad,imagen,boton) VALUES (NULL,%s,%s,%s,%s);"
    values = (doc_nombre, doc_especialidad, doc_imagen_new, doc_link)

    #CONEXION CON BD *****************************************
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,values)
    conexion.commit()

    #print(nombre,especialidad,imagen,link) #--> Así pruebo si pasa los datos
    return redirect ('/admin/dir_medico')



#ELIMINAR REGISTRO E IMAGEN DE BD ***************************************************************

@app.route('/admin/dir_medico/delete', methods=['POST'])
def admin_dir_medico_delete():

    doc_id = request.form['dir_med_id']
    print(doc_id)

    #ELIMINO IMAGEN *******************************************
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT imagen FROM doc_registro WHERE id = %s;", (doc_id))
    doc_registro = cursor.fetchall()
    conexion.commit()
    print(doc_registro)

    if os.path.exists("templates/imgs/"+str(doc_registro[0][0])):
        os.unlink("templates/imgs/"+str(doc_registro[0][0]))

    #ELIMINO REGISTRO  *****************************************
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM doc_registro WHERE id=%s",(doc_id))
    conexion.commit()    
    

    return redirect ('/admin/dir_medico')


#**************** Instanciamos **********************************************************#
if __name__ == '__main__':
    app.run(debug=True) 