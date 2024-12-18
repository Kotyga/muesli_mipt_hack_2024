from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from core.FSM.dialog_fsm import DialogReg
import core.keyboards.reply_kbs as reply_kb
from core.utils.search_by_text import most_similar_sentence
import pandas as pd
import base64
import core.keyboards.inline_kbs as inl_kb
from dotenv import load_dotenv
import core.database.requests as rq

load_dotenv()

# хендлеры для работы c короткими сообщениями
short_msg_router = Router()


# начальный хендлер обработки короткого текста
@short_msg_router.message(DialogReg.service_chose, F.text == 'Поиск по тексту')
async def handle_short_txt_service(message: Message, state: FSMContext):
    await state.set_state(DialogReg.text_search_start)
    bot_answer = 'Введите текст'

    await rq.logging(tg_id=message.from_user.id,
                     client_action='Нажал кнопку "Поиск по тексту"',
                     bot_answer_text=bot_answer)

    await message.answer(bot_answer,
                         reply_markup=reply_kb.service_process_kb)


# хендлер получающий текст для обработки моделью
@short_msg_router.message(DialogReg.text_search_start, F.text)
async def handle_short_txt(message: Message, state: FSMContext):
    await state.update_data(text_search=message.text)

    bot_answer = 'Выберете количество фото для отображения'

    await rq.logging(tg_id=message.from_user.id,
                     client_action='Ввел текст для поиска',
                     bot_answer_text=bot_answer)

    await state.set_state(DialogReg.text_search_end)
    await message.answer(bot_answer,
                         reply_markup=reply_kb.num_photos_kb)


# последний хендлер обработки короткого текста
@short_msg_router.message(DialogReg.text_search_end, F.text)
async def handle_num_photos_short_txt(message: Message, state: FSMContext):
    data = await state.get_data()

    short_text = data['text_search']

    df = pd.read_csv('new_hack.csv')

    find_answer = df.loc[most_similar_sentence(short_text, df)]

    with open("photo_from_csv/img_from_csv.png", "wb") as fh:
        fh.write(base64.b64decode(find_answer['image']))

    # result_text

    img = FSInputFile('photo_from_csv/img_from_csv.png')

    try:
        # количество отображаемых фото
        num_photos = int(message.text)

        state_data = await state.get_data()

        await rq.logging(tg_id=message.from_user.id,
                         client_action='Ввел текст для поиска',
                         bot_answer_text=find_answer['Name'],
                         bot_answer_image=img)

        if state_data['location'] == 'Любой':
            await state.set_state(DialogReg.service_chose)
            # Вывод выбранного количества фото
            await message.answer_photo(photo=img,
                                       caption=f"{find_answer['Name']}",
                                       reply_markup=reply_kb.service_kb)
            await message.answer("Возвращаемся в главное меню")

        else:
            # Вывод выбранного количества фото
            await state.set_state(DialogReg.service_chose)
            await message.answer_photo(photo=img,
                                       caption=f"{find_answer['Name']}",
                                       reply_markup=inl_kb.path_build_kb)

            await message.answer(text='Нажмите построить путь к объетку либо вернуться в главное меню.',
                                 reply_markup=reply_kb.exit_to_menu)

    except Exception as e:
        await rq.logging(tg_id=message.from_user.id,
                         client_action='Ошибка в модели для поиска по тексту',
                         bot_answer_text=e)

        await message.answer("Пожалуйста введите число")
        print(e)
