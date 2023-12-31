from fastapi import FastAPI
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(debug=True) #debug me muestra en el docs de fast api el error que tira y no solo internal server error

# Carga los datos desde los CSV
steam_games = pd.read_csv('data/df_games_clean.csv')
users_items = pd.read_csv('data/user_items_clean.csv')
users_reviews = pd.read_csv('data/user_reviews_clean.csv')


@app.get('/PlayTimeGenre/{genero}')
def PlayTimeGenre(genero: str):

    # Obtener las primeras 4000 filas de users_items
    users_items_first_2000 = users_items.head(2000)

    # Combinar los DataFrames steam_games y users_items (solo las primeras 4000 filas)
    merged_data = pd.merge(users_items_first_2000, steam_games, on='id', how='inner')

    # Filtrar por género en la columna 'genres'
    df_filtered = merged_data[merged_data['genres'].str.contains(genero, case=False)]
    
    # Verificar si el DataFrame está vacío después del filtro
    if df_filtered.empty:
        return {"Mensaje": f"No se encontraron registros para el género {genero}"}
    
    # Agrupar por 'posted year' y sumar las horas jugadas
    df_grouped = df_filtered.groupby(pd.to_datetime(df_filtered['year'], format='%Y').dt.year)['playtime_forever'].sum()
    
    # Verificar si la Serie está vacía después de la agregación
    if df_grouped.empty:
        return {"Mensaje": f"No se encontraron registros para el género {genero} en años específicos"}
    
    # Encontrar el año con más horas jugadas
    max_year = df_grouped.idxmax()
    
    return {"Año de lanzamiento con más horas jugadas para " + genero: int(max_year)}



@app.get('/UserForGenre/{genero}')
def UserForGenre(genero: str):
    # Obtener las primeras 2000 filas de users_items
    users_items_first_2000 = users_items.head(2000)

    # Realizar el merge de users_items y steam_games en base a user_id
    merged_data = pd.merge(users_items_first_2000, steam_games, on='id', how='inner')

    # Filtrar los juegos por el género dado
    genero_df = merged_data[merged_data['genres'].str.contains(genero, case=False)]

    if genero_df.empty:
        return {"Mensaje": f"No se encontraron juegos para el género {genero}"}

    # Obtener el usuario con más horas jugadas para el género
    usuario_mas_horas = genero_df.loc[genero_df['playtime_forever'].idxmax(), 'user_id']

    # Calcular la acumulación de horas jugadas por año
    horas_por_anio = genero_df.groupby('year')['playtime_forever'].sum().reset_index()
    acumulacion_horas = [{"Año": int(row['year']), "Horas": int(row['playtime_forever'])} for _, row in horas_por_anio.iterrows()]

    # Crear el diccionario de respuesta formateado
    respuesta = {
        "Usuario con más horas jugadas para " + genero: usuario_mas_horas,
        "Horas jugadas": acumulacion_horas
    }

    return respuesta



   



@app.get('/users_recommend/{anio}')
def users_recommend(anio: int):
    # Obtener las primeras 4000 filas de users_reviews
    users_reviews_first_4000 = users_reviews.head(4000)

    # Filtrar las reseñas para el año dado y las reseñas recomendadas y positivas/neutrales
    filtered_reviews = users_reviews_first_4000[(users_reviews_first_4000['posted year'] == anio) & (users_reviews_first_4000['recommend'] == True) & (users_reviews_first_4000['sentiment_analysis'] >= 0)]

    # Realizar un merge de los DataFrames users_items, filtered_reviews y steam_games
    merged_data = pd.merge(users_items, filtered_reviews, on='user_id')
    merged_data = pd.merge(merged_data, steam_games, left_on='id', right_on='id')

    # Calcular la cantidad total de recomendaciones para cada juego y ordenarlos en orden descendente
    game_recommendations = merged_data.groupby('title')['recommend'].count().reset_index()
    game_recommendations = game_recommendations.rename(columns={'recommend': 'recommend_count'})
    game_recommendations = game_recommendations.sort_values(by='recommend_count', ascending=False)

    # Tomar los 3 juegos más recomendados
    top_3_games = game_recommendations.head(3)

    # Formatear la salida en el formato deseado
    result = [{"Puesto {}: {}".format(i + 1, row['title']): row['recommend_count']} for i, row in top_3_games.iterrows()]

    return result




@app.get('/UsersNotRecommend/{anio}')
def UsersNotRecommend(anio: int):
    # Obtener las primeras 2000 filas de users_reviews
    users_reviews_first_4000 = users_reviews.head(4000)

    # Realizar un merge entre steam_games y users_reviews en base a la columna 'item_id'
    merged_data = pd.merge(users_reviews_first_4000, steam_games, left_on='item_id', right_on='id', how='inner')

    # Filtrar las reseñas para el año dado y las reseñas NO recomendadas y con comentarios negativos
    filtered_reviews = merged_data[(merged_data['posted year'] == anio) & (merged_data['recommend'] == False)]

    # Calcular la cantidad de reseñas negativas por juego
    negative_reviews_count = filtered_reviews.groupby('title')['recommend'].count().reset_index()
    negative_reviews_count = negative_reviews_count.rename(columns={'recommend': 'negative_reviews_count'})

    # Obtener el top 3 de juegos con menos recomendaciones negativas
    top_3_least_recommended = negative_reviews_count.nlargest(3, 'negative_reviews_count')

    # Crear la respuesta en el formato deseado
    result = [{"Puesto {}: {}".format(i + 1, row['title']): row['negative_reviews_count']} for i, row in top_3_least_recommended.iterrows()]

    # Devolver el resultado
    return result



@app.get('/sentiment_analysis/{anio}')
def sentiment_analysis(anio: int):
    if anio < 1900 or anio > 2023:
        return {"Error": "Año fuera de rango"}

    # Obtener las primeras 2000 filas de users_reviews
    users_reviews_first_4000 = users_reviews.head(4000)

    # Filtra los datos para el año proporcionado
    reviews_anio = users_reviews_first_4000[users_reviews_first_4000['posted year'] == anio]

    # Cuenta los registros para cada categoría de análisis de sentimiento
    sentiment_counts = reviews_anio['sentiment_analysis'].value_counts()

    # Convierte el resultado a un diccionario
    result = sentiment_counts.to_dict()

    return result


#Modelo machine learning

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Cargar los primeros 1000 datos de tu conjunto de datos
steam_games = pd.read_csv('data/df_games_clean.csv', nrows=1000)

# Crear la matriz TF-IDF
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(steam_games['genres'])

# Calcular la similitud del coseno entre los juegos
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

@app.get("/recommend/{game_id}")
async def get_recommendations(game_id: int):
    # Obtener el índice del juego correspondiente al ID dado
    idx = steam_games.index[steam_games['id'] == game_id].tolist()[0]

    # Calcular las puntuaciones de similitud del coseno para todos los juegos
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Ordenar los juegos según las puntuaciones de similitud
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Obtener los 5 juegos más similares (excluyendo el juego de entrada)
    sim_scores = sim_scores[1:6]

    # Obtener los índices de los juegos recomendados
    game_indices = [i[0] for i in sim_scores]

    # Devolver los títulos de los juegos recomendados
    recommendations = steam_games['title'].iloc[game_indices].tolist()
    return recommendations








