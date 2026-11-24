import json
import re
import sys

# Patrones de elementos que deben protegerse.
PATRON_ENV = re.compile(
    r"(?i)(?<![A-Za-z0-9_-])\.env(?:$|[./\\:_-]|\s|[\"'])"
)

PATRON_SCRIPT = re.compile(
    r"(?i)(?<![A-Za-z0-9_-])verificar_entorno\.py(?![A-Za-z0-9_-])"
)

# Campos de tool_input que pueden contener rutas o comandos.
CAMPOS_RELEVANTES = {
    "file_path",
    "path",
    "notebook_path",
    "filename",
    "target_file",
    "command",
    "cmd",
    "script",
    "powershell",
    "bash",
}


def buscar_cadenas(objeto, nombre_campo=""):
    """Recorre los campos relevantes, incluidos los objetos anidados."""
    encontrados = []

    if isinstance(objeto, dict):
        for clave, valor in objeto.items():
            if clave.lower() in CAMPOS_RELEVANTES:
                encontrados.extend(buscar_cadenas(valor, clave))
            elif isinstance(valor, (dict, list)):
                encontrados.extend(buscar_cadenas(valor, clave))

    elif isinstance(objeto, list):
        for elemento in objeto:
            encontrados.extend(buscar_cadenas(elemento, nombre_campo))

    elif isinstance(objeto, str) and nombre_campo.lower() in CAMPOS_RELEVANTES:
        encontrados.append(objeto)

    return encontrados


def main():
    try:
        evento = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError):
        print("Bloqueado: evento JSON inválido.", file=sys.stderr)
        return 2

    datos = evento.get("tool_input", {})
    cadenas = buscar_cadenas(datos)

    for contenido in cadenas:
        if PATRON_ENV.search(contenido):
            print(
                "Bloqueado: operación sobre el archivo .env.",
                file=sys.stderr
            )
            return 2

        if PATRON_SCRIPT.search(contenido):
            print(
                "Bloqueado: ejecución o acceso a verificar_entorno.py.",
                file=sys.stderr
            )
            return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
