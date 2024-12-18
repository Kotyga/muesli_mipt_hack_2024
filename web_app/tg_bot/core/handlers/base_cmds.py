from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
import core.keyboards.reply_kbs as reply_kb
from core.FSM.dialog_fsm import DialogReg
from aiogram.fsm.context import FSMContext
import core.database.requests as rq


# хендлеры базовых команд
base_cmd_router = Router()


@base_cmd_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(DialogReg.city_chose)
    await state.update_data(user_tg_id=message.from_user.id)

    bot_answer = 'Выберите город на клавиатуре'

    await rq.logging(tg_id=message.from_user.id,
                     client_action='Старт бота',
                     bot_answer_text=bot_answer)

    await message.answer(bot_answer,
                         reply_markup=reply_kb.main_kb)



