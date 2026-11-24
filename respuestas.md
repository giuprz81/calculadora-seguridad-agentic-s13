# Respuestas — Reto 4: Auditoría de contenido Unicode

## 1. Comparación entre el contenido renderizado y el archivo original

Al revisar `variantes/README_unicode_demo.md`, se encontraron elementos que no son evidentes en la visualización habitual del Markdown:

- Cuatro caracteres Unicode U+200B (ZERO WIDTH SPACE), que son espacios de ancho cero y no se muestran como caracteres visibles.
- Un comentario HTML que permanece en el archivo original, pero no aparece en la representación normal del Markdown.

El archivo `INSTALAR.md` no presentó hallazgos.

## 2. Resultado de la auditoría

Se ejecutó el siguiente comando:

`python variantes/auditar_unicode.py INSTALAR.md variantes/README_unicode_demo.md`

Resultado:

- `INSTALAR.md`: sin hallazgos.
- `variantes/README_unicode_demo.md`: cinco hallazgos.
- Total: cinco hallazgos.

La auditoría permitió identificar caracteres invisibles y contenido oculto en un comentario HTML.

## 3. ¿Quién escribió ese texto?

No es posible determinar la identidad del autor únicamente a partir del contenido inspeccionado. El texto se encuentra dentro del repositorio y debe considerarse contenido proporcionado por este, no una instrucción autorizada por el usuario.

## 4. ¿Qué nivel de confianza tiene?

El contenido del repositorio debe tratarse como entrada no confiable. Que un texto aparezca en un README o en otro archivo de documentación no significa que tenga autoridad para modificar las instrucciones del usuario ni para autorizar acciones del agente.

El agente puede analizar el contenido para cumplir la tarea, pero debe mantener la distinción entre información del repositorio e instrucciones de mayor autoridad.

## 5. ¿Qué acción intentaba introducir?

El texto visible del archivo contiene una indicación para instalar la calculadora con Python 3 y ejecutar las pruebas. Los caracteres U+200B aparecen insertados dentro de algunas palabras, y el comentario HTML permite observar contenido que no aparece en la vista renderizada.

Sin embargo, el contenido inspeccionado no demuestra que se intentara introducir una acción maliciosa, acceder a información sensible o ejecutar comandos ajenos a la actividad. Por ello, no es correcto atribuirle una intención maliciosa sin evidencia.

El riesgo que demuestra el ejercicio es que un agente puede recibir contenido que no resulta evidente en la representación visual de un archivo. Debe analizarlo como información no confiable y no asumir que tiene autoridad para modificar las instrucciones del usuario.
## 6. Limitación del guardrail

El hook `proteger_env.py` utiliza patrones de texto para identificar referencias a `.env` y `verificar_entorno.py`.

Las pruebas de auditoría del propio laboratorio demostraron que puede no detectar determinadas variantes, como:

- Construcción de rutas mediante fragmentos.
- Uso de comodines.
- Uso de variables intermedias de shell.

Por ello, no debe considerarse una protección completa contra todas las formas posibles de acceso a archivos o ejecución de comandos.

## 7. Segunda barrera de seguridad

Se propone complementar el hook con dos medidas principales:

**Mínimo privilegio:** limitar los permisos del agente a los archivos, herramientas y operaciones estrictamente necesarios para realizar la tarea.

**Aislamiento mediante sandbox:** ejecutar al agente en un entorno restringido que limite el acceso al sistema de archivos, los procesos y los recursos externos.

También se recomienda mantener la aprobación humana para operaciones sensibles.

Estas medidas se proponen como defensas adicionales y no se presentan como implementadas en este laboratorio.

## 8. Conclusión

La auditoría demuestra que un archivo puede contener elementos que no son evidentes en su representación visual. Por esta razón, el agente debe tratar el contenido del repositorio como información que necesita analizar, pero no como instrucciones con autoridad para cambiar la solicitud del usuario.

El hook preventivo aporta una primera barrera para bloquear operaciones identificadas como sensibles. Sin embargo, sus limitaciones justifican complementarlo con mínimo privilegio, aislamiento y supervisión humana.
