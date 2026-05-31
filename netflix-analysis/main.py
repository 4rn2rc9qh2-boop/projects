import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import networkx as nx

from data_loader import load_and_clean_data
from geo_analysis import get_top_countries

from similarity import (
    build_similarity_matrix,
    get_recommendations
)

from trends import generate_tv_show_growth_summary


# ================= DATA =================

df = load_and_clean_data("data/netflix_titles.csv")

matrix = build_similarity_matrix(df)

trend_canvas = None
network_canvas = None


# ================= MAIN WINDOW =================

root = tk.Tk()

root.title("Netflix Analyzer")

root.geometry("1200x900")


# ================= TABS =================

notebook = ttk.Notebook(root)

notebook.pack(fill="both", expand=True)

main_tab = tk.Frame(notebook)
analytics_tab = tk.Frame(notebook)

notebook.add(main_tab, text="Main")
notebook.add(analytics_tab, text="Analytics")


# =========================================================
# ===================== MAIN TAB ==========================
# =========================================================

# ---------------- TOP COUNTRIES ----------------

countries_label = tk.Label(
    main_tab,
    text="Top Countries",
    font=("Arial", 18)
)

countries_label.pack(pady=10)

countries_text = tk.Text(
    main_tab,
    height=10,
    width=80
)

countries_text.pack(pady=10)


def show_top_countries():

    countries_text.delete("1.0", tk.END)

    top_countries = get_top_countries(df)

    for country, count in top_countries.items():

        countries_text.insert(
            tk.END,
            f"{country}: {count}\n"
        )


countries_button = tk.Button(
    main_tab,
    text="Show Top Countries",
    command=show_top_countries
)

countries_button.pack(pady=10)


# ---------------- RECOMMENDATIONS ----------------

recommendation_label = tk.Label(
    main_tab,
    text="Movie Recommendations",
    font=("Arial", 18)
)

recommendation_label.pack(pady=10)

recommendation_entry = tk.Entry(
    main_tab,
    width=40
)

recommendation_entry.pack(pady=10)

recommendation_text = tk.Text(
    main_tab,
    height=10,
    width=80
)

recommendation_text.pack(pady=10)


def show_recommendations():

    recommendation_text.delete("1.0", tk.END)

    title = recommendation_entry.get()

    recommendations = get_recommendations(
        title,
        df,
        matrix
    )

    if recommendations.empty:

        recommendation_text.insert(
            tk.END,
            "Movie not found"
        )

        return

    for _, row in recommendations.iterrows():

        recommendation_text.insert(
            tk.END,
            f"{row['title']} ({row['release_year']})\n"
        )


recommendation_button = tk.Button(
    main_tab,
    text="Find Similar",
    command=show_recommendations
)

recommendation_button.pack(pady=10)


# =========================================================
# ================== ANALYTICS TAB ========================
# =========================================================

# ---------------- TRENDS ----------------

trends_label = tk.Label(
    analytics_tab,
    text="Netflix Trends",
    font=("Arial", 18)
)

trends_label.pack(pady=10)

trends_text = tk.Text(
    analytics_tab,
    height=5,
    width=80
)

trends_text.pack(pady=10)


def show_trends():
    global trend_canvas

    trends_text.delete("1.0", tk.END)

    summary = generate_tv_show_growth_summary(df)

    trends_text.insert(
        tk.END,
        summary
    )

    trends = (
        df.groupby(["release_year", "type"])
        .size()
        .unstack(fill_value=0)
    )

    fig, ax = plt.subplots(figsize=(7, 4))

    if "Movie" in trends.columns:

        ax.plot(
            trends.index,
            trends["Movie"],
            label="Movies"
        )

    if "TV Show" in trends.columns:

        ax.plot(
            trends.index,
            trends["TV Show"],
            label="TV Shows"
        )

    ax.set_title("Netflix Trends")

    ax.set_xlabel("Year")

    ax.set_ylabel("Count")

    ax.legend()

    if trend_canvas is not None:

        trend_canvas.get_tk_widget().destroy()

    trend_canvas = FigureCanvasTkAgg(
        fig,
        master=analytics_tab
    )

    trend_canvas.draw()

    trend_canvas.get_tk_widget().pack(pady=10)


trends_button = tk.Button(
    analytics_tab,
    text="Show Trends",
    command=show_trends
)

trends_button.pack(pady=10)


# ---------------- ACTOR NETWORK ----------------

network_label = tk.Label(
    analytics_tab,
    text="Actor Network",
    font=("Arial", 18)
)

network_label.pack(pady=10)

network_text = tk.Text(
    analytics_tab,
    height=10,
    width=80
)

network_text.pack(pady=10)


def show_actor_network():

    global network_canvas

    graph = nx.Graph()

    movie_titles = set(df["title"])

    # строим граф
    for _, row in df.iterrows():

        title = row["title"]

        actors = row["cast"]

        if not isinstance(actors, list):
            continue

        for actor in actors:

            graph.add_edge(actor, title)

    # только актеры
    actor_degrees = []

    for node, degree in graph.degree():

        if node not in movie_titles:

            actor_degrees.append((node, degree))

    # топ актеров
    top_actors = sorted(
        actor_degrees,
        key=lambda x: x[1],
        reverse=True
    )[:5]

    # очищаем текст
    network_text.delete("1.0", tk.END)

    network_text.insert(
        tk.END,
        "Top actors:\n\n"
    )

    for actor, degree in top_actors:

        network_text.insert(
            tk.END,
            f"{actor}: {degree}\n"
        )

    # маленький граф
    small_graph = nx.Graph()

    edge_count = 0

    for edge in graph.edges():

        small_graph.add_edge(*edge)

        edge_count += 1

        if edge_count >= 20:
            break

    # удаляем старый график
    if network_canvas is not None:

        network_canvas.get_tk_widget().destroy()

    # рисуем
    fig, ax = plt.subplots(figsize=(6, 4))

    pos = nx.spring_layout(
        small_graph,
        seed=42
    )

    nx.draw(
        small_graph,
        pos,
        with_labels=False,
        node_size=80,
        ax=ax
    )

    ax.set_title("Actor Network")

    network_canvas = FigureCanvasTkAgg(
        fig,
        master=analytics_tab
    )

    network_canvas.draw()

    network_canvas.get_tk_widget().pack(pady=10)

network_button = tk.Button(
    analytics_tab,
    text="Show Actor Network",
    command=show_actor_network
)

network_button.pack(pady=10)


# ================= START APP =================

root.mainloop()