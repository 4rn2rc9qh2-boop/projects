import pandas as pd


def get_top_countries(df, top_n=20):
    all_countries = []
    #собираем все страны
    for countries in df["country"]:
        for country in countries:
            all_countries.append(country)
    country_counts = pd.Series(all_countries).value_counts()
    return country_counts.head(top_n)

def get_country_type_counts(df, country):
    filtered_rows = []
    for i in range(len(df)):
        countries = df["country"].iloc[i]
        if country in countries:
            filtered_rows.append(df.iloc[i])
    filtered_df = pd.DataFrame(filtered_rows)
    return filtered_df["type"].value_counts()

def get_genre_distribution_for_country(df, country, top_n=10):
    genres = []
    for i in range(len(df)):
        countries = df["country"].iloc[i]
        if country in countries:
            movie_genres = df["listed_in"].iloc[i]
            for genre in movie_genres:
                genres.append(genre)
    # считаем жанры
    genre_counts = pd.Series(genres).value_counts()
    return genre_counts.head(top_n)