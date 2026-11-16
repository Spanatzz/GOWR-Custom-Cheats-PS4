# Integración real en PS4: pendiente

Este directorio contiene un **núcleo lógico portable**, NO un `.prx` que se pueda instalar.

Para obtener el menú visual dentro del juego hace falta implementar tres piezas:

1. **Pad**: adaptador a `scePadRead`/`scePadReadState`, convertir `ScePadData.buttons` al conjunto `MenuButton` y evitar que L1+Círculo active acciones del juego. Debe respetar los demás plugins y evitar dobles llamadas por frame.
2. **Render**: dibujar una capa superpuesta sobre el framebuffer del juego mediante un backend PS4 específico; no escribir directamente en memoria del juego o asumir offsets de GPU. Hay referencias de frameworks de overlay de PS4, pero no están incorporados aquí ni probados en esta versión.
3. **Trucos**: para activar las entradas desde el menú propio se necesita un motor de aplicación de los Cheatline (secciones, offsets, códigos original/restauración) o una interfaz pública de GoldHEN con esas funciones. No hay tal interfaz pública documentada en los enlaces consultados; por seguridad NO se implementaron escrituras a direcciones arbitrarias.

Si se quiere usar **ya** los trucos en PS4: el archivo `.shn` generado se puede instalar como cheat GoldHEN. Ese menú se abre con **SHARE mantenido**, no con L1+Círculo. No instalar este núcleo como `.prx`.

Referencias:
- https://github.com/GoldHEN/GoldHEN/blob/master/CHEATMENU.md
- https://github.com/GoldHEN/GoldHEN_Plugins_SDK
- https://github.com/GoldHEN/GoldHEN_Plugins_Repository
- https://github.com/Faultz/odyssey-game (plantilla de overlay, dependencias adicionales)
