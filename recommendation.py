import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def recommend():

    data = {
        "book": ["Python", "AI Basics", "Machine Learning", "Deep Learning", "SQL Guide"],
        "python": [1,0,0,0,0],
        "ai": [0,1,1,1,0],
        "data": [0,1,1,1,1]
    }

    df = pd.DataFrame(data)

    similarity = cosine_similarity(df.iloc[:,1:])

    scores = list(enumerate(similarity[0]))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    rec = []

    for i in scores[1:4]:
        rec.append(df.iloc[i[0]].book)

    return rec
