from flask import Flask
from flask import render_template, request, redirect ,url_for#acceder a las rutas 
from flaskext.mysql import MySQL #para la conexion a la base de datos
from datetime import datetime 
from flask import send_from_directory #mostrar imagenes
import firebase_admin
from firebase_admin import credentials, storage
import psycopg2

import os #verificar carpetas o crearlas para evitar errores

app = Flask(__name__)


# Ruta del archivo de credenciales relativa al directorio actual
ruta_credenciales = os.path.join(os.path.dirname(__file__), 'JSON/imagenes-web-5c4f6-firebase-adminsdk-49ckf-94533fe483.json')

#credenciales para firebase
cred = credentials.Certificate(ruta_credenciales)
firebase_admin.initialize_app(cred, {'projectId': 'imagenes-web-5c4f6', 'storageBucket': 'imagenes-web-5c4f6.appspot.com'})

# Obtiene una instancia del bucket de almacenamiento
bucket = storage.bucket()

# Configuración de la conexión a la base de datos
conn = psycopg2.connect(
    host='rajje.db.elephantsql.com',
    user='pgmnlggy',
    password='My3_pA_ZLonoQQUOld8dHhXitq9ijiFS',
    database='pgmnlggy'
)


@app.route('/')
def index():
    return render_template('sitio/inicio.html')

#para retornar la imagen y mostarla en pantalla
@app.route('/img/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(os.path.join('templates/sitio/temp_img'),imagen)




#seccion de productos
@app.route('/index_muestra_de_productos')
def index_productos():
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    recepcion = cursor.fetchall()
    return render_template('sitio/index_muestra_de_productos.html',recepcion = recepcion)

#mascotas
@app.route('/mascotas')
def index_mascotas():
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mascotas")
    recepcion = cursor.fetchall()
    return render_template('sitio/mascotas.html',recepcion = recepcion)

#accesorios
@app.route('/accesorios')
def index_accesorios():
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accesorios")
    recepcion = cursor.fetchall()
    return render_template('sitio/accesorios.html',recepcion = recepcion)


@app.route('/carrito')
def carrito():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM carrito")
    recepcion = cursor.fetchall()

    return render_template('carrito/index.html',recepcion = recepcion)

@app.route('/carrito/guardar', methods = ['POST'])
def carrito_guardar():
    _id = request.form['txtID']

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = %s", (_id,))
    product = cursor.fetchone()

    _nombre = product[1]
    _descripcion = product[2]
    _color = product[3]
    _precio = product[4]
    _imagen = product[5]
    _cantidad = product[6]    

    sql = "INSERT INTO carrito (nombre, descripcion, color, precio, imagen, cantidad) VALUES (%s, %s, %s, %s, %s, %s);"
    datos = (_nombre, _descripcion, _color, _precio, _imagen, _cantidad)

    
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/index_muestra_de_productos')


@app.route('/carrito/eliminar', methods=['POST'])
def carrito_eliminar():
    _id = request.form['txtID']

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM carrito WHERE id = %s", (_id,))
        conn.commit()

        return redirect('/carrito')
    except psycopg2.Error as e:
        conn.rollback()  # Revertir la transacción abortada
        print("Error en la transacción:", e)
        # Realizar cualquier otra acción de manejo de errores necesaria
        return redirect('/error')



#vista de usuario
@app.route('/inicio/usuario/<id>')
def vista_usuario_inicio(id):
    _id = id

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_pass WHERE id = %s", (_id,))
    user = cursor.fetchall()

    return render_template('sitio/vista_usuario/inicio.html', user=user)



@app.route('/carrito/usuario/<id>')
def vista_usuario_carrito(id):
    _id = id

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_pass WHERE id = %s", (_id,))
    user = cursor.fetchall()

    return render_template('sitio/vista_usuario/carrito.html', user=user)


@app.route('/productos/usuario/<id>')
def vista_usuario_productos(id):
    _id = id

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_pass WHERE id = %s", (_id,))
    user = cursor.fetchall()

    cursor.execute("SELECT * FROM productos")
    recepcion = cursor.fetchall()

    return render_template('sitio/vista_usuario/index_muestra_de_productos.html', recepcion=recepcion, user=user)


    

@app.route('/login/inicio')
def login_inicio():
    return render_template('login/login-crear-inicio.html')

@app.route('/login/creacion_1')
def login_creacion_1():
    return render_template('/login/login-creacion.html')

@app.route('/login/login-crear-inicio/Save_data', methods=['POST'])
def login_create_save_data():
    _nombre = request.form['txtName']
    _email = request.form['txtEmail']
    _password = request.form['txtPass']
    cursor = conn.cursor()
    sql = "INSERT INTO user_pass (Nombre, Email, Password) VALUES (%s, %s, %s) RETURNING Id;"
    datos = (_nombre, _email, _password)
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/login/creacion_1')



@app.route('/login/login-crear-inicio/check', methods=['POST'])
def login_check():
    _email = request.form['txtUser']
    _password = request.form['txtPassword']
    cursor = conn.cursor()
    sql = "SELECT * FROM user_pass;"
    cursor.execute(sql)
    recepcion = cursor.fetchall()

    for data in recepcion:
        if data[2] == _email and data[3] == _password:
            if data[0] == 1:
                return redirect('/admin')
            else:
                id = data[0]
                return redirect(url_for('vista_usuario_inicio', id=id))
    
    return redirect('/login/inicio')

           

    


@app.route('/login/recuperar')
def login_recuperar():
    return render_template('login/login-recuperar.html')




@app.route('/admin')
def admin_index():

    cursor = conn.cursor()

    sql = "SELECT * FROM user_pass;"
    cursor.execute(sql)
    recepcion = cursor.fetchall()

    cursor.close()

    return render_template('admin/index.html', recepcion=recepcion)

@app.route('/admin/accesorios')
def admin_accesorios():
    cursor = conn.cursor()

    sql = "SELECT * FROM accesorios;"
    cursor.execute(sql)
    recepcion = cursor.fetchall()

    cursor.close()
    return render_template('admin/accesorios.html', recepcion=recepcion)

@app.route('/admin/productos')
def admin_productos():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    recepcion = cursor.fetchall()
    cursor.close()
    return render_template('admin/productos.html', recepcion=recepcion)


@app.route('/admin/mascotas')
def admin_mascotas():
    cursor = conn.cursor()

    sql = "SELECT * FROM mascotas;"
    cursor.execute(sql)
    recepcion = cursor.fetchall()

    cursor.close()
    return render_template('admin/mascotas.html', recepcion = recepcion)

@app.route('/admin/crear_user', methods=['POST'])
def admin_crear_user():
    _nombre = request.form['txtName']
    _email = request.form['txtEmail']
    _Password = request.form['txtPass']

    sql = "INSERT INTO \"user_pass\" (\"Nombre\", \"Email\", \"Password\") VALUES (%s, %s, %s);"
    datos = (_nombre, _email, _Password)

    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    cursor.close()

    return redirect('/admin')

@app.route('/admin/crear_product',methods = ['POST'])
def admin_crear_product():
    _nombre = request.form['txtName']
    _descripcion = request.form['txtDescr']
    _color = request.form['txtColor']
    _precio = request.form['txtPrecio']
    _imagen = request.files['txtImg']
    _cantidad = request.form['txtCant']
    _imagen2 = request.files['txtImg2']
    
    tiempo = datetime.now()
    HoraActual= tiempo.strftime('%Y%H%M%S')

    if _imagen.filename !="":
        nuevoNombre = HoraActual+"_"+_imagen.filename
        if not os.path.exists("app/templates/sitio/temp_img/"):
            os.makedirs("app/templates/sitio/temp_img/")
        _imagen.save("app/templates/sitio/temp_img/"+nuevoNombre)
    
    if _imagen2.filename !="":
        nuevoNombre2 = HoraActual+"_2"+_imagen2.filename
        if not os.path.exists("app/templates/sitio/temp_img/"):
            os.makedirs("app/templates/sitio/temp_img/")
        _imagen2.save("app/templates/sitio/temp_img/"+nuevoNombre2)

    sql = "INSERT INTO productos (nombre, descripcion, color, precio, imagen, cantidad, imagen2) VALUES (%s, %s, %s, %s, %s, %s,%s);"
    datos = (_nombre, _descripcion, _color, _precio, nuevoNombre, _cantidad,nuevoNombre2)


    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    cursor.close()

    return redirect('/admin/productos')


@app.route('/admin/crear_mascotas',methods = ['POST'])
def admin_crear_mascota():
    _nombre = request.form['txtName']
    _descripcion = request.form['txtDescr']
    _color = request.form['txtColor']
    _precio = request.form['txtPrecio']
    _imagen = request.files['txtImg']
    _cantidad = request.form['txtCant']
    _imagen2 = request.files['txtImg2']
    
    tiempo = datetime.now()
    HoraActual= tiempo.strftime('%Y%H%M%S')

    if _imagen.filename !="":
        nuevoNombre = HoraActual+"_"+_imagen.filename
        if not os.path.exists("app/templates/sitio/temp_img/"):
            os.makedirs("app/templates/sitio/temp_img/")
        _imagen.save("app/templates/sitio/temp_img/"+nuevoNombre)
    
    if _imagen2.filename !="":
        nuevoNombre2 = HoraActual+"_2"+_imagen2.filename
        if not os.path.exists("app/templates/sitio/temp_img/"):
            os.makedirs("app/templates/sitio/temp_img/")
        _imagen2.save("app/templates/sitio/temp_img/"+nuevoNombre2)

    sql = "INSERT INTO mascotas (nombre, descripcion, color, precio, imagen, cantidad, imagen2) VALUES (%s, %s, %s, %s, %s, %s,%s);"
    datos = (_nombre, _descripcion, _color, _precio, nuevoNombre, _cantidad,nuevoNombre2)


    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    cursor.close()

    return redirect('/admin/mascotas')

@app.route('/admin/crear_accesorios',methods = ['POST'])
def admin_crear_accesorios():
    _nombre = request.form['txtName']
    _descripcion = request.form['txtDescr']
    _color = request.form['txtColor']
    _precio = request.form['txtPrecio']
    _imagen = request.files['txtImg']
    _cantidad = request.form['txtCant']
    _imagen2 = request.files['txtImg2']
    
    tiempo = datetime.now()
    HoraActual= tiempo.strftime('%Y%H%M%S')

    if _imagen.filename !="":
        nuevoNombre = HoraActual+"_"+_imagen.filename
        if not os.path.exists("app/templates/sitio/temp_img/"):
            os.makedirs("app/templates/sitio/temp_img/")
        _imagen.save("app/templates/sitio/temp_img/"+nuevoNombre)
    
    if _imagen2.filename !="":
        nuevoNombre2 = HoraActual+"_2"+_imagen2.filename
        if not os.path.exists("app/templates/sitio/temp_img/"):
            os.makedirs("app/templates/sitio/temp_img/")
        _imagen2.save("app/templates/sitio/temp_img/"+nuevoNombre2)

    sql = "INSERT INTO accesorios (nombre, descripcion, color, precio, imagen, cantidad, imagen2) VALUES (%s, %s, %s, %s, %s, %s,%s);"
    datos = (_nombre, _descripcion, _color, _precio, nuevoNombre, _cantidad,nuevoNombre2)


    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    cursor.close()

    return redirect('/admin/accesorios')

@app.route('/admin/borrar_productos', methods=['POST'])
def admin_borrar_product():
    _id = request.form['txtID']

    # Eliminar imagen de la carpeta
    cursor = conn.cursor()
    cursor.execute("SELECT imagen FROM productos WHERE id = %s", (_id,))
    imagen_result = cursor.fetchone()
    conn.commit()

    if imagen_result:
        imagen = imagen_result[0]
        if os.path.exists("app/templates/sitio/temp_img/" + str(imagen)):
            os.unlink("app/templates/sitio/temp_img/" + str(imagen))

    # Eliminar de la base de datos
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (_id,))
    conn.commit()

    return redirect('/admin/productos')

@app.route('/admin/borrar_accesorios', methods=['POST'])
def admin_borrar_accesorios():
    _id = request.form['txtID']

    # Eliminar imagen de la carpeta
    cursor = conn.cursor()
    cursor.execute("SELECT imagen FROM accesorios WHERE id = %s", (_id,))
    imagen_result = cursor.fetchone()
    conn.commit()

    if imagen_result:
        imagen = imagen_result[0]
        if os.path.exists("app/templates/sitio/temp_img/" + str(imagen)):
            os.unlink("app/templates/sitio/temp_img/" + str(imagen))

    # Eliminar de la base de datos
    cursor = conn.cursor()
    cursor.execute("DELETE FROM accesorios WHERE id = %s", (_id,))
    conn.commit()

    return redirect('/admin/acesorios')

@app.route('/admin/borrar_mascotas', methods=['POST'])
def admin_borrar_mascotas():
    _id = request.form['txtID']

    # Eliminar imagen de la carpeta
    cursor = conn.cursor()
    cursor.execute("SELECT imagen FROM mascotas WHERE id = %s", (_id,))
    imagen_result = cursor.fetchone()
    conn.commit()

    if imagen_result:
        imagen = imagen_result[0]
        if os.path.exists("app/templates/sitio/temp_img/" + str(imagen)):
            os.unlink("app/templates/sitio/temp_img/" + str(imagen))

    # Eliminar de la base de datos
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mascotas WHERE id = %s", (_id,))
    conn.commit()

    return redirect('/admin/mascotas')

@app.route('/admin/borrar', methods=['POST'])
def admin_borrar():
    _id = request.form['txtID']

    # Eliminar de la base de datos
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_pass WHERE id = %s", (_id,))
    conn.commit()

    return redirect('/admin')




if __name__ == '__main__':
    app.run(debug=True)