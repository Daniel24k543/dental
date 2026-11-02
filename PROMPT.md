# PROMPT — Sitio 3D interactivo para clínica odontológica

Construye UN solo archivo `index.html` (HTML + CSS + JS inline) para **Alba Dental**, una clínica odontológica de Lima. Debe ser una experiencia 3D con scroll narrativo, no una plantilla genérica.

====================================================================
1. RECURSOS
====================================================================
- Three.js 0.160 (importmap, jsdelivr) + GLTFLoader + DRACOLoader + DecalGeometry + RoomEnvironment.
- GSAP 3.12 + ScrollTrigger (cdnjs).
- Modelo real: `modelo/diente.glb` (molar, University of Dundee, CC BY 4.0). Mostrar el crédito en el pie.
- Un solo `<canvas>` fijo detrás del contenido. El diente se mueve entre secciones; nunca varios canvas.
- Prohibido usar emojis: todos los iconos son SVG inline de trazo (`currentColor`).

====================================================================
2. DIRECCIÓN VISUAL
====================================================================
- Paleta: porcelana `#f4f1ea`, tinta `#0e2230`, turquesa `#14b8a6`, coral de aviso `#ff6b57`. Una sección oscura (`#0b1a24`) para la tecnología.
- Tipografía: Fraunces (títulos, con palabras en cursiva de acento) + Manrope (texto).
- Mucho aire, títulos grandes, una sola idea por pantalla. Cero degradados morados genéricos.

====================================================================
3. SECCIONES (en orden)
====================================================================
1. HERO — titular "Tu sonrisa, vista en 3D antes de empezar", 2 CTA, 3 cifras de confianza. Diente grande a la derecha, girable con arrastre (inercia) y con parallax suave del mouse.
2. TECNOLOGÍA (sección fija con scroll de 3 pasos, fondo oscuro):
   a) Escaneo: un plano de luz recorre el diente y deja una malla (wireframe) detrás.
   b) Diagnóstico: vista de rayos X (diente translúcido, pulpa y conductos brillando).
   c) Plan: el diente luce impecable con destellos.
3. ANATOMÍA — puntos sobre el diente (esmalte, dentina, pulpa, raíz), panel lateral, interruptor "Rayos X". Tocar el diente identifica la zona.
4. SIMULADOR — sliders de caries, manchas y desalineación + casilla de raíz comprometida. Un motor de reglas arma el plan (tratamiento, sesiones, precio en S/ y total). "Aplicar tratamiento" ejecuta cada paso sobre el diente: la caries se cierra, el color se aclara, el diente se alinea con aparato, o se coloca un implante. La caries es un decal pegado a la superficie y se coloca tocando el diente. La desalineación muestra dos dientes vecinos y una línea guía del arco.
5. SERVICIOS — 6 tarjetas con icono SVG.
6. OPINIONES — 3 testimonios.
7. PREGUNTAS FRECUENTES — acordeón.
8. RESERVA — formulario (nombre, teléfono, servicio, fecha, hora) que abre WhatsApp con el mensaje armado + horario y dirección.

====================================================================
4. COMPORTAMIENTO 3D
====================================================================
- Cada sección declara posición/escala/rotación del diente (`data-x`, `data-s`, `data-ry`); el diente llega con amortiguación exponencial (`1-exp(-k·dt)`), nunca con saltos.
- En secciones sin 3D el diente se oculta (escala → 0, `visible=false`).
- El estado del simulador solo se ve dentro de su sección.
- Móvil: diente centrado arriba y reducido; texto abajo.
- `pixelRatio` máx. 1.75, pausar el loop con la pestaña oculta.

====================================================================
5. MOVIMIENTO (reglas de las skills)
====================================================================
- Easing de salida fuerte `cubic-bezier(.23,1,.32,1)`. Nada de `ease-in` ni `transition: all`.
- UI < 300 ms; solo `transform` y `opacity`. Entradas con `opacity:0 + translateY(14px)`, nunca desde `scale(0)`.
- Escalonado de 40–80 ms entre elementos que entran juntos.
- Botones: `:active { transform: scale(.97) }`. Hover solo dentro de `@media (hover:hover) and (pointer:fine)`.
- `prefers-reduced-motion`: sin giro automático ni pin; contenido visible y estático.
- Foco visible en todo lo interactivo; contraste AA.

====================================================================
6. ENTREGA
====================================================================
- Pantalla de carga mientras cargan fuentes y modelo; mensaje claro si falta el `.glb`.
- Funciona vía servidor local (`iniciar.bat`).
- Verificar en escritorio y en 390 px de ancho; sin errores en consola.
