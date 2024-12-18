from core.database.models import async_session
from core.database.models import User


async def logging(tg_id, client_action, bot_answer_text, bot_answer_image=""):
    async with async_session() as session:
        session.add(User(tg_id=tg_id,
                         client_action=client_action,
                         bot_answer_text=bot_answer_text,
                         bot_answer_image=bot_answer_image))
        await session.commit()
