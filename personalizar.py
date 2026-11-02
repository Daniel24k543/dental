"""Personaliza el demo para un cliente en un solo comando.

Ejemplo:
  python personalizar.py "Clínica Sonrisa Norte" --telefono "+51 987 654 321" \\
      --direccion "Av. Primavera 456" --distrito "Surco" --ciudad "Lima" \\
      --dominio https://www.sonrisanorte.pe

Cambia, en todo el sitio (página principal, páginas de servicio, sitemap, robots,
datos estructurados para Google y la imagen para compartir):
  nombre, teléfono / WhatsApp, dirección, distrito, ciudad y dominio.

Solo es obligatorio el nombre; lo que no indiques se deja como está.
Se puede ejecutar varias veces: recuerda los últimos valores en personalizar.config.json.
Si cambias la ciudad, también renombra las carpetas de servicio (…-lima → …-<ciudad>).

Lo que NO cambia solo (revísalo a mano): precios, cifras de la portada (años, pacientes,
valoración), opiniones, coordenadas del mapa (`geo` en index.html) y horarios.
"""
import argparse, json, os, re, shutil, sys, unicodedata
from urllib.parse import quote, quote_plus
from pathlib import Path

RAIZ = Path(__file__).parent
CFG = RAIZ / "personalizar.config.json"
DEFECTO = {"nombre": "Tu Clínica Dental", "telefono": "+51 999 999 999", "digitos": "51999999999",
           "direccion": "Av. Ejemplo 123", "distrito": "Miraflores", "ciudad": "Lima",
           "dominio": "https://dent-sage.vercel.app", "vendedor": "51000000000", "color": "#14b8a6",
           "zonas": ["Miraflores", "San Isidro", "Surquillo", "Barranco", "San Borja", "Santiago de Surco", "Jesús María", "Magdalena"]}


def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def archivos_sitio():
    pats = ["index.html", "404.html", "sitemap.xml", "robots.txt"]
    out = [RAIZ / p for p in pats if (RAIZ / p).exists()]
    out += [p for p in RAIZ.glob("*/index.html")]
    return out


def reemplazar_todo(pares):
    n = 0
    for f in archivos_sitio():
        t0 = f.read_text(encoding="utf8")
        t = t0
        for a, b in pares:
            if a and a != b:
                t = t.replace(a, b)
        if t != t0:
            f.write_text(t, encoding="utf8", newline="\n"); n += 1
    return n


def hacer_og(nombre, distrito, ciudad):
    base = RAIZ / "assets" / "og-base.png"
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("  (aviso) Instala Pillow para regenerar og-image.png:  pip install pillow")
        return
    if not base.exists():
        print("  (aviso) Falta assets/og-base.png; no se regeneró og-image.png")
        return
    im = Image.open(base).convert("RGB")
    d = ImageDraw.Draw(im)

    def fuente(nombres, tam):
        for n in nombres:
            for carpeta in ("C:/Windows/Fonts/", "/usr/share/fonts/truetype/dejavu/", "/Library/Fonts/"):
                if os.path.exists(carpeta + n):
                    return ImageFont.truetype(carpeta + n, tam)
        return ImageFont.load_default()

    serif_b = fuente(["georgiab.ttf", "DejaVuSerif-Bold.ttf", "Georgia Bold.ttf"], 66)
    serif_i = fuente(["georgiai.ttf", "DejaVuSerif-Italic.ttf", "Georgia Italic.ttf"], 66)
    sans_b = fuente(["segoeuib.ttf", "DejaVuSans-Bold.ttf", "Arial Bold.ttf"], 26)
    sans = fuente(["segoeui.ttf", "DejaVuSans.ttf", "Arial.ttf"], 30)
    logo = fuente(["georgiab.ttf", "DejaVuSerif-Bold.ttf", "Georgia Bold.ttf"], 34)
    ink, teal = (14, 34, 48), (11, 143, 129)
    d.rounded_rectangle((70, 70, 118, 118), radius=14, fill=(20, 184, 166))
    d.text((134, 76), nombre, font=logo, fill=ink)
    d.text((70, 190), "Tu sonrisa,", font=serif_b, fill=ink)
    d.text((70, 275), "vista en 3D", font=serif_i, fill=teal)
    d.text((70, 360), "antes de empezar.", font=serif_b, fill=ink)
    d.text((70, 510), f"Clínica odontológica en {distrito}, {ciudad}", font=sans_b, fill=teal)
    d.text((70, 550), "Diagnóstico digital · Implantes · Ortodoncia invisible", font=sans, fill=(82, 103, 122))
    im.save(RAIZ / "og-image.png", optimize=True)


def main():
    ap = argparse.ArgumentParser(description="Personaliza el demo para un cliente.")
    ap.add_argument("nombre", help='Nombre de la clínica, p. ej. "Clínica Sonrisa Norte"')
    ap.add_argument("--telefono", help='Teléfono/WhatsApp, p. ej. "+51 987 654 321"')
    ap.add_argument("--direccion", help='Calle y número, p. ej. "Av. Primavera 456"')
    ap.add_argument("--distrito", help="Distrito principal, p. ej. Surco")
    ap.add_argument("--ciudad", help="Ciudad, p. ej. Lima")
    ap.add_argument("--zonas", help='Distritos o zonas que atiendes, separados por coma, p. ej. "Cayma, Yanahuara, Cerro Colorado"')
    ap.add_argument("--vendedor", help='Tu WhatsApp para el botón "Quiero esta página" del demo, p. ej. "+51 900 000 000"')
    ap.add_argument("--color", help="Color principal en hex, p. ej. #2563eb")
    ap.add_argument("--quitar-demo", action="store_true", help="Quita la etiqueta DEMO, el botón Quiero esta página y la sección Así se vería, y permite que Google indexe la página")
    ap.add_argument("--dominio", help="Dirección final, p. ej. https://www.sonrisanorte.pe")
    a = ap.parse_args()

    cfg = dict(DEFECTO)
    if CFG.exists():
        cfg.update(json.loads(CFG.read_text(encoding="utf8")))
    nuevo = dict(cfg)
    nuevo["nombre"] = a.nombre.strip()
    if a.telefono:
        dig = re.sub(r"\D", "", a.telefono)
        if len(dig) == 9:
            dig = "51" + dig                      # número peruano sin código de país
        nuevo["telefono"], nuevo["digitos"] = a.telefono.strip(), dig
    if a.direccion: nuevo["direccion"] = a.direccion.strip()
    if a.distrito: nuevo["distrito"] = a.distrito.strip()
    if a.ciudad: nuevo["ciudad"] = a.ciudad.strip()
    if a.zonas: nuevo["zonas"] = [z.strip() for z in a.zonas.split(",") if z.strip()]
    if a.vendedor:
        v = re.sub(r"\D", "", a.vendedor)
        nuevo["vendedor"] = ("51" + v) if len(v) == 9 else v
    if a.color:
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", a.color): sys.exit("El color debe ser hex de 6 dígitos, p. ej. #2563eb")
        nuevo["color"] = a.color.lower()
    if a.dominio: nuevo["dominio"] = a.dominio.strip().rstrip("/")

    # 1) renombrar carpetas de servicio si cambia la ciudad (…-lima → …-<ciudad>)
    s_old, s_new = slug(cfg["ciudad"]), slug(nuevo["ciudad"])
    pares_slug = []
    if s_old != s_new:
        for carpeta in sorted(RAIZ.glob(f"*-{s_old}")):
            if carpeta.is_dir():
                nom_old, nom_new = carpeta.name, carpeta.name[: -len(s_old)] + s_new
                carpeta.rename(RAIZ / nom_new)
                pares_slug.append((nom_old, nom_new))

    # 2) pares de reemplazo (los más largos primero para no pisar)
    def frase(z):                         # "A, B, C y D"
        z = z[:4]
        return z[0] if len(z) == 1 else ", ".join(z[:-1]) + " y " + z[-1]
    def cercanas(z, dist):                # zonas cercanas distintas al distrito principal
        return [x for x in z if x != dist][:4] or z[:1]
    jz = lambda z: ", ".join('{"@type": "AdministrativeArea", "name": "%s"}' % x for x in z)
    pares = []
    pares += pares_slug
    if cfg["zonas"] != nuevo["zonas"]:
        pares += [(jz(cfg["zonas"]), jz(nuevo["zonas"])),
                  ("".join(f"<li>{x}</li>" for x in cfg["zonas"]), "".join(f"<li>{x}</li>" for x in nuevo["zonas"])),
                  (", ".join(cfg["zonas"]), ", ".join(nuevo["zonas"])),
                  (frase(cercanas(cfg["zonas"], cfg["distrito"])), frase(cercanas(nuevo["zonas"], nuevo["distrito"])))]
    pares += [("+" + cfg["digitos"], "+" + nuevo["digitos"]), ("wa.me/" + cfg["digitos"], "wa.me/" + nuevo["digitos"]),
              (cfg["telefono"], nuevo["telefono"]), (cfg["digitos"], nuevo["digitos"])]
    pares += [(cfg["dominio"], nuevo["dominio"]), (cfg["direccion"], nuevo["direccion"]),
              (cfg["nombre"], nuevo["nombre"]),
              (f'{nuevo["direccion"]}, {cfg["distrito"]}', f'{nuevo["direccion"]}, {nuevo["distrito"]}'),
              (f'{nuevo["direccion"]}, {nuevo["distrito"]}, {cfg["ciudad"]}', f'{nuevo["direccion"]}, {nuevo["distrito"]}, {nuevo["ciudad"]}'),
              (f'toda {cfg["ciudad"]}', f'toda {nuevo["ciudad"]}'),
              (f'>{cfg["ciudad"]}, Perú<', f'>{nuevo["ciudad"]}, Perú<')]
    pares += [(f'{cfg["distrito"]}, {cfg["ciudad"]}', f'{nuevo["distrito"]}, {nuevo["ciudad"]}'),
              (f'en {cfg["distrito"]}', f'en {nuevo["distrito"]}'),
              (f'"addressLocality": "{cfg["distrito"]}"', f'"addressLocality": "{nuevo["distrito"]}"'),
              (f'"addressRegion": "{cfg["ciudad"]}"', f'"addressRegion": "{nuevo["ciudad"]}"'),
              (f'"name": "{cfg["ciudad"]}"', f'"name": "{nuevo["ciudad"]}"'),
              (f'en {cfg["ciudad"]}', f'en {nuevo["ciudad"]}'),
              (f'de {cfg["ciudad"]}', f'de {nuevo["ciudad"]}')]
    pares += [("wa.me/" + cfg["vendedor"], "wa.me/" + nuevo["vendedor"])]
    for k in ("nombre", "direccion", "distrito", "ciudad"):
        if cfg[k] != nuevo[k]:
            pares += [(quote_plus(cfg[k]), quote_plus(nuevo[k])), (quote(cfg[k]), quote(nuevo[k]))]
    n = reemplazar_todo(pares)
    if nuevo["color"] != cfg["color"]:
        lum = lambda h: 0.299 * int(h[1:3], 16) + 0.587 * int(h[3:5], 16) + 0.114 * int(h[5:7], 16)
        texto = "#032a26" if lum(nuevo["color"]) > 150 else "#ffffff"
        for f in (RAIZ / "index.html", RAIZ / "assets" / "servicio.css"):
            if f.exists():
                x = f.read_text(encoding="utf8")
                x = x.replace("--teal:" + cfg["color"] + ";", "--teal:" + nuevo["color"] + ";")
                x = re.sub(r"(--on-teal:)#[0-9a-fA-F]{6}", r"\g<1>" + texto, x)
                f.write_text(x, encoding="utf8", newline="\n")
    if a.quitar_demo:
        for f in archivos_sitio():
            x = f.read_text(encoding="utf8")
            x2 = re.sub(r"[ \t]*<!-- DEMO:INICIO -->.*?<!-- DEMO:FIN -->\n?", "", x, flags=re.S)
            x2 = x2.replace('<meta name="robots" content="noindex,follow">', '<meta name="robots" content="index,follow,max-image-preview:large">')
            if x2 != x:
                f.write_text(x2, encoding="utf8", newline="\n")
        print("  Demo quitado: la página ya es indexable por Google.")
    hacer_og(nuevo["nombre"], nuevo["distrito"], nuevo["ciudad"])
    CFG.write_text(json.dumps(nuevo, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    print(f"Listo: {n} archivos actualizados para «{nuevo['nombre']}».")
    print("Revisa a mano: precios, cifras de la portada, opiniones, coordenadas (geo) y horarios.")
    print("Luego sube los cambios a Git/Vercel.")


if __name__ == "__main__":
    main()
