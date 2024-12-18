from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Поделиться геолокацией', request_location=True)],
        [KeyboardButton(text='Любой')],
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню.'
)

service_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Поиск по фото')],
        [KeyboardButton(text='Поиск по тексту')],
        [KeyboardButton(text='Туристический гид')],
        [KeyboardButton(text='Оставить отзыв')],
        [KeyboardButton(text='Отмена')],
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню.'
)

num_photos_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='1')],
        [KeyboardButton(text='2')],
        [KeyboardButton(text='3')],
        [KeyboardButton(text='4')],
        [KeyboardButton(text='5')],
        [KeyboardButton(text='Вернуться к выбору сервиса')],
        [KeyboardButton(text='Отмена')],
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню.'
)

guide_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Текст')],
        [KeyboardButton(text='Аудио')],
        [KeyboardButton(text='Вернуться к выбору сервиса')],
        [KeyboardButton(text='Отмена')],
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню.'
)

service_process_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Вернуться к выбору сервиса')],
        [KeyboardButton(text='Отмена')],
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню.'
)

exit_to_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Вернуться в главное меню')],
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню.'
)

