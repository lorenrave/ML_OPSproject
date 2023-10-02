#  Machine Learning Operations

En este proyecto, asumí el rol de Data Scientist para la plataforma de juegos Steam, donde tuve la oportunidad de contribuir con la mejora de la experiencia de los usuarios.

El objetivo principal de este proyecto fué la creación de un Producto Mínimo Viable (MVP) que pudiera aprender de los usuarios, centrandose en lo esencial y adaptandose a medida que se adquiere conocimiento sobre las necesidades y deseos.


###  Proceso de ETL y Data Engineering:


Dentro de este proyecto, uno de los aspectos fundamentales fué el proceso de Extracción, Transformación y Carga de Datos (ETL), junto con tareas de Ingeniería de Datos.

En este contexto, realicé la extracción de datos de diferentes archivos JSON, y gestioné datos anidados y valores nulos para garantizar que los datos estuvieran en condiciones óptimas para su posterior análisis.

Llevé a cabo transformaciones críticas en los datos para convertirlos en un formato más eficiente y escalable, como la conversión de archivos JSON a formato csv. Además, eliminé columnas de datos irrelevantes que no aportaban valor al análisis.

Feature Engineering

En esta etapa trabajé en generar un análisis de sentimiento de las reseñas de los usuarios utilizando técnicas avanzadas de Procesamiento de Lenguaje Natural (NLP). Este análisis se tradujo en la creación de la columna 'sentiment_analysis'

que tomó valores de '0' para reseñas negativas, '1' para neutrales y '2' para positivas. 


###  Desarrollo API


También realicé la implementación de una API que permitiera acceder a los datos y las recomendaciones.

Utilicé el eficiente framework FastAPI para lograr esta tarea, donde la API proporciona consultas que facilitan la obtención de información valiosa sobre los juegos 

y las recomendaciones resultantes del modelo de machine learning. 

Las funciones para los endpoints que se consumirán en la API, son las siguientes:

def PlayTimeGenre( genero : str ): Debe devolver año con mas horas jugadas para dicho género.
Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}

def UserForGenre( genero : str ): Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}

def UsersRecommend( año : int ): Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

def UsersNotRecommend( año : int ): Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

def sentiment_analysis( año : int ): Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.
Ejemplo de retorno: {Negative = 182, Neutral = 120, Positive = 278}

Aquí el enlace del deploy en render para poder ejecutar dichas consultas:

https://proyect-ml-deploy.onrender.com/docs


###  Análisis Exploratorio de Datos (EDA):


Una vez que los datos estuvieron preparados, realicé un Análisis Exploratorio de Datos (EDA) para comprender a fondo la naturaleza de los juegos en Steam. Algunas de las áreas clave exploradas incluyeron:

-Visualizar cuál es el género más jugado

-Análisis de los precios de los juegos, permitiendo identificar tendencias de precios y entender cómo se ajustan a las preferencias de los usuarios a través de los años.

-La exploración de los géneros de juegos más populares, lo que proporcionó información valiosa sobre las preferencias de los jugadores y ayudó a definir estrategias de recomendación.

-Conocer la cantidad de juegos de un usuario, lo cuál puede influir en sus preferencias y hábitos de juego. Los usuarios con muchas opciones pueden estar más dispuestos a probar nuevos juegos y explorar diferentes géneros.

-Cantidad de juegos que dan sentimientos positivos/neutrales/negativos por año.


### Modelo de Aprendizaje Automático y Sistema de Recomendación (Machine Learning):



También se abordó la tarea de desarrollar un sistema de recomendación que se basa en la relación ítem-ítem. Esto significa que, dado un juego específico como entrada (el "ítem de consulta"), el objetivo 

era recomendar una lista de juegos similares a ese juego en particular. Para lograr esto, se aplicó un enfoque de similitud del coseno, que se basa en la similitud de características entre los juegos.

Datos Utilizados:

Título del Juego: El título del juego proporciona información sobre la temática y el contenido del juego. Dos juegos con títulos similares 

o relacionados podrían ser más atractivos para los mismos usuarios.

Género del Juego: Los géneros de los juegos son una característica importante, ya que los jugadores a menudo tienen preferencias específicas en términos de género.

Precio del Juego: El precio del juego es un factor que influye en la decisión de compra de los usuarios. La similitud de precios puede indicar que los juegos tienen un rango de precio similar y, por lo tanto, pueden 

ser atractivos para los mismos usuarios en función de su presupuesto.

Metodología:

Para construir el modelo de recomendación, se utilizó la métrica de similitud del coseno. Esta métrica mide la similitud entre dos vectores en función del ángulo entre ellos, 

lo que permite calcular cuán parecidos son los juegos en términos de sus características.

Se representaron los juegos como vectores en un espacio multidimensional, donde cada dimensión corresponde a una característica (título, género y precio).

Los juegos con las similitudes más altas se consideraron los más similares y se recomendaron como resultados.





