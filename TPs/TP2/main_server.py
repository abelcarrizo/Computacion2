# Abel Carrizo
import argparse
from http.server import SimpleHTTPRequestHandler, HTTPServer
from io import BytesIO
import socket
from PIL import Image

def procesar_imagen(archivo_entrada, factor_escala):
    try:
        # Leer la imagen desde BytesIO
        imagen_bytes = archivo_entrada.read()
        imagen_pillow = Image.open(BytesIO(imagen_bytes))

        # Mensaje antes de la conversión de la imagen
        print(f"Servidor Principal: Imagen recibida del cliente. Dimensiones originales: {imagen_pillow.size}")

        if imagen_pillow.mode != 'L':
            # Convertir la imagen a escala de grises si no está en modo L (escala de grises)
            imagen_gris = imagen_pillow.convert('L')
        else:
            imagen_gris = imagen_pillow

        # Convertir la imagen en escala de grises a bytes
        with BytesIO() as output:
            imagen_gris.save(output, format='JPEG')
            imagen_procesada = output.getvalue()

        """ 
        Verifico si la imagen se almacena correctamente en el server local
        nombre_archivo = "imagen_gris.jpg"
        with open(nombre_archivo, 'wb') as f:
            f.write(imagen_procesada)
        """
        return imagen_procesada

    except Exception as e:
        print(f"Error al procesar la imagen: {e}")

def enviar_imagen_procesada(sock, imagen_bytes_procesada):
    try:
        # Envia la longitud de los datos primero
        sock.sendall(len(imagen_bytes_procesada).to_bytes(4, byteorder='big'))
        # Luego envía los datos
        sock.sendall(imagen_bytes_procesada)
    except Exception as e:
        print(f"Error al enviar la imagen procesada: {e}")

class ImageHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            imagen_bytes = self.rfile.read(content_length)

            # Procesa la imagen y obtiene la imagen procesada en bytes
            imagen_procesada = procesar_imagen(BytesIO(imagen_bytes), factor_escala=0.5)

            # Imprime mensaje antes de enviar la imagen al servidor de escalado
            print(f"Servidor Principal: Enviando imagen al servidor de escalado...")

            # Envia la imagen procesada al servidor de escalado
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                direccion_escalado = ('localhost', 5051)  # Usar el puerto correcto
                sock.connect(direccion_escalado)
                enviar_imagen_procesada(sock, imagen_procesada)

                # Recibe la imagen escalada en gris del servidor de escalado
                longitud_datos = int.from_bytes(sock.recv(4), byteorder='big')
                imagen_escalada_bytes = sock.recv(longitud_datos)

                # Imprime mensaje después de enviar la imagen al cliente
                print("Servidor Principal: Imagen escalada recibida del servidor de escalado.")

            # Guarda la imagen escalada en el servidor principal
            nombre_archivo_escalada_principal = "imagen_procesada.jpg"
            with open(nombre_archivo_escalada_principal, 'wb') as f:
                f.write(imagen_escalada_bytes)

            # Responde al cliente con la imagen procesada
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            self.wfile.write(imagen_escalada_bytes)

            # Imprime mensaje después de enviar la imagen al cliente
            print("Servidor Principal: Imagen procesada enviada al cliente y guardada localmente.")

        except Exception as e:
            print(f"Error al manejar la solicitud POST: {e}")

def servidor(ip, puerto):
    handler = ImageHandler

    with HTTPServer((ip, puerto), handler) as httpd:
        print(f"Servidor escuchando en {ip}:{puerto}")
        httpd.serve_forever()

def main():
    parser = argparse.ArgumentParser(description='Procesamiento de imágenes')
    parser.add_argument('-i', '--ip', required=True, help='Dirección de escucha')
    parser.add_argument('-p', '--puerto', type=int, required=True, help='Puerto de escucha')
    args = parser.parse_args()

    try:
        servidor(args.ip, args.puerto)
    except KeyboardInterrupt:
        print('Servidor detenido.')

if __name__ == '__main__':
    main()