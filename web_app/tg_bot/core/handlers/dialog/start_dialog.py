import os
from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from core.FSM.dialog_fsm import DialogReg
import core.keyboards.reply_kbs as reply_kb
from dotenv import load_dotenv
import requests
import core.database.requests as rq

load_dotenv()


# хендлеры для начала диалога
msg_router = Router()


# входной хендлер
@msg_router.message(DialogReg.city_chose, F.text=='Любой')
async def handle_city(message: Message, state: FSMContext):
    await state.set_state(DialogReg.service_chose)

    await state.update_data(location=message.text)

    bot_answer = 'Выберите сервис на клавиатуре'

    await rq.logging(tg_id=message.from_user.id,
                     client_action='Выбрал любой город',
                     bot_answer_text=bot_answer)

    await message.answer(bot_answer,
                         reply_markup=reply_kb.service_kb)


# хендлер возвращения к выбору сервисов
@msg_router.message(F.text == 'Вернуться к выбору сервиса')
async def handle_back_to_serevice(message: Message, state: FSMContext):
    await state.set_state(DialogReg.service_chose)

    bot_answer='Выберите сервис на клавиатуре'

    await rq.logging(tg_id=message.from_user.id,
                     client_action='Вернулся к выбору сервиса',
                     bot_answer_text=bot_answer)

    await message.answer(bot_answer,
                         reply_markup=reply_kb.service_kb)


# хендлер возвращения к выбору сервисов
@msg_router.message(F.text == 'Отмена')
async def handle_decline(message: Message, state: FSMContext):
    await state.set_state(DialogReg.service_chose)

    bot_answer = 'Выберите сервис'

    await rq.logging(tg_id=message.from_user.id,
                     client_action='Нажал кнопку отмена',
                     bot_answer_text=bot_answer)

    await message.answer(bot_answer,
                         reply_markup=reply_kb.service_process_kb)


# хендлер возвращения к выбору сервисов
@msg_router.message(F.text == 'Вернуться в главное меню')
async def handle_back_to_menu(message: Message, state: FSMContext):
    await state.set_state(DialogReg.service_chose)

    bot_answer = 'Выберите сервис'

    await rq.logging(tg_id=message.from_user.id,
                     client_action='Вернулся в главное меню',
                     bot_answer_text=bot_answer)

    await message.answer(bot_answer,
                         reply_markup=reply_kb.service_kb)

# хендлер обработки геолокации
@msg_router.message(DialogReg.city_chose, F.location)
async def handle_location(message: Message, state: FSMContext):
    await state.set_state(DialogReg.service_chose)

    await state.update_data(lat=str(message.location.latitude),
                            lon=str(message.location.longitude))

    bot_answer = 'Выберите сервис на клавиатуре'

    await rq.logging(tg_id=message.from_user.id,
                     client_action='Отправил координаты',
                     bot_answer_text=bot_answer)

    await message.answer(bot_answer,
                         reply_markup=reply_kb.service_kb)

# входной хендлер для отзывов
@msg_router.message(DialogReg.service_chose, F.text=='Оставить отзыв')
async def handle_rev(message: Message, state: FSMContext):
    await state.set_state(DialogReg.start_rev)

    bot_answer = 'Напишите ваш отзыв'

    await rq.logging(tg_id=message.from_user.id,
                     client_action='Решил оставить отзыв',
                     bot_answer_text=bot_answer)

    await message.answer(bot_answer,
                         reply_markup=reply_kb.exit_to_menu)


# последний хендлер отзывов
# после него возвращаемся в начальное состояние
@msg_router.message(DialogReg.start_rev, F.text)
async def handle_answer(message: Message, state: FSMContext):
    await state.set_state(DialogReg.service_chose)

    rev_answer = requests.post(
            f"https://datasphere.api.cloud.yandex.net/datasphere/v1/nodes/{os.getenv('NODE_REV_ID')}:execute",
            headers={"Authorization": f"Bearer {os.getenv('IAM-TOKEN')}"},
            json={
                "folder_id": f"{os.getenv('CATALOG_ID')}",
                "node_id": f"{os.getenv('NODE_REV_ID')}",
                "input": {
                    "text": message.text

                }
            }
        )

    bot_answer = 'Спасибо за отзыв'

    await rq.logging(tg_id=message.from_user.id,
                     client_action='Решил оставить отзыв',
                     bot_answer_text=f"Бот определил отзыв как {rev_answer} и ответил {bot_answer}")

    await message.answer(bot_answer,
                         reply_markup=reply_kb.service_kb)















