### Pagina_web_DB_

**Creacion del entorno virtual en vscode**
1.- abra una terminal y ejecute el siguiente comando:

`$ pip install virtualenv`

2.- dirígase a la carpeta en la cual desea el entorno virtual(desde la terminal)
3.- ejecute el siguiente comando:

`$virtualenv -p python3 env`

**Inicie su entorno virtual**
1.- ejecute 
`$ .\env\Scripts\activate`

**Si ocurre un error al iniciar el entorno virtual ejecute lo siguiente**
`$ Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

**instalacion de librerias a travez de requeriments.txt**
IMPORTANTE: tener la carpeta app y el archivo requeriments en el mismo sitio en el que se encuentra la carpeta env. Quedando

[![example.png](https://i.postimg.cc/3x65gP8N/example.png)](https://postimg.cc/tshMbvVG)

`$ pip install -r .\requeriments.txt`

**EJECUTAR LA PAGINA WEB**
IMPORTANTE: Tener activado el entorno virtual 
`$ .\env\Scripts\activate`

Ejecutar el siguiente comando para iniciar el servidor
`$ python .\app\app.py`

Ir a la ruta que aparece en la terminal
[![Example01.png](https://i.postimg.cc/9MsYbY4G/Example01.png)](https://postimg.cc/7GMzY7n6)

**SALIR DEL ENTORNO VIRTUAL**
Ejecute:
`$ deactivate`


para el login como administrador reconoce: admin@gmail.com      pass:admin
el resto de usuarios solo podran acceder a la vista de compras, mientras que el administrador maneja la base de datos
