from transformers import pipeline


# Используем модель для анализа тональности на русском языке
classifier = pipeline(
    "sentiment-analysis",
    model="blanchefort/rubert-base-cased-sentiment"
)


async def classify_reviews(reviews):
    results = {
        "positive": [],
        "negative": []
    }

    for review in reviews:
        sentiment = classifier(review)[0]
        label = sentiment['label']

        # Переводим метки модели в наши категории
        if label == "POSITIVE":
            results['positive'].append((review, sentiment['score']))
        elif label == "NEGATIVE":
            results['negative'].append((review, sentiment['score']))

    return results
