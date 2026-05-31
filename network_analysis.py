import networkx as nx
import pandas as pd

# создание графа актеров или режиссеров
def build_people_graph(df, column_name):
    graph = nx.Graph()
    # проходим по всем фильмам
    for _, row in df.iterrows():
        title = row["title"]
        # берем актеров или режиссеров
        people = row[column_name]
        # создаем связи
        for person in people:

            graph.add_node(person)
            graph.add_node(title)
            graph.add_edge(person, title)

    return graph

# топ самых связанных людей
def get_top_people(graph, top_n=10):
    # degree = количество связей
    degrees = graph.degree()
    # сортируем по количеству связей
    sorted_people = sorted(
        degrees,
        key=lambda x: x[1],
        reverse=True
    )
    # превращаем в таблицу
    rows = []
    for person, degree in sorted_people[:top_n]:
        rows.append({
            "name": person,
            "connections": degree
        })
    return pd.DataFrame(rows)

# краткая информация о графе
def get_graph_info(graph):
    info = {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges()
    }

    return info