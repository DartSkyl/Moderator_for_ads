import datetime
from utils import admin_router, queue_for_moderation, queue_for_publication
from keyboards import main_admin_keyboard, moderation_keyboard, admin_file, admin_back, channel_mang, rm_channel_keys
from states import ModerationAds
from loader import bot, db

from aiogram.types import Message, CallbackQuery
from aiogram import F, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder


async def moderation_func(msg: Message, state: FSMContext):
    ads_items = await state.get_data()
    ads_count = await queue_for_moderation.get_quantity()
    await msg.answer(text=f'Объявление для модерации\n(всего объявлений в очереди {ads_count}):',
                     reply_markup=moderation_keyboard, parse_mode='HTML')
    msg_with_time = f'Желаемое время публикации: <b>{ads_items["public_time"]}</b>\n'
    if ads_items['mediafile']:  # Если данный список пуст, значит объявление без медиафайлов
        media_group = MediaGroupBuilder(caption=ads_items['text'])
        for mediafile in ads_items['mediafile']:
            media_group.add(type=mediafile[1], media=mediafile[0])
        await bot.send_media_group(chat_id=msg.from_user.id, media=media_group.build())

    else:
        await msg.answer(text=ads_items['text'])
    if ads_items['public_time'] != 'None':
        await msg.answer(text=msg_with_time, parse_mode='HTML')
    await state.set_state(ModerationAds.mod_preview)


@admin_router.message(Command('start'))
async def start_function(msg: Message, state: FSMContext):
    """Функция запускается при старте бота и вводе соответствующей команды от имени администратора"""
    await state.clear()
    await msg.answer(
        text=f'Привет, {html.quote(msg.from_user.first_name)}!\nЖду ваших решений😉',
        reply_markup=main_admin_keyboard, parse_mode='HTML'
    )


@admin_router.message(F.text == '📋 Очередь объявлений на модерацию')
async def view_queue_for_moderation(msg: Message, state: FSMContext):
    """Здесь начинается просмотр очереди на модерацию"""
    # Данный метод всегда (если только там не пусто) возвращает первое объявление в списке!
    ads = await queue_for_moderation.get_ads_from_queue()
    if isinstance(ads, str):
        await msg.answer(text=ads, reply_markup=main_admin_keyboard, parse_mode='HTML')
        await state.clear()
    else:
        await state.set_state(ModerationAds.mod_preview)
        await state.set_data({
            'container_id': ads.container_id,
            'text': ads.text,
            'user_id': ads.user_id,
            'mediafile': ads.file_id,
            'public_time': ads.public_time,
            'public_channel': ads.public_channel
        })
        await moderation_func(msg=msg, state=state)


@admin_router.message(ModerationAds.mod_preview, F.text == 'Отправить на публикацию')
async def send_to_publication_queue(msg: Message, state: FSMContext):
    """Здесь объявление отправляется на публикацию"""
    ads_items = await state.get_data()
    await queue_for_publication.add_ads_in_queue(
        container_id=ads_items['container_id'],
        text=ads_items['text'],
        user_id=ads_items['user_id'],
        mediafile=ads_items['mediafile'],
        public_time=ads_items['public_time'],
        public_channel=ads_items['public_channel'],
        time_index=int(datetime.datetime.strptime(ads_items['public_time'], "%H:%M %d.%m.%Y").timestamp())
        if ads_items['public_time'] != 'None' else None
    )
    await queue_for_moderation.remove_ads_from_queue(container_id=ads_items['container_id'])
    await db.remove_ads_mod(container_id=ads_items['container_id'])
    await msg.answer(text='Объявление отправлено на публикацию')
    await view_queue_for_moderation(msg, state)


@admin_router.message(ModerationAds.mod_preview, F.text == 'Отказать в публикации')
async def refuse_publication(msg: Message, state: FSMContext):
    """Здесь администратор отказывает в публикации"""
    await msg.answer(text='Введите комментарий к отказу:', reply_markup=admin_back, parse_mode='HTML')
    await state.set_state(ModerationAds.mod_refuse)


@admin_router.message(ModerationAds.mod_refuse, F.text != 'Назад')
async def send_comment(msg: Message, state: FSMContext):
    """Здесь мы отправляем владельцу объявления сообщение об отказе и комментарий"""
    user_id = (await state.get_data())['user_id']
    ads_id = (await state.get_data())['container_id']
    await queue_for_moderation.remove_ads_from_queue(container_id=ads_id)
    standard_text = 'Вым было отказано в публикации объявления по причине:\n'
    await bot.send_message(chat_id=user_id, text=(standard_text + msg.text), parse_mode='HTML')
    await msg.answer(text='Сообщение отправлено')
    await view_queue_for_moderation(msg, state)


@admin_router.message(ModerationAds.mod_preview, F.text != 'Вернуться в главное меню')
async def moderation_text(msg: Message, state: FSMContext):
    """Здесь администратор выбирает действие для модерации"""
    actions = {
        'Редактировать текст': (ModerationAds.mod_text, 'Введите новый текст\n❗Все ссылки вводить только прямым адресом❗\nПример: https://yandex.ru', admin_back),
        'Редактировать фото/видео': (ModerationAds.mod_mediafile, 'Добавьте фото или видео (до 7 файлов) '
                                                                  'и/или нажмите кнопку "Дальше ▶️"', admin_file),
        'Редактировать время публикации': (ModerationAds.mod_time_for_publication, 'Введите время в формате\n'
                                                                                   f'<b>{datetime.datetime.now().strftime("%H:%M %d.%m.%Y")}</b>', admin_back)
    }

    await state.set_state(actions[msg.text][0])
    await msg.answer(text=actions[msg.text][1], reply_markup=actions[msg.text][2], parse_mode='HTML')
    if msg.text == 'Редактировать фото/видео':
        # На случай, если после начала модерации медиафайла, администратор передумает,
        # то вернем файлы на место из backup
        backup = (await state.get_data())['mediafile']
        await state.update_data({'backup': backup})
        await state.update_data({'mediafile': []})


@admin_router.message(F.text.in_(('Назад', '◀️ Назад')))
async def back_func(msg: Message, state: FSMContext):
    """Хэндлер возвращает администратора назад в меню модерации"""
    if msg.text == '◀️ Назад':
        # Так как данная кнопка используется только при модерирование медиафайлов
        # и в этот момент они стираются, то в случае отмены модерации вернем их на место из backup
        backup = (await state.get_data())['backup']
        await state.update_data({'mediafile': backup})
    await state.set_state(ModerationAds.mod_preview)
    await moderation_func(msg, state)


@admin_router.message(ModerationAds.mod_text)
async def edit_text_func(msg: Message, state: FSMContext):
    """Здесь пользователь корректирует текст объявления"""
    if len(msg.text) > 1000:
        await msg.answer(f'Ограничение для объявления 1000 символов '
                         f'(Вы ввели {len(msg.text)} символа).\nПопробуйте еще раз', parse_mode='HTML')
    else:
        await state.update_data({'text': msg.md_text})
        await msg.answer(text='Текст объявления изменен!', parse_mode='HTML')
        await state.set_state(ModerationAds.mod_preview)
        await moderation_func(msg, state)


@admin_router.message(ModerationAds.mod_mediafile, F.text != 'Дальше ▶️')
async def edit_mediafile(msg: Message, state: FSMContext):
    """Здесь пользователь редактирует медиафайлы"""
    file_id_list = (await state.get_data())['mediafile']

    if msg.photo:
        file_id_list.append((msg.photo[-1].file_id, 'photo'))
    elif msg.video:
        file_id_list.append((msg.video.file_id, 'video'))

    await state.update_data({'mediafile': file_id_list})


@admin_router.message(ModerationAds.mod_mediafile, F.text == 'Дальше ▶️')
async def edit_mediafile2(msg: Message, state: FSMContext):
    """Здесь медиафайлы перезаписываются"""
    file_id_list = (await state.get_data())['mediafile']
    # смотрим, что бы файлов было не больше разрешенного
    if len(file_id_list) > 7:
        await msg.answer(text='Фалов слишком много, повторите попытку', reply_markup=admin_file, parse_mode='HTML')
        await state.update_data({'mediafile': []})
    else:
        await msg.answer(text='Фото/Видео изменено!', parse_mode='HTML')
        await state.set_state(ModerationAds.mod_preview)
        await moderation_func(msg, state)


@admin_router.message(ModerationAds.mod_time_for_publication, F.text.regexp(r'\d{1,2}[:]\d{2}\s\d{1,2}.\d{1,2}.\d{4}$'))
async def edit_time_for_publication(msg: Message, state: FSMContext):
    """Здесь пользователь редактирует желаемое время публикации"""
    await state.update_data({'public_time': msg.text})
    await state.set_state(ModerationAds.mod_preview)
    await moderation_func(msg, state)


@admin_router.message(F.text == 'Вернуться в главное меню')
async def return_to_the_main_menu(msg: Message, state: FSMContext):
    """Хэндлер возвращает администратора в главное меню"""
    await msg.answer(text='Возврат в главное меню', reply_markup=main_admin_keyboard)
    await state.clear()


# ====================
# Управление каналами для публикаций
# ====================


@admin_router.message(F.text == '📣 Каналы для публикаций')
async def channels_menu(msg: Message):
    """Начинаем добавление канала для публикации"""
    await msg.answer('Выберете действие:', reply_markup=channel_mang)


@admin_router.message(F.text == 'Добавить канал')
async def adding_channels_start(msg: Message, state: FSMContext):
    """Начинаем добавление канала для публикации"""
    await state.set_state(ModerationAds.add_channel)
    await msg.answer('Перешлите сюда сообщение из канала который хотите добавить')


@admin_router.message(ModerationAds.add_channel)
async def catch_new_channel(msg: Message, state: FSMContext):
    """Ловим пересланное сообщение из добавляемого канала"""
    if msg.forward_from_chat:
        await db.add_new_channel(msg.forward_from_chat.id, msg.forward_from_chat.title)
        await state.clear()
        await msg.answer('Канал добавлен', reply_markup=main_admin_keyboard)


@admin_router.message(F.text == 'Удалить канал')
async def open_remove_menu(msg: Message):
    """Открываем меню для удаления каналов"""
    all_channels = await db.get_channels()
    await msg.answer('Выберете канал для удаления:', reply_markup=await rm_channel_keys(all_channels))


@admin_router.callback_query(F.data.startswith('rm_id_'))
async def remove_channel_func(callback: CallbackQuery):
    """Удаляем канал для публикации"""
    await callback.answer()
    await db.remove_channel(int(callback.data.replace('rm_id_', '')))
    await callback.message.answer('Канал удален', reply_markup=main_admin_keyboard)
