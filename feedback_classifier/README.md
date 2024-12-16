# Классификатор отзывов
Данный классификатор предназначен для автоматической категоризации отзывов пользователей о работе сервисов нашего приложения. После взаимодействия с нашими сервисами, пользователю предлагается оставить отзыв, который затем будет обработан и оценен с помощью классификатора.

# Пример использования

```python
import requests

API_URL = "https://api-inference.huggingface.co/models/blanchefort/rubert-base-cased-sentiment"
headers = {"Authorization": "Bearer hf_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"}

def query(payload):
  response = requests.post(API_URL, headers=headers, json=payload)
  return response.json()
  
output = query({
  "inputs": "Все хорошо"
})

print(output)
```

# Ответственный за разработку
1. Семён Квасенко