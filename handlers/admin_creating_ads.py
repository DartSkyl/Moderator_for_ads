import asyncio
from random import choices
import string
from utils import admin_router, queue_for_publication
from keyboards import (main_admin_keyboard, moderation_keyboard, admin_cancel, admin_file, admin_back,
                       admin_file_2, admin_back_2, view_queue, edit_public_keyboard, admin_preview_keyboard)
from states import AdminCreated
from loader import bot

from aiogram.types import Message, FSInputFile
from aiogram import F, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder


async def preview_func(msg: Message, state: FSMContext):
    ads_items = await state.get_data()

    await msg.answer(text='Предпросмотр:', reply_markup=admin_preview_keyboard)
    msg_with_time = (f'Время публикации: <b>{ads_items["public_time"]}</b>\n'
                     f'Время действия: <b>{ads_items["validity"]}</b> суток')
    if len(ads_items['mediafile']) > 0:  # Если данный список пуст, значит объявление без медиафайлов
        media_group = MediaGroupBuilder(caption=html.quote(ads_items['text']))
        for mediafile in ads_items['mediafile']:
            media_group.add(type=mediafile[1], media=mediafile[0])
        await bot.send_media_group(chat_id=msg.from_user.id, media=media_group.build())

    else:
        await msg.answer(text=html.quote(ads_items['text']))

    await msg.answer(text=msg_with_time)
    await state.set_state(AdminCreated.preview)


@admin_router.message(F.text == '📝 Создать пост')
async def started_creating_ads(msg: Message, state: FSMContext):
    """Данный хэндлер запускает создание объявления"""
    await state.set_state(AdminCreated.adding_text)
    await msg.answer(text='Введите текст будущего объявления (максимум 1024 символа):',
                     reply_markup=admin_cancel)


@admin_router.message(AdminCreated.adding_text, F.text != '🚫 Отмена')
async def adding_time_or_file(msg: Message, state: FSMContext):
    """Здесь сохраняется текст, а далее либо вводится время публикации, либо добавляются файлы"""

    # Сразу проверяем корректность длинны сообщения
    if len(msg.text) > 1024:
        await state.set_state(AdminCreated.false_state)  # Это нужно для того, что бы когда телеграмм разобьет
        # сообщение на две части не пропустить второе
        await msg.answer(f'Ограничение для объявления 1024 символов '
                         f'(Вы ввели {len(msg.text)} символа).\nПопробуйте еще раз')
        await asyncio.sleep(1)
        await state.set_state(AdminCreated.adding_text)  # И сразу установим стэйт обратно,
        # что бы пользователь мог повторить ввод текста для публикации

    else:
        await msg.answer(text='Теперь скиньте фото или видео (до 7 файлов) и/или нажмите кнопку "Дальше ▶️"',
                         reply_markup=admin_file)
        await state.set_state(AdminCreated.adding_mediafile)
        await state.update_data({'mediafile': []})

        await state.update_data({'text': msg.text, 'user_id': msg.from_user.id})


@admin_router.message(AdminCreated.adding_mediafile, F.text != 'Дальше ▶️')
async def mediafile_input(msg: Message, state: FSMContext):
    """Здесь пользователь добавляет медиафайлы"""

    # Так как, при скидывании более одного файла, бот воспринимает это как сразу несколько отдельных
    # сообщений, то будем использовать эту причудливую конструкцию с заранее созданным списком

    file_id_list = (await state.get_data())['mediafile']

    if msg.photo:
        file_id_list.append((msg.photo[-1].file_id, 'photo'))
    elif msg.video:
        file_id_list.append((msg.video.file_id, 'video'))

    await state.update_data({'mediafile': file_id_list})


@admin_router.message(AdminCreated.adding_mediafile, F.text == 'Дальше ▶️')
async def end_mediafile_input(msg: Message, state: FSMContext):
    """Здесь заканчиваем ловлю файлов и переходим к установке времени публикации"""
    file_id_list = (await state.get_data())['mediafile']
    # смотрим, что бы файлов было не больше разрешенного
    if len(file_id_list) > 7:
        await msg.answer(text='Фалов слишком много, повторите попытку', reply_markup=admin_file)
        await state.update_data({'mediafile': []})
    else:
        await msg.answer(text="Теперь введите время и дату для публикации в следующем формате:\n"
                              "<b>11:00 13.03.2024</b>\n\n",
                         reply_markup=admin_cancel)
        await state.set_state(AdminCreated.time_for_publication)


@admin_router.message(AdminCreated.time_for_publication,
                      F.text.regexp(r'\d{1,2}[:]\d{2}\s\d{1,2}.\d{1,2}.\d{4}$'))
async def setting_the_desired_time(msg: Message, state: FSMContext):
    """Здесь происходит установка желаемого времени и даты публикации"""
    await state.update_data({'public_time': msg.text})
    await msg.answer(text='Теперь введите срок действия объявления (от 1 до 30 суток)', reply_markup=admin_cancel)
    await state.set_state(AdminCreated.validity)


@admin_router.message(AdminCreated.time_for_publication, F.text != '🚫 Отмена')
async def time_error_input(msg: Message):
    """Хэндлер неверного ввода времени публикации"""
    await msg.answer(text='Неверный формат времени или даты!\nПовторите попытку\n'
                          'Необходимый формат <b>11:00 13.03.2024</b>')


@admin_router.message(AdminCreated.validity, F.text.regexp(r'\d{1,2}'))
async def validity_input(msg: Message, state: FSMContext):
    """Здесь пользователь вводит желаемый срок действия объявления"""
    if 1 <= int(msg.text) <= 30:
        await state.update_data({'validity': int(msg.text)})
        await state.set_state(AdminCreated.preview)
        await preview_func(msg, state)
    else:
        await msg.answer(text='Неверный ввод! Допустимо от 1 до 30 суток. Повторите попытку')


@admin_router.message(AdminCreated.preview, F.text == 'Отправить на публикацию')
async def send_to_publication_queue(msg: Message, state: FSMContext):
    """Здесь объявление отправляется на публикацию"""
    ads_items = await state.get_data()
    generate_id = ''.join(choices(string.digits + string.ascii_letters, k=8))
    await queue_for_publication.add_ads_in_queue(
        container_id=generate_id,
        text=ads_items['text'],
        user_id=ads_items['user_id'],
        mediafile=ads_items['mediafile'],
        public_time=ads_items['public_time'],
        validity=ads_items['validity']
    )
    await msg.answer(text='Объявление отправлено на публикацию', reply_markup=main_admin_keyboard)
    await state.clear()


@admin_router.message(F.text == 'Удалить объявление')
async def delete_created_ads(msg: Message, state: FSMContext):
    """Данный хэндлер удаляет только что созданное объявление"""
    await msg.answer(text='Объявление удалено!', reply_markup=main_admin_keyboard)
    await state.clear()


@admin_router.message(AdminCreated.preview)
async def action_after_preview(msg: Message, state: FSMContext):
    """Здесь пользователь выбирает действие для редактирования"""
    actions = {
        'Редактировать текст': (AdminCreated.edit_text, 'Введите новый текст:', admin_back),
        'Редактировать фото/видео': (AdminCreated.edit_mediafile, 'Добавьте фото или видео (до 7 файлов) '
                                                                  'и/или нажмите кнопку "Дальше ▶️"', admin_file_2),
        'Редактировать время публикации': (AdminCreated.edit_time_for_publication, 'Введите желаемое время в формате\n'
                                                                                   '<b>11:00 13.03.2024</b>',
                                           admin_back),
        'Редактировать время действия': (AdminCreated.edit_validity, 'Ведите желаемое время действия '
                                                                     'объявления (от 1 до 30 суток)', admin_back),
    }

    await state.set_state(actions[msg.text][0])
    await msg.answer(text=actions[msg.text][1], reply_markup=actions[msg.text][2])
    if msg.text == 'Редактировать фото/видео':
        # На случай, если после начала модерации медиафайла, пользователь передумает,
        # то вернем файлы на место из backup
        backup = (await state.get_data())['mediafile']
        await state.update_data({'backup': backup})
        await state.update_data({'mediafile': []})


@admin_router.message(F.text.in_(('Назад', '◀️ Назад')))
async def back_func(msg: Message, state: FSMContext):
    """Хэндлер возвращает администратора назад в меню модерации"""
    if msg.text == '◀️ Назад':
        # Так как данная кнопка используется только при редактировании медиафайлов
        # и в этот момент они стираются, то в случае отмены редактирования вернем их на место из backup
        backup = (await state.get_data())['backup']
        await state.update_data({'mediafile': backup})
    await state.set_state(AdminCreated.preview)
    await preview_func(msg, state)


@admin_router.message(AdminCreated.edit_text)
async def edit_text_func(msg: Message, state: FSMContext):
    """Здесь пользователь корректирует текст объявления"""
    await state.update_data({'text': msg.text})
    await msg.answer(text='Текст объявления изменен!')
    await state.set_state(AdminCreated.preview)
    await preview_func(msg, state)


@admin_router.message(AdminCreated.edit_mediafile, F.text != 'Дальше ▶️')
async def edit_mediafile(msg: Message, state: FSMContext):
    """Здесь пользователь редактирует медиафайлы"""
    file_id_list = (await state.get_data())['mediafile']

    if msg.photo:
        file_id_list.append((msg.photo[-1].file_id, 'photo'))
    elif msg.video:
        file_id_list.append((msg.video.file_id, 'video'))

    await state.update_data({'mediafile': file_id_list})


@admin_router.message(AdminCreated.edit_mediafile, F.text == 'Дальше ▶️')
async def edit_mediafile2(msg: Message, state: FSMContext):
    """Здесь медиафайлы перезаписываются"""
    file_id_list = (await state.get_data())['mediafile']
    # смотрим, что бы файлов было не больше разрешенного
    if len(file_id_list) > 7:
        await msg.answer(text='Фалов слишком много, повторите попытку', reply_markup=admin_file_2)
        await state.update_data({'mediafile': []})
    else:
        await msg.answer(text='Фото/Видео изменено!')
        await state.set_state(AdminCreated.preview)
        await preview_func(msg, state)


@admin_router.message(AdminCreated.edit_time_for_publication, F.text.regexp(r'\d{1,2}[:]\d{2}\s\d{1,2}.\d{1,2}.\d{4}$'))
async def edit_time_for_publication(msg: Message, state: FSMContext):
    """Здесь пользователь редактирует желаемое время публикации"""
    await state.update_data({'public_time': msg.text})
    await state.set_state(AdminCreated.preview)
    await preview_func(msg, state)


@admin_router.message(AdminCreated.edit_validity, F.text.regexp(r'\d{1,2}'))
async def edit_validity(msg: Message, state: FSMContext):
    """Здесь пользователь редактирует желаемое время действия объявления"""
    if 1 <= int(msg.text) <= 30:
        await state.update_data({'validity': int(msg.text)})
        await state.set_state(AdminCreated.preview)
        await preview_func(msg, state)
    else:
        await msg.answer(text='Неверный ввод! Допустимо от 1 до 30 суток. Повторите попытку')


@admin_router.message(F.text == '🚫 Отмена')
async def cancel(msg: Message, state: FSMContext):
    """Кнопка отмены"""
    await msg.answer(text='Действие отменено', reply_markup=main_admin_keyboard)
    await state.clear()