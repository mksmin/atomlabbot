# import from libraries
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# buttons to confirm send message
keyboard_send_mess = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отправить', callback_data='send'),
     InlineKeyboardButton(text='Отменить', callback_data='cancel')],

])

keys_for_create_project = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сохранить', callback_data='save_prj'),
     InlineKeyboardButton(text='Отменить', callback_data='cancel_prj')],

])

cancel_key_prj = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отменить', callback_data='cancel_prj')],
])

rpanel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Мои проекты', callback_data='myprojects'),
     InlineKeyboardButton(text='Создать проект', callback_data='create_prj')],
    [InlineKeyboardButton(text='Сообщение в чаты', callback_data='send_msg_fchats'),
     InlineKeyboardButton(text='👮‍♂️ Назначить админа', callback_data='set_user_to_admin')],
    [InlineKeyboardButton(text='📜 Статистика регистраций', callback_data='get_statistics')],
    [InlineKeyboardButton(text='🪪 Профиль пользователя', callback_data='user_profile')],
    [InlineKeyboardButton(text='Создать QR', callback_data='create_qr_code')],
])

keyboard_user_profile = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Помощь', callback_data='user_help'),
     InlineKeyboardButton(text='Задать вопрос', url="tg://resolve?domain=atomlab_help")],
    [InlineKeyboardButton(text='Мой id', callback_data='user_tg_id')],

])

to_support_key = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Задать вопрос', url="tg://resolve?domain=atomlab_help")],
])

manage_projects = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Переключиться на проект', callback_data='switch_project')],
    [InlineKeyboardButton(text='Создать проект', callback_data='create_prj')],
    [InlineKeyboardButton(text='Вернуться в профиль', callback_data='my_profile')]
])

confirm_deletion = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Удалить проект', callback_data='confirm_delete'),
     InlineKeyboardButton(text='Отменить удаление', callback_data='cancel_delete')],
])

return_to_profile = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Создать проект', callback_data='create_prj')],
    [InlineKeyboardButton(text='Вернуться в профиль', callback_data='my_profile')]
])
