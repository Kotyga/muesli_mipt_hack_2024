from aiogram.fsm.state import StatesGroup, State


class DialogReg(StatesGroup):
    city_chose = State()
    service_chose = State()
    photo_search = State()
    photo_chose_num = State()
    text_search_start = State()
    text_search_end = State()
    guide_time = State()
    guide_user_answer_audio = State()
    guide_user_answer_txt = State()
    guide_type_answer = State()

    location = State()

    lon = State()
    lat = State()

    start_rev = State()
    test_rev = State()

    user_tg_id = State()


