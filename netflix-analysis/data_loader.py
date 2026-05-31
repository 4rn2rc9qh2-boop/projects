import pandas as pd

LIST_COLUMNS = ("director", "cast", "country", "listed_in")
TEXT_COLUMNS = ("title", "description","listed_in","cast",
    "director","country","rating", "type",)

#превращает в строки и очищает от пробелов
def _split_to_list(value: object) -> list[str]:
    if pd.isna(value):
        return []
    return [item.strip() for item in str(value).split(",") if item.strip()]

#склеивает строки 
def _join_iterable(items):
    return " ".join(str(item).strip() for item in items if str(item).strip())

#читает csv
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

#подготавливает данные, очищает от мусора
def clean_data(df):
    df = df.copy()

    for column in LIST_COLUMNS:
        df[column] = df[column].apply(_split_to_list)

    df["content_text"] = df.apply(build_content_text, axis=1)

    df["title_normalized"] = (
        df["title"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    return df
def build_content_text(row: pd.Series) -> str:
    parts: list[str] = []
    for column in TEXT_COLUMNS:
        value = row.get(column, "")
        if isinstance(value, list):
            parts.append(_join_iterable(value))
        elif pd.notna(value):
            parts.append(str(value).strip())
    return " ".join(part for part in parts if part)


def load_and_clean_data(path: str) -> pd.DataFrame:
    return clean_data(load_data(path))


if __name__ == "__main__":
    dataset_path = "data/netflix_titles.csv"
    dataset = load_and_clean_data(dataset_path)
    print(dataset.head())
