import random

# import from libraries
from aiogram import Router, F
from aiogram.filters import Command, CommandStart, CommandObject, ChatMemberUpdatedFilter, \
    KICKED, LEFT, MEMBER, RESTRICTED
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery
from aiogram.fsm.context import FSMContext

# import from modules
import app.database.request as rq
from app.database import crud_manager
from app.messages import msg_texts
from app.middlewares import ChatType
from config import get_id_chat_root, logger
from app.keyboards import keyboard_user_profile, to_support_key

router = Router()  # main handler


@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject) -> None:
    """
    Start handler
    :return: none
    """
    try:
        args: str = command.args

        if args:
            args_list: list = args.split('=')
            if len(args_list) > 1:
                key, value = args_list[0], args_list[1]
                await message.answer(f'Получил аргументы: {key}, {value}')
        else:
            # await message.answer(f'аргументов нет')
            pass
    except Exception as e:
        print(e)
        pass

    from_user = message.from_user
    await crud_manager.user.create_user(tg_id=from_user.id, username=from_user.username)
    await message.answer(f'Привет, {from_user.first_name}!')


# Добавляем пользователя в бд после вступления в чат
@router.chat_member(ChatMemberUpdatedFilter(
    member_status_changed=
    (KICKED | LEFT | -RESTRICTED)
    >>
    (+RESTRICTED | MEMBER)
))
async def get_member(update: ChatMemberUpdated) -> None:
    """
    Add user's info to DB after he's joined to chat
    and check number of chats, where he's member
    :param update:
    :return: None
    """
    chat = update.chat
    user = update.new_chat_member.user

    await crud_manager.user.create_user(tg_id=user.id, username=user.username)  # регистрируем юзера
    await rq.set_user_chat(user.id, chat.id)  # записываем в какой чат вступил
    count_chats = await rq.get_count_users_chat(user.id)  # получаем количество чатов

    if user.username is None:
        username_ = f'{user.first_name}'
    else:
        username_ = f'{user.first_name} (@{user.username})'

    if count_chats < 2:
        hello_txt = random.choice(msg_texts.hello_for_user)
        message_text = f'{hello_txt}, {username_}!'
        await update.answer(message_text)
    else:
        message_text = (f'Привет, {username_}!'
                        f'\nУчиться можно только на одном направлении'
                        f'\n\nЯ отправил админу сообщение, он свяжется с тобой и удалит тебя из других чатов')
        await update.answer(message_text)

        root_id = await get_id_chat_root()
        chats_titles_list = await rq.get_list_of_users_chats(user.id)
        chats_counter = len(chats_titles_list)
        chats_titles_str = '\n— '.join(map(str, chats_titles_list))
        await update.bot.send_message(chat_id=int(root_id),
                                      text=f'{username_}'
                                           f'\nвступил в несколько чатов ({chats_counter}): '
                                           f'\n\n— {chats_titles_str}'
                                           f'\n\nСвяжись с ним, чтобы обсудить детали')


@router.chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=
        (+RESTRICTED | MEMBER)
        >>
        (KICKED | LEFT | -RESTRICTED)
    )
)
async def remove_chat_member(update: ChatMemberUpdated) -> None:
    """
    Функция удаляет из БД связь пользователя с чатом в таблице chatandusers
    когда пользователь выходит из чата или его кикают
    :param update:
    :return: None
    """
    chat = update.chat
    user = update.new_chat_member.user
    try:
        await rq.remove_link_from_db(
            tg_user_id=user.id,
            tg_chat_id=chat.id,
        )
    except Exception as e:
        error_text_message = f'Ошибка при удалении user id {user.id} и chat id {chat.id}: {e}'
        logger.warning(error_text_message)

        root_id = await get_id_chat_root()
        await update.bot.send_message(chat_id=int(root_id),
                                      text=error_text_message)


# /-- karma start --/
# Функция увеличения репутации
@router.message(F.reply_to_message,
                F.text.lower().contains('+rep'),
                ChatType(chat_type=["group", "supergroup"]))
async def add_rep_to_user(message: Message) -> None:
    id_sender, id_recipient = message.from_user.id, message.reply_to_message.from_user.id

    if id_recipient in (message.bot.id, id_sender):
        msg = msg_texts.bot_karma_message if id_recipient == message.bot.id else msg_texts.self_karma_raise
        await message.reply(msg)
        return

    sender, recipient = await rq.check_karma(id_sender, id_recipient)

    if sender.karma_start_value <= 0:
        await message.reply(msg_texts.karmas_points_over)
    else:
        recipient_username = message.reply_to_message.from_user.username
        sender.remove_karma_points()

        await rq.update_karma(id_sender, id_recipient)
        await message.reply(f'Репутация @{recipient_username} повышена. '
                            f'У тебя осталось очков репутации - <b>{sender.karma_start_value}</b>')


# /-- karma end --/

@router.message(Command('myid'), ChatType(chat_type='private'))
async def get_user_id(message: Message | CallbackQuery) -> None:
    """
    Функция для получения пользователем своего тг-id
    """
    text_for_message = f'Твой id в телеграме: <code>{message.from_user.id}</code>'

    if isinstance(message, CallbackQuery):
        text_for_message = f'Твой id в телеграме: <code>{message.from_user.id}</code>'
        message = message.message

    await message.reply(text_for_message)


@router.message(Command('my'), ChatType(chat_type='private'))
async def get_user_profile(message: Message | CallbackQuery) -> None:
    """
    Вызов профиля пользователя
    """
    text_for_message = f'Привет, {message.from_user.first_name}!'

    if isinstance(message, CallbackQuery):
        text_for_message = f'Привет, {message.from_user.first_name}!'
        message = message.message

    await message.answer(text_for_message, reply_markup=keyboard_user_profile)


@router.callback_query(F.data == 'user_help')
async def create_prj_through_button(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Помощь')
    text = msg_texts.text_for_help_user
    await callback.message.answer(text, reply_markup=to_support_key)


@router.callback_query(F.data == 'user_tg_id')
async def create_prj_through_button(callback: CallbackQuery, state: FSMContext):
    await callback.answer('В процессе... ')
    await get_user_id(message=callback)


@router.message(ChatType(chat_type='private'))
async def help_to_user(message: Message) -> None:
    text = msg_texts.text_for_help_user
    await message.answer(text)
