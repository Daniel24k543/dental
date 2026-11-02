# Tu Clínica Dental — guía para subir a Vercel

Sitio estático (sin build). Carpeta raíz del proyecto: esta misma.

## 1. Cambia los datos de ejemplo (OBLIGATORIO antes de publicar)
Todo lo siguiente es de relleno y **debe reemplazarse por datos reales**; si no, Google mostrará información falsa:

| Qué | Dónde |
| --- | --- |
| Dirección, teléfono, WhatsApp (`51999999999`), horarios | `index.html` (reserva, JSON-LD `Dentist`, pie) y las 6 páginas de servicio |
| Coordenadas (`-12.1211, -77.0297`) | JSON-LD `geo` en `index.html` |
| Precios «Desde S/ …» | `index.html` y páginas de servicio |
| Cifras de confianza (12 años, 8,500+, 4.9/5) | sección de portada de `index.html` |
| Opiniones de pacientes | sección Opiniones de `index.html` (usa opiniones reales, con permiso) |

## Personalizar para un cliente (recomendado)
```
python personalizar.py "Clínica Sonrisa Norte" --telefono "+51 987 654 321" --direccion "Av. Primavera 456" --distrito "Surco" --ciudad "Lima" --zonas "Surco, San Borja, La Molina" --dominio https://www.sonrisanorte.pe
```
Solo el nombre es obligatorio. Cambia nombre, teléfono y WhatsApp, dirección, distrito, ciudad, zonas y dominio en todo el sitio
(principal, 6 páginas de servicio, sitemap, robots, datos de Google e imagen para compartir). Se puede repetir las veces que quieras.
Si cambias la ciudad, renombra las carpetas de servicio (`…-lima` → `…-<ciudad>`).
Requiere Python 3 y, para regenerar la imagen para compartir, `pip install pillow`.

Opciones extra:
- `--vendedor "+51 900 000 000"` → **tu** WhatsApp para el botón «Quiero esta página» del demo (los botones de WhatsApp de la clínica usan `--telefono`).
- `--color "#2563eb"` → color principal de toda la página.
- `--quitar-demo` → quita la etiqueta DEMO, el botón «Quiero esta página» y la sección «Así se vería con tu marca», y deja que Google indexe la página. **Úsalo en la versión final del cliente.**

El demo sale con `noindex` a propósito (para que Google no indexe datos de ejemplo). Se levanta con `--quitar-demo`.

**Revisa a mano después:** precios, cifras de la portada, opiniones, coordenadas (`geo` en `index.html`) y horarios.

## 2. Pon tu dominio
```
python configurar-dominio.py https://www.tudominio.com
```
Actualiza canonical, Open Graph, sitemap, robots y datos estructurados.

## 3. Publica
**Opción A — Vercel CLI**
```
npm i -g vercel
vercel          # primera vez: pruebas
vercel --prod   # producción
```
**Opción B — GitHub:** sube la carpeta a un repositorio, impórtalo en vercel.com/new (Framework: *Other*, sin build, directorio de salida vacío).

## 4. Después de publicar
1. Entra a **Google Search Console**, añade tu dominio y envía `https://tudominio.com/sitemap.xml`.
2. Crea y completa tu **Perfil de Negocio de Google** (Google Maps) con los mismos nombre, dirección y teléfono que el sitio. Es lo que más pesa para búsquedas como «dentista en Miraflores».
3. Revisa con PageSpeed Insights y con la prueba de resultados enriquecidos de Google.

## Estructura SEO
- `/` → «Dentista en Miraflores, Lima»
- `/limpieza-dental-lima/`, `/blanqueamiento-dental-lima/`, `/ortodoncia-invisible-lima/`, `/implantes-dentales-lima/`, `/endodoncia-lima/`, `/odontopediatria-lima/` → una página por servicio, con su título, descripción, preguntas y datos estructurados.

## Crédito del modelo 3D
«Maxillary First Molar», © University of Dundee, School of Dentistry, CC BY 4.0. El crédito del pie de página debe mantenerse.
