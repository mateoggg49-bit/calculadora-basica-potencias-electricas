# calculadora-basica-potencias-electricas
Proyecto desarrollado en Python para la determinación, análisis y exportación de resultados para potencia eléctrica en circuitos AC y DC
Este proyecto implementa una calculadora de potencias eléctricas en sistemas monofásicos, permitiendo analizar cargas y fuentes tanto en corriente directa (DC) como en corriente alterna (AC).
El programa está diseñado para estudiantes y profesionales que necesitan evaluar el comportamiento energético de un circuito eléctrico mediante:
- Cálculo de potencias activas, reactivas, aparentes y complejas.
- Visualización de gráficos (triángulo de potencias, potencia instantánea, potencia vs. tiempo).
- Análisis automático de la naturaleza de la carga.
- Exportación de resultados en formato CSV.
- Soporte de unidades en notación científica e ingeniería.
- Manejo de fasores en forma polar, con ángulos en grados.
Las funcionalidades son:
1. Análisis en corriente directa (DC)
- Cálculo de potencia usando:
P = (V)(I)
P = (V**2)/(R)
P = (I**2)/(R)
- Gráfica potencia vs. tiempo.
- Resultados en notación de ingeniería.
2. Análisis en corriente alterna (AC)
- Entrada de voltaje y corriente como fasores en forma polar.
- Cálculo correcto de potencia compleja: S = (V)(I*)
- Obtención de:
Potencia activa 𝑃
Potencia reactiva 𝑄
Potencia aparente S
Factor de potencia
Ángulo de desfase entre voltaje y corriente
- Gráfica del triángulo de potencias.
- Gráfica de potencia instantánea.
3. Exportación de resultados
- Genera un archivo CSV con los resultados.
Parámetros ingresados
Potencias calculadas
Naturaleza de la carga
- Descarga automática en Google Colab.
4. Análisis Automático
El programa detecta automáticamente:
- Si la carga es inductiva, capacitiva o resistiva
- Si el factor de potencia es adecuado
- Si existe desfase significativo
- Interpretación física básica del sistema
5. Estado del proyecto
Este proyecto corresponde a la segunda entrega, donde se implementa:
- Funcionalidad completa para análisis monofásico DC/AC
- Gráficas y exportación
- Notación de ingeniería
- Manejo correcto de fasores
Para la tercera entrega se considerará:
- Análisis trifásico
- Reportes automáticos PDF
- Interfaz gráfica (opcional)
===========================================================================================================
Autor 
Mateo García Caldas
Estudiante de Ingeniería Eléctrica
Universidad Distrital Francisco José de Caldas
=)
