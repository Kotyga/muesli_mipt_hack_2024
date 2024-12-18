import asyncio
import os
import requests
from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from core.FSM.dialog_fsm import DialogReg
import core.keyboards.reply_kbs as reply_kb
from core.utils.speech_flow import speech_to_text
from pathlib import Path
from core.utils.speech_flow import text_to_speech
import core.database.requests as rq


# хендлеры для работы c гидом
guide_router = Router()


# начальный хендлер обработки гида
@guide_router.message(DialogReg.service_chose, F.text == 'Туристический гид')
async def handle_guide_service(message: Message, state: FSMContext):
    await state.set_state(DialogReg.guide_time)

    bot_answer = 'Выберите каким образом вы хотите общаться с гидом'

    await rq.logging(tg_id=message.from_user.id,
                     client_action='Нажал кнопку "Туристический гид"',
                     bot_answer_text=bot_answer)

    await message.answer(bot_answer,
                         reply_markup=reply_kb.guide_kb)


# хендлер обрабатывающий текст
@guide_router.message(DialogReg.guide_time, F.text == 'Текст')
async def handle_guide_text(message: Message, state: FSMContext):
    await state.set_state(DialogReg.guide_user_answer_txt)

    bot_answer = 'Напишите о чем бы вы хотели поговорить с гидом'

    await rq.logging(tg_id=message.from_user.id,
                     client_action='Выбрал общение с гидом через текст',
                     bot_answer_text=bot_answer)

    await message.answer(bot_answer,
                         reply_markup=reply_kb.service_process_kb)


# хендлер переключающий состояние на аудио
@guide_router.message(DialogReg.guide_time, F.text == 'Аудио')
async def handle_guide_audio(message: Message, state: FSMContext):
    await state.set_state(DialogReg.guide_user_answer_audio)

    bot_answer = 'Запишите голосовое сообщение'

    await rq.logging(tg_id=message.from_user.id,
                     client_action='Выбрал общение с гидом через аудио',
                     bot_answer_text=bot_answer)

    await message.answer(bot_answer,
                         reply_markup=reply_kb.service_process_kb)


# хендлер для транскрипции аудио
@guide_router.message(DialogReg.guide_user_answer_audio, F.content_type == "voice")
async def handle_guide_audio(message: Message, state: FSMContext):
    await state.set_state(DialogReg.guide_type_answer)

    Path(f'user_data').mkdir(parents=True, exist_ok=True)

    file = await message.bot.get_file(message.voice.file_id)
    file_path = file.file_path

    await message.bot.download_file(file_path=file_path, destination=f'user_data/{message.from_user.id}_voice')

    recognized_text = await speech_to_text(f'user_data/{message.from_user.id}_voice', "ru-RU")
    await message.answer(f"Распознанный текст:\n{recognized_text}")

    os.remove(f'user_data/{message.from_user.id}_voice')

    bot_answer = 'Выберите вариант ответа гида'

    await rq.logging(tg_id=message.from_user.id,
                     client_action='Записал аудио',
                     bot_answer_text=bot_answer)

    await message.answer('Выберите вариант ответа гида',
                         reply_markup=reply_kb.guide_kb)


# хендлер для выбора варианта ответа гида
@guide_router.message(DialogReg.guide_user_answer_txt, F.text)
async def handle_type_answer_guide(message: Message, state: FSMContext):
    await state.set_state(DialogReg.guide_type_answer)
    await state.update_data(guide_txt=message.text)

    bot_answer = 'Выберите вариант ответа гида'

    await rq.logging(tg_id=message.from_user.id,
                     client_action='Перешел к выбору варианта ответа гида',
                     bot_answer_text=bot_answer)

    await message.answer(bot_answer,
                         reply_markup=reply_kb.guide_kb)


# хендлер для реализации ответа гида в зависимости от выбранного варианта
@guide_router.message(DialogReg.guide_type_answer, lambda message: message.text in ["Текст", "Аудио"])
async def handle_guide_answer(message: Message, state: FSMContext):
    await state.update_data(guide_type_answer=message.text)

    data = await state.get_data()

    guide_answer = requests.post(
            f"https://datasphere.api.cloud.yandex.net/datasphere/v1/nodes/{os.getenv('NODE_GUIDE_ID')}:execute",
            headers={"Authorization": f"Bearer {os.getenv('IAM-TOKEN')}"},
            json={
                "folder_id": f"{os.getenv('CATALOG_ID')}",
                "node_id": f"{os.getenv('NODE_GUIDE_ID')}",
                "input": {
                    "text": data['guide_txt']

                }
            }
        )

    if message.text == "Текст":
        await state.set_state(DialogReg.service_chose)

        await rq.logging(tg_id=message.from_user.id,
                         client_action='Выбрал текстовый вариант ответа гида',
                         bot_answer_text=guide_answer)

        await message.answer(guide_answer,
                             reply_markup=reply_kb.service_kb)

    if message.text == "Аудио":
        await asyncio.sleep(5)

        await state.set_state(DialogReg.service_chose)

        audio_answer = await text_to_speech(guide_answer)

        audio = FSInputFile(f"user_data/{audio_answer}")

        await rq.logging(tg_id=message.from_user.id,
                         client_action='Выбрал аудио вариант ответа гида',
                         bot_answer_text='Ответил аудио')

        # озвучивание ответа
        await message.answer_audio(audio=audio,
                                   reply_markup=reply_kb.service_kb)










