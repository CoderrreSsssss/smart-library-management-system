import pandas as pd

def recommend(book_title, books):

    df = pd.DataFrame(books)

    if book_title not in df["title"].values:
        return []

    genre = df[df["title"] == book_title]["genre"].values[0]

    rec = df[df["genre"] == genre]["title"].tolist()

    return [b for b in rec if b != book_title][:5]
