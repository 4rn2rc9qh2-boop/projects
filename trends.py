import pandas as pd


# подсчет фильмов и сериалов по годам
def get_yearly_type_counts(df):
    rows = []
    # группируем данные
    grouped = df.groupby(["release_year", "type"]).size()
    # превращаем в список словарей
    for (year, content_type), count in grouped.items():
        rows.append({
            "release_year": year,
            "type": content_type,
            "count": count
        })

    # создаем DataFrame
    result = pd.DataFrame(rows)
    # сортируем
    result = result.sort_values(["release_year", "type"])
    return result

# текстовый вывод про рост TV Show
def generate_tv_show_growth_summary(df):
    counts = get_yearly_type_counts(df)
    # оставляем только сериалы
    tv_counts = counts[counts["type"] == "TV Show"]
    # если данных нет
    if len(tv_counts) == 0:
        return "В датасете нет TV Show."

    # первый год
    first_year = tv_counts.iloc[0]["release_year"]
    first_count = tv_counts.iloc[0]["count"]
    # последний год
    last_year = tv_counts.iloc[-1]["release_year"]
    last_count = tv_counts.iloc[-1]["count"]
    # определяем тренд
    if last_count > first_count:
        trend = "рост"
    else:
        trend = "снижение"
    # формируем текст
    summary = (
        f"TV Show показывают {trend}: "
        f"от {first_count} релизов в {first_year} году "
        f"до {last_count} релизов в {last_year} году."
    )

    return summary