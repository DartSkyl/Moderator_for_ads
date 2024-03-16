from utils import admin_router, queue_for_publication
from keyboards import (main_admin_keyboard, moderation_keyboard,
                       admin_file_2, admin_back_2, view_queue, edit_public_keyboard)
from states import ModerationAds
from loader import bot

from aiogram.types import Message, FSInputFile
from aiogram import F, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder


async def demonstrate_func(msg: Message, state: FSMContext, ads):
    """Здесь мы показываем одно из объявлений в очереди на публикацию"""
    queue_info = await state.get_data()

    await msg.answer(text=f'Объявление {queue_info["page"]}/{queue_info["count"]}:',
                     reply_markup=view_queue)
    msg_with_time = (f'Время публикации: <b>{ads.public_time}</b>\n'
                     f'Время действия: <b>{ads.validity}</b> суток')
    if ads.file_id:  # Если данный список пуст, значит объявление без медиафайлов
        media_group = MediaGroupBuilder(caption=html.quote(ads.text))
        for mediafile in ads.file_id:
            media_group.add(type=mediafile[1], media=mediafile[0])
        await bot.send_media_group(chat_id=msg.from_user.id, media=media_group.build())

    else:
        await msg.answer(text=html.quote(ads.text))

    await msg.answer(text=msg_with_time)
    await state.set_state(ModerationAds.pub_preview)


@admin_router.message(F.text == '📰 Очередь объявлений на публикацию')
async def view_queue_for_publication(msg: Message, state: FSMContext):
    """Здесь начинается просмотр очереди на публикацию"""
    ads_list = await queue_for_publication.get_ads_list()
    if not isinstance(ads_list, str):
        await state.set_state(ModerationAds.pub_preview)

        await state.set_data({
            'queue': ads_list,
            'page': 1,
            'count': len(ads_list)
        })
        await demonstrate_func(msg=msg, state=state, ads=ads_list[0])
    else:
        await msg.answer(text=ads_list, reply_markup=main_admin_keyboard)


@admin_router.message(ModerationAds.pub_preview, F.text == 'Следующее объявление ▶️')
async def next_ads(msg: Message, state: FSMContext):
    """Здесь мы перелистываем на следующее объявление"""
    queue_info = await state.get_data()
    if queue_info['count'] > queue_info['page']:
        await state.update_data({'page': queue_info['page'] + 1})

        # Номер индекса демонстрируемого объявления равен номеру предыдущей страницы. Так, на всякий случай
        await demonstrate_func(msg=msg, state=state, ads=queue_info['queue'][queue_info['page']])

    else:
        await msg.answer(text='Это конец очереди!')


@admin_router.message(ModerationAds.pub_preview, F.text == '◀️ Предыдущее объявление')
async def previous_ads(msg: Message, state: FSMContext):
    """Здесь мы перелистываем на предыдущее объявление"""
    queue_info = await state.get_data()
    if queue_info['page'] > 1:
        await state.update_data({'page': queue_info['page'] - 1})

        await demonstrate_func(msg=msg, state=state, ads=queue_info['queue'][queue_info['page'] - 2])

    else:
        await msg.answer(text='Это начало очереди!')


@admin_router.message(ModerationAds.pub_preview, F.text == 'Редактировать объявление')
async def edit_public_ads(msg: Message, state: FSMContext):
    """Здесь запускается редактор объявления из очереди на публикацию"""
    queue_info = await state.get_data()
    ads = queue_info['queue'][queue_info['page'] - 1]

    # Сохраним объявление, которое будем редактировать
    await state.update_data({'edit_ads': ads})
    await msg.answer(text='Что редактируем?', reply_markup=edit_public_keyboard)


@admin_router.message(ModerationAds.pub_preview, F.text != 'Вернуться в очередь на публикацию')
async def moderation_text(msg: Message, state: FSMContext):
    """Здесь администратор выбирает действие для модерации"""
    actions = {
        'Редактировать текст': (ModerationAds.pub_text, 'Введите новый текст:', admin_back_2),
        'Редактировать фото/видео': (ModerationAds.pub_mediafile, 'Добавьте фото или видео (до 7 файлов) '
                                                                  'и/или нажмите кнопку "Дальше ▶️"', admin_file_2),
        'Редактировать время публикации': (ModerationAds.pub_time_for_publication, 'Введите время в формате\n'
                                                                                   '<b>11:00 13.03.2024</b>', admin_back_2),
        'Редактировать время действия': (ModerationAds.pub_validity, 'Ведите время действия '
                                                                     'объявления (от 1 до 30 суток)', admin_back_2)
    }

    await state.set_state(actions[msg.text][0])
    await msg.answer(text=actions[msg.text][1], reply_markup=actions[msg.text][2])
    if msg.text == 'Редактировать фото/видео':
        # На случай, если после начала модерации медиафайла, администратор передумает,
        # то вернем файлы на место из backup
        backup = (await state.get_data())['edit_ads'].file_id
        await state.update_data({'backup': backup})
        (await state.get_data())['edit_ads'].file_id = []
        await state.update_data({'mediafile': []})


@admin_router.message(F.text.in_(('Вернуться', '◀️ Вернуться')))
async def back_func(msg: Message, state: FSMContext):
    """Хэндлер возвращает администратора назад в меню модерации"""
    edit_ads = (await state.get_data())['edit_ads']
    if msg.text == '◀️ Вернуться':
        # Так как данная кнопка используется только при модерирование медиафайлов
        # и в этот момент они стираются, то в случае отмены модерации вернем их на место из backup
        backup = (await state.get_data())['backup']
        edit_ads.file_id = backup
    await state.set_state(ModerationAds.pub_preview)
    await demonstrate_func(msg, state, edit_ads)


@admin_router.message(ModerationAds.pub_text)
async def edit_text_func(msg: Message, state: FSMContext):
    """Здесь пользователь корректирует текст объявления"""
    edit_ads = (await state.get_data())['edit_ads']
    edit_ads.text = msg.text
    await msg.answer(text='Текст объявления изменен!')
    await state.set_state(ModerationAds.pub_preview)
    await demonstrate_func(msg, state, edit_ads)


@admin_router.message(ModerationAds.pub_mediafile, F.text != 'Дальше ▶️')
async def edit_mediafile(msg: Message, state: FSMContext):
    """Здесь пользователь редактирует медиафайлы"""
    file_id_list = (await state.get_data())['mediafile']

    if msg.photo:
        file_id_list.append((msg.photo[-1].file_id, 'photo'))
    elif msg.video:
        file_id_list.append((msg.video.file_id, 'video'))

    await state.update_data({'mediafile': file_id_list})


@admin_router.message(ModerationAds.pub_mediafile, F.text == 'Дальше ▶️')
async def edit_mediafile2(msg: Message, state: FSMContext):
    """Здесь медиафайлы перезаписываются"""
    file_id_list = (await state.get_data())['mediafile']
    edit_ads = (await state.get_data())['edit_ads']
    # смотрим, что бы файлов было не больше разрешенного
    if len(file_id_list) > 7:
        await msg.answer(text='Фалов слишком много, повторите попытку', reply_markup=admin_file_2)
        await state.update_data({'mediafile': []})
    else:
        edit_ads.file_id = file_id_list
        await msg.answer(text='Фото/Видео изменено!')
        await state.set_state(ModerationAds.pub_preview)
        await demonstrate_func(msg, state, edit_ads)


@admin_router.message(ModerationAds.pub_time_for_publication, F.text.regexp(r'\d{1,2}[:]\d{2}\s\d{1,2}.\d{1,2}.\d{4}$'))
async def edit_time_for_publication(msg: Message, state: FSMContext):
    """Здесь пользователь редактирует желаемое время публикации"""
    edit_ads = (await state.get_data())['edit_ads']
    edit_ads.public_time = msg.text
    await state.set_state(ModerationAds.pub_preview)
    await demonstrate_func(msg, state, edit_ads)


@admin_router.message(ModerationAds.pub_validity, F.text.regexp(r'\d{1,2}'))
async def edit_validity(msg: Message, state: FSMContext):
    """Здесь пользователь редактирует желаемое время действия объявления"""
    if 1 <= int(msg.text) <= 30:
        edit_ads = (await state.get_data())['edit_ads']
        edit_ads.public_time = int(msg.text)
        await state.set_state(ModerationAds.pub_preview)
        await demonstrate_func(msg, state, edit_ads)
    else:
        await msg.answer(text='Неверный ввод! Допустимо от 1 до 30 суток. Повторите попытку')
