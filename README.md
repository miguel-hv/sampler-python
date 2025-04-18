# SAMPLER

Clon en python del sampler PO KO de teenage engineering con UI optimizada para ordenador. Vibe coding con chatgpt. 
Es un proyecto de prueba/exploración para ver hasta dónde puedo llegar solo con el concepto del diseño y la ui sin saber programar las librerías de python.

## Concepto
Diseñar un sampler inspirado en el PO KO y el sp404 para usar en el ordenador desde el teclado (sin ratón). Quiero conseguir un sampler minimalista donde pueda coger sonidos y tirarlos a un secuenciador para hacer beats por diversión. Está enfocado a jugar y esbozar ideas rápidamente, no a ser una herramienta musical completa.

Se van a imponer muchas restricciones en el flujo de creación y las posibilidades sónicas a fin de tener una aplicación sencilla.  

## por hacer

- cargar samples desde el pad directamente
- solo un slider para los volúmenes: cada pad tiene el suyo y lo muestra bajo el nombre del sample (para distintos volúmenes en el secuenciador clonar samples)
- botón "pattern" para organizar los patrones sobre la rejilla de pads
- copiar sonidos de un pad a otro y borrar
- copiar/borrar para patrones
- asignar teclas como atajo de teclado a cada botón
- setear volúmenes con las teclas de rejilla z-v/1-4
- ¿meter como teclas de acción la rejilla z-v/1-4 y una simétrica b-,/5-8? O solo la primera rejilla y una tecla extra "command" para x2
- ¿samplear desde el sonido del ordenador? (ya lo hace la extensión de chrome Sample)
- trim y pitch samples
- efectos: filtro, delay, reverse (scratch),
- ¿guardar y cargar proyecto? o quizá solo grabar salida audio

## Limitaciones

Está por ver si se implementan:

- dejar audio en lofi: The LIVEN Lofi-12 has a 16bit - 12kHz/24kHz sampling engine with the 12bit Sampler mode that will turn any sound into a pleasing lo-fi sound
- solo sonido mono
- 8 bancos de sonido 
- solo 9 sonidos a la vez en el secuenciador
- tiempo máximo de sample ¿5s? (determinar)