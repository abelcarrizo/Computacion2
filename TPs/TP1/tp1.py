#Abel Carrizo
import os
import argparse
import time

def transform_line(line):
    """Transforma una línea invirtiéndola y concatenándola con la original."""
    return line + "   |   " + line[::-1] + "\n"

def transform_text(lines):
    """Transforma todas las líneas del texto."""
    child_read, parent_write = os.pipe()
    parent_read, child_write = os.pipe()

    line_lengths = [len(line.encode()) for line in lines]

    for line in lines:
        os.write(parent_write, line.encode())

    for length in line_lengths:
        rt = os.fork()
        if rt > 0:
            time.sleep(0.5)
            continue
        if rt == 0:
            line = os.read(child_read, length - 1).decode()
            os.read(child_read, 1)
            transformed_line = transform_line(line)
            os.write(child_write, transformed_line.encode())
            exit()

    for x in range(len(lines)):
        os.wait()

    result_line = os.read(parent_read, 2024).decode()
    print(result_line)

    os.close(child_read)
    os.close(child_write)
    os.close(parent_read)
    os.close(parent_write)

def main():
    """Función principal que gestiona el flujo del programa."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help="ruta al archivo para ser invertido y espejado", type=str, required=True)
    args = parser.parse_args()

    if not args.f:
        print("Debe especificar un archivo de texto con el argumento -f")
        exit(1)

    if not os.access(args.f, os.R_OK):
        print(f"No se puede acceder al archivo {args.f}")
        exit(1)

    try:
        with open(args.f, "r") as original_file:
            lines = original_file.readlines()
    except (PermissionError, IOError) as e:
        print(f"Error al abrir el archivo: {e}")
        exit(1)

    transform_text(lines)

if __name__ == "__main__":
    main()
