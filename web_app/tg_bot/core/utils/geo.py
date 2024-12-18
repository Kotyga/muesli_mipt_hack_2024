
async def format_coordinates(*coords):
    return '~'.join(f"{lat},{lon}" for lat, lon in coords)


async def ya_map(coord_str):
    return "https://yandex.ru/maps/?rtext=" + coord_str