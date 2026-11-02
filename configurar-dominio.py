"""Reemplaza el dominio de ejemplo por el tuyo en todo el sitio.

Uso:   python configurar-dominio.py https://www.midominio.com
Luego vuelve a subir a Vercel.
"""
import sys, pathlib

VIEJO = "https://dent-sage.vercel.app"
if len(sys.argv) != 2 or not sys.argv[1].startswith("http"):
    sys.exit("Uso: python configurar-dominio.py https://www.midominio.com")
nuevo = sys.argv[1].rstrip("/")
raiz = pathlib.Path(__file__).parent
n = 0
for p in raiz.rglob("*"):
    if p.suffix in {".html", ".xml", ".txt", ".json", ".svg"} and p.is_file():
        t = p.read_text(encoding="utf8")
        if VIEJO in t:
            p.write_text(t.replace(VIEJO, nuevo), encoding="utf8")
            n += 1
print(f"Listo: {n} archivos actualizados a {nuevo}")
