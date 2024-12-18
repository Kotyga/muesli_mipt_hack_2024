from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

test_rev_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text="Написать отзыв",
                              callback_data="test_rev")],])

path_build_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text="Построить путь к объекту",
                              callback_data="build_path")],])