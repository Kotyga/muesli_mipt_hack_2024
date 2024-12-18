import os
from aiogram import F, Router
from aiogram.types import CallbackQuery
import core.keyboards.reply_kbs as reply_kb
from core.FSM.dialog_fsm import DialogReg
from aiogram.fsm.context import FSMContext
from core.utils.geo import format_coordinates, ya_map
from dotenv import load_dotenv
import core.database.requests as rq


load_dotenv()

clbks_router = Router()


@clbks_router.callback_query(F.data == "build_path")
async def build_path_to_object(callback_query: CallbackQuery, state: FSMContext):
    coord_str = await format_coordinates((os.getenv('CLIENT_LAT'), os.getenv('CLIENT_LON')),
                                         (os.getenv('OBJECT_LAT'), os.getenv('OBJECT_LON')))

    await callback_query.message.answer(await ya_map(coord_str))

    await callback_query.answer()

    await rq.logging(tg_id=callback_query.message.from_user.id,
                     client_action='Пользователь выбрал построить координаты',
                     bot_answer_text=coord_str)

    await state.set_state(DialogReg.service_chose)
    await callback_query.message.answer('Возвращаемся в главное меню',
                                        reply_markup=reply_kb.service_kb)