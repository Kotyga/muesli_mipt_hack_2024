import os
from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from core.FSM.dialog_fsm import DialogReg
import core.keyboards.reply_kbs as reply_kb
import core.keyboards.inline_kbs as inl_kb
import requests
import core.database.requests as rq

# хендлеры для работы изображениями
photos_router = Router()


# начальный хендлер обработки фото
@photos_router.message(DialogReg.service_chose, F.text == 'Поиск по фото')
async def handle_photo_service(message: Message, state: FSMContext):
    await state.set_state(DialogReg.photo_search)

    bot_answer = 'Пожалуйста пришлите фотографию'

    await rq.logging(tg_id=message.from_user.id,
                     client_action='Нажал кнопку "Поиск по фото"',
                     bot_answer_text=bot_answer)

    await message.answer(bot_answer,
                         reply_markup=reply_kb.service_process_kb)


# хендлер для сообщения об ошибке связанной с другим типом контента при загрузке фото
@photos_router.message(DialogReg.photo_search, F.content_type != "photo")
async def handle_not_photo(message: Message):
    bot_answer='Пожалуйста пришлите фотографию'

    await rq.logging(tg_id=message.from_user.id,
                     client_action='Пользователь прислал не фото',
                     bot_answer_text=bot_answer)

    await message.answer(bot_answer,
                         reply_markup=reply_kb.service_process_kb)


# хендлер получающий фото для обработки моделью
@photos_router.message(DialogReg.photo_search, F.photo)
async def handle_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]

    file_info = await message.bot.get_file(photo.file_id)
    file_path = file_info.file_path
    file_extension = file_path.split('.')[-1].lower()

    if file_extension in ['jpg', 'png']:
        await state.update_data(photo_search=photo)
        await state.set_state(DialogReg.photo_chose_num)

        bot_answer = "Выберите количество фото для отображения"

        await rq.logging(tg_id=message.from_user.id,
                         client_action='Пользователь прислал фото',
                         bot_answer_text=bot_answer)

        await message.reply(bot_answer,
                            reply_markup=reply_kb.num_photos_kb)
    else:
        bot_answer = "Неверный формат"

        await rq.logging(tg_id=message.from_user.id,
                         client_action='Пользователь прислал не тот формат фото',
                         bot_answer_text=bot_answer)

        await message.reply(bot_answer)


# последний хендлер обработки фото
# из него возвращаемся в начальное состояние
@photos_router.message(DialogReg.photo_chose_num, F.text)
async def handle_num_photo(message: Message, state: FSMContext):
    data = await state.get_data()

    photo = data['photo_search']

    try:
        await state.set_state(DialogReg.service_chose)
        num_photos = int(message.text)

        img, caption = requests.post(
            f"https://datasphere.api.cloud.yandex.net/datasphere/v1/nodes/{os.getenv('NODE_PHOTO_ID')}:execute",
            headers={"Authorization": f"Bearer {os.getenv('IAM-TOKEN')}"},
            json={
                "folder_id": f"{os.getenv('CATALOG_ID')}",
                "node_id": f"{os.getenv('NODE_PHOTO_ID')}",
                "input": {
                    "num_photos": num_photos,
                    "photo": photo

                }
            }
        )

        await rq.logging(tg_id=message.from_user.id,
                         client_action='Пользователь выбрал количество фото',
                         bot_answer_text=caption,
                         bot_answer_image=img)

        await message.answer_photo(photo=img,
                                   caption=caption,
                                   reply_markup=inl_kb.path_build_kb)

        await message.answer(text='Нажмите построить путь к объетку либо вернуться в главное меню.',
                             reply_markup=reply_kb.exit_to_menu)

    except Exception as e:
        bot_answer = "Ошибка при загрузке ответа фото модели"

        await rq.logging(tg_id=message.from_user.id,
                         client_action=bot_answer,
                         bot_answer_text=e)

        await message.answer(bot_answer)