def format_coordinates(*coords):
    # Преобразуем каждый tuple в строку и объединяем их с помощью тильды
    return '~'.join(f"{lat},{lon}" for lat, lon in coords)

def ya_map(coord_str):
  return "https://yandex.ru/maps/?rtext=" + coord_str