# Documentación de Uso

## Requisitos Previos

Antes de ejecutar los servidores y el cliente, asegúrate de tener las siguientes bibliotecas instaladas:

```bash
pip install Pillow
```

## Servidor Principal (`main_server.py`)

El servidor principal recibe imágenes en formato JPEG, las convierte a escala de grises y las envía al servidor de escalado. A continuación se detalla cómo ejecutar el servidor principal:

```bash
python3 main_server.py -i localhost -p 5050
```

- `-i` o `--ip`: La dirección IP en la que el servidor principal escuchará las solicitudes.
- `-p` o `--puerto`: El puerto en el que el servidor principal escuchará las solicitudes.

## Servidor de Escalado (`scaling_server.py`)

El servidor de escalado recibe las imágenes en escala de grises del servidor principal, las escala según el factor proporcionado y las envía de vuelta al servidor principal. A continuación se detalla cómo ejecutar el servidor de escalado:

```bash
python3 scaling_server.py -i localhost -p 5051 -s 0.5
```

- `-i` o `--ip`: La dirección IP en la que el servidor de escalado escuchará las solicitudes.
- `-p` o `--puerto`: El puerto en el que el servidor de escalado escuchará las solicitudes.
- `-s` o `--escala`: El factor de escala que se aplicará a las imágenes recibidas.

## Cliente (Enviar Imágenes al Servidor Principal)

Para enviar una imagen al servidor principal, puedes usar el comando `curl`. Asegúrate de tener una imagen en formato JPEG (por ejemplo, `image.jpg`). Ejecuta el siguiente comando:

```bash
curl -X POST -H "Content-Type: image/jpeg" --data-binary @image.jpg http://localhost:5050
```

Este comando utiliza `curl` para realizar una solicitud POST al servidor principal (`http://localhost:5050`) con la imagen en formato JPEG.

**Nota:** Asegúrate de tener permisos para ejecutar estos comandos y de tener una imagen llamada `image.jpg` en el mismo directorio.

Con estos pasos, deberías poder ejecutar los servidores y enviar imágenes al servidor principal para su procesamiento y escala.