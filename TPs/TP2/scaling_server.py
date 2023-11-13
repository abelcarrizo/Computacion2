import argparse
import socket
from PIL import Image
from io import BytesIO
import threading

def escalar_imagen(imagen, factor_escala):
    nueva_dimension = tuple(int(dim * factor_escala) for dim in imagen.size)
    imagen_escalada = imagen.resize(nueva_dimension, Image.ANTIALIAS)
    return imagen_escalada

def manejar_cliente_escalado(socket_cliente, factor_escala):
    try:
        # Recibe la longitud de los datos primero
        longitud_datos = int.from_bytes(socket_cliente.recv(4), byteorder='big')

        # Recibe los datos de la imagen
        imagen_bytes = socket_cliente.recv(longitud_datos)

        imagen_pillow = Image.open(BytesIO(imagen_bytes))
        
        # Imprime el mensaje cuando se recibe la imagen del servidor principal en el servidor de escalado
        print(f"Servidor de Escalado: Recibida imagen del servidor principal en el servidor de escalado. Dimensiones: {imagen_pillow.size}")

        # Escala la imagen con Pillow
        imagen_escalada = escalar_imagen(imagen_pillow, factor_escala)

        # Imprimir información sobre la imagen después de la escala
        print(f"Servidor de Escalado: Dimensiones después de escalar: {imagen_escalada.size}")

        # Convierte la imagen escalada a bytes
        with BytesIO() as output:
            imagen_escalada.save(output, format='JPEG')
            imagen_bytes_escalada = output.getvalue()
        
        """
        Verifico si la imagen se almacena correctamente en el server local
        nombre_archivo_escalada = "imagen_escalada  .jpg"
        with open(nombre_archivo_escalada, 'wb') as f:
        f.write(imagen_bytes_escalada)
        """

        # Envia la imagen escalada al servidor principal
        enviar_imagen_escalada(socket_cliente, imagen_bytes_escalada)
    except Exception as e:
        print(f"Error al manejar el cliente de escalado: {e}")
    finally:
        socket_cliente.close()

def enviar_imagen_escalada(sock, imagen_bytes_escalada):
    try:
        # Envia la longitud de los datos primero
        longitud_datos = len(imagen_bytes_escalada)
        sock.sendall(longitud_datos.to_bytes(4, byteorder='big'))

        # Luego envía los datos
        sock.sendall(imagen_bytes_escalada)
        print("Servidor de Escalado: Imagen escalada enviada al servidor principal.")

    except BrokenPipeError:
        print("La conexión fue cerrada por el otro extremo.")
    except Exception as e:
        print(f"Error al enviar la imagen escalada: {e}")
    finally:
        sock.close()

def servidor_escalado(ip, puerto, factor_escala):
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socket_servidor.bind((ip, puerto))
    except socket.error:
        print("Error al vincular el socket.")
        return

    socket_servidor.listen(5)
    print(f"Servidor de Escalado escuchando en {ip}:{puerto}")

    try:
        while True:
            socket_cliente, direccion = socket_servidor.accept()
            print(f"Conexión aceptada desde {direccion[0]}:{direccion[1]}")

            threading.Thread(target=manejar_cliente_escalado, args=(socket_cliente, factor_escala)).start()
    except KeyboardInterrupt:
        print('Servidor de Escalado detenido.')
    finally:
        socket_servidor.close()

def main():
    parser = argparse.ArgumentParser(description='Servidor de Escalado')
    parser.add_argument('-i', '--ip', required=True, help='Dirección de escucha')
    parser.add_argument('-p', '--puerto', type=int, required=True, help='Puerto de escucha')
    parser.add_argument('-s', '--escala', type=float, required=True, help='Factor de escala')
    args = parser.parse_args()

    try:
        servidor_escalado(args.ip, args.puerto, args.escala)
    except KeyboardInterrupt:
        print('Servidor de Escalado detenido.')

if __name__ == '__main__':
    main()
