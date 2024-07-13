# Здесь создаю функции запросов к БД

# Импорт библиотек

# Импорт функций из библиотек
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.sql import text

# Импорт из файлов
from app.database.models import async_session
from app.database.models import User, ChatUsers, Chat, Admin


# Функция обращается к БД и проверяет связь пользователя и чата в бд
# Если такой связи нет - она создается
# Если пользователь состоит в 2х и более чатах, возвращает значение True
async def set_user_chat(tg_id, chat_id, chat_title):
    async with async_session() as session:
        if not tg_id == chat_id:  # Фильтр, чтобы в базу не добавлялся чат пользователя с ботом
            setsql = True
        else:
            setsql = False

        user = await session.scalar(select(ChatUsers).where(ChatUsers.tg_id == tg_id, ChatUsers.chat_id == chat_id))

        if not user and setsql:
            session.add(ChatUsers(tg_id=tg_id, chat_id=chat_id, chat_title=chat_title))
            await session.commit()  # сохраняем информацию
        else:
            pass

        count_value = await session.scalar(select(func.count()).select_from(ChatUsers).where(ChatUsers.tg_id == tg_id))

        if count_value <= 1:
            return True
        else:
            return False


# Используем контекстный менеджер, чтобы сессия закрывалась после исполнения функции
# Функция сохраняет id и никнейм пользователя в БД
# Need FIX: Если пользователь сменит никнейм -- бд не обновится (нужно ли это?)
async def set_user(tg_id, username):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, tg_username=username))
            await session.commit()  # сохраняем информацию


# Функция регистрирует ID чата и чат в БД
async def set_chat(chat_id, chat_title):
    async with async_session() as session:
        chat = await session.scalar(select(Chat).where(Chat.chat_id == chat_id))

        if not chat:
            print(chat_id)
            session.add(Chat(chat_id=chat_id, chat_title=chat_title))
            await session.commit()  # сохраняем информацию


async def get_chats(tg_id):  # Получаю список чатов, в которые вступил конкретный пользователь
    async with async_session() as session:
        count_value = await session.scalar(select(func.count()).select_from(ChatUsers).where(ChatUsers.tg_id == tg_id))
        data = await session.execute(select(ChatUsers.chat_title).where(ChatUsers.tg_id == tg_id))
        data_fetch = data.fetchall()
        data_list = []
        index = 0
        while index < count_value:
            first_strip = str(data_fetch[index]).strip("()")
            second_strip = f'— {first_strip.strip(",'")}'
            data_list.append(second_strip)
            index += 1
        data_return = '\n'.join(map(str, data_list))
        return data_return


async def get_list_chats():  # Получаю список id всех чатов из БД
    async with async_session() as session:
        data = await session.execute(select(Chat.chat_id))
        data_fetch = data.fetchall()

        data_list = []
        index = 0
        while index < len(data_fetch):
            first_strip = str(data_fetch[index]).strip("()")
            second_strip = first_strip.strip(",'")
            data_list.append(second_strip)
            index += 1

        return data_list


# Функция регистрации администраторов
async def reg_admin(tg_id, username, first_name):
    async with async_session() as session:
        admin = await session.scalar(select(Admin).where(Admin.tg_id == tg_id))
        if not admin:
            session.add(Admin(tg_id=tg_id, username=username, first_name=first_name))
            await session.commit()


# Работа с репутацией
# Функция обращается к БД и выгружает значение очков репутации
async def check_karma(tg_id, tg_id_recipient):
    async with async_session() as session:
        sender = await session.scalar(select(User).where(User.tg_id == tg_id))
        recipitent = await session.scalar(select(User).where(User.tg_id == tg_id_recipient))

        if sender and recipitent:
            text_recipitent = text(f"SELECT tg_id, karma_capital FROM users WHERE tg_id = {tg_id_recipient}")
            text_sender = text(f"SELECT tg_id, karma_value FROM users WHERE tg_id = {tg_id}")
            karma_sender = await session.execute(text_sender)
            karma_recipitent = await session.execute(text_recipitent)
            await session.commit()
            return karma_sender, karma_recipitent


# Функция обновляет репутацию пользователя и уменьшает очки репутации у отправителя
async def update_karma(id_send, send_new_karma,
                       recipient_id, recipient_new_karma):
    async with async_session() as session:
        s = await session.scalar(select(User).where(User.tg_id == id_send))
        s.karma_value = int(send_new_karma)
        r = await session.scalar(select(User).where(User.tg_id == recipient_id))
        r.karma_capital = int(recipient_new_karma)
        session.add(s, r)
        await session.commit()
