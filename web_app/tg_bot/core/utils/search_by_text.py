import pandas as pd
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


def most_similar_sentence(input_string, df, embeddings_file="precomputed_embeddings.pkl"):
    """
    Определяет наиболее похожую строку из предварительно сохраненного списка на входную строку по косинусному сходству.

    Args:
        input_string (string): Строка, для которой ищем наиболее похожую.
        df (DataFrame): DataFrame с колонкой 'clip_lables'.
        embeddings_file (string): Путь к файлу с сохраненными эмбеддингами.

    Returns:
        int: Индекс наиболее похожей строки в DataFrame.
    """
    with open(embeddings_file, "rb") as f:
        data = pickle.load(f)

    sentences = data["sentences"]
    sentence_embeddings = data["embeddings"]

    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    input_embedding = model.encode([input_string])

    similarities = cosine_similarity(input_embedding, sentence_embeddings)[0]
    most_similar_index = np.argmax(similarities)

    return df[df['clip_lables'] == sentences[most_similar_index]].index[0]


if __name__ == '__main__':
    input_string = "Культурные учреждения Екатеринбурга, такие как Театр кукол, включая его здание с куполом и фасад, украшенный часами."
    df = pd.read_csv('../../new_hack.csv')
    result = most_similar_sentence(input_string, df)
    print(df.loc[result])