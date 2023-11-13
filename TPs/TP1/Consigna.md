### Requerimientos
Escriba un programa que abra un archvo de texto pasado por argumento utilizando el modificador -f.
* El programa deberá generar tantos procesos hijos como líneas tenga el archivo de texto.
* El programa deberá enviarle, vía pipes (os.pipe()), cada línea del archivo a un hijo.
* Cada hijo deberá invertir el orden de las letras de la línea recibida, y se lo enviará al proceso padre nuevamente, también usando os.pipe().
* El proceso padre deberá esperar a que terminen todos los hijos, y mostrará por pantalla las líneas invertidas que recibió por pipe.
* Debe manejar los errores.
​
​
#### Ejemplo modo de uso
​
~~~~~~~~~~~~~~~~~~~
Contenido del archivo /tmp/texto.txt
​
Hola Mundo
que tal
este es un archivo
de ejemplo
​
#### Ejecución:
python3 inversor.py -f /tmp/texto.txt
odnuM aloH
lat euq
ovihcra nu se etse
olpmeje ed
​
~~~~~~~~~~~~~~~~~~~
​
​
### Objetivos
​
* Manejo de archivos 
* Creación de procesos.
* Uso de mecanismos de IPC.
​
​
### Bonus Track
Realizar la misma aplicación con ayuda del módulo multiprocessing 