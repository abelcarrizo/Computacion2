import argparse
import os
import threading
import socket
import cv2
from queue import Queue

def procesar_imagen(archivo_entrada, archivo_salida, factor_escala):
    imagen = cv2.imread(archivo_entrada, cv2.IMREAD_COLOR)
    imagen_reducida = cv2.resize(imagen, (0, 0), fx=factor_escala, fy=factor_escala)
    cv2.imwrite(archivo_salida, imagen_reducida)

def manejar_cliente(socket_cliente, archivo_imagen, cola_respuestas, factor_escala, desde_servicio_reduccion=False):
    archivo_salida = 'reducida_' + archivo_imagen
    procesar_imagen(archivo_imagen, archivo_salida, factor_escala)

    with open(archivo_salida, 'rb') as f:
        imagen_procesada = f.read()

    cola_respuestas.put(imagen_procesada)

    if not desde_servicio_reduccion:
        socket_cliente.close()

def servicio_reduccion(cola_trabajo, cola_respuestas, factor_escala):
    while True:
        archivo_imagen = cola_trabajo.get()
        manejar_cliente(None, archivo_imagen, cola_respuestas, factor_escala, desde_servicio_reduccion=True)

def servidor(ip, puerto, archivo_imagen, factor_escala):
    cola_trabajo = Queue()
    cola_respuestas = Queue()

    # Iniciar el servidor de reducción
    hilo_reduccion = threading.Thread(target=servicio_reduccion, args=(cola_trabajo, cola_respuestas, factor_escala))
    hilo_reduccion.start()

    socket_servidor = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    try:
        socket_servidor.bind((ip, puerto))
    except socket.error:
        socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_servidor.bind((ip, puerto))

    socket_servidor.listen(5)
    print(f"Escuchando en {ip}:{puerto}")

    while True:
        socket_cliente, direccion = socket_servidor.accept()
        print(f"Conexión aceptada desde {direccion[0]}:{direccion[1]}")

        archivo_imagen_cliente = archivo_imagen  # Puedes cambiar esto según cómo recibas el nombre del archivo del cliente
        cola_trabajo.put(archivo_imagen_cliente)

        imagen_procesada = cola_respuestas.get()
        socket_cliente.sendall(imagen_procesada)

    socket_servidor.close()

def main():
    parser = argparse.ArgumentParser(description='Procesamiento de imágenes')
    parser.add_argument('-i', '--ip', required=True, help='Dirección de escucha')
    parser.add_argument('-p', '--puerto', type=int, required=True, help='Puerto de escucha')
    parser.add_argument('-f', '--archivo', required=True, help='Nombre del archivo de imagen a procesar')
    parser.add_argument('-s', '--escala', type=float, required=True, help='Factor de escala para reducción de imagen')
    args = parser.parse_args()

    try:
        servidor(args.ip, args.puerto, args.archivo, args.escala)
    except KeyboardInterrupt:
        print('Servidor detenido.')

if __name__ == '__main__':
    main()
