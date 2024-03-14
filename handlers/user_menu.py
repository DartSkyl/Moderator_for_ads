import asyncio
from utils import users_router, queue_for_moderation, ContainerForAds, editing_function
from keyboards import main_user_keyboard, user_cancel, preview_keyboard, user_file
from states import CreatingAds
from loader import bot

from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram import F, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from asyncpg.exceptions import UniqueViolationError
from aiogram.utils.media_group import MediaGroupBuilder


@users_router.message(Command('start'))
async def start_function(msg: Message):
    """Функция запускается при старте бота и вводе соответствующей команды от имени пользователя"""
    await msg.answer(text=f'Привет, {html.quote(msg.from_user.first_name)}!\nЖду твоих объявлений😉',
                     reply_markup=main_user_keyboard)


@users_router.message(F.text == '📝 Создать объявление')
async def started_creating_ads(msg: Message, state: FSMContext):
    """Данный хэндлер запускает создание объявления"""
    await state.set_state(CreatingAds.adding_text)
    await msg.answer(text='Введите текст будущего объявления (максимум 1024 символа):',
                     reply_markup=user_cancel)


# @users_router.callback_query(CreatingAds.start_creating)
# async def adding_text(callback: CallbackQuery, state: FSMContext):
#     """Здесь происходит добавления текста в объявление пользователем"""
#     await callback.answer()
#     await callback.message.delete()
#
#     content_type_dict = {'text': '3000', 'photo': '1000', 'video': '1000'}
#
#     if callback.data != 'cancel':
#         await callback.message.answer(text=f'Введите текст объявления '
#                                            f'(максимум {content_type_dict[callback.data]} символов)',
#                                       reply_markup=user_cancel)
#
#         await state.set_state(CreatingAds.adding_text)
#         await state.set_data({'content_type': callback.data, 'user_id': callback.from_user.id})
#
#     else:
#         await callback.message.answer(text='Действие отменено', reply_markup=main_user_keyboard)
#         await state.clear()


@users_router.message(CreatingAds.adding_text, F.text != '🚫 Отмена')
async def adding_time_or_file(msg: Message, state: FSMContext):
    """Здесь сохраняется текст, а далее либо вводится время публикации, либо добавляются файлы"""

    # content_type = (await state.get_data())['content_type']  # Сразу выгрузим выбор пользователя
    # content_type_dict = {'text': 3000, 'photo': 1000, 'video': 1000}

    # Сразу проверяем корректность длинны сообщения
    if len(msg.text) > 1024:
        await state.set_state(CreatingAds.false_state)  # Это нужно для того, что бы когда телеграмм разобьет
        # сообщение на две части не пропустить второе
        await msg.answer(f'Ограничение для объявления 1024 символов '
                         f'(Вы ввели {len(msg.text)} символа).\nПопробуйте еще раз')
        await asyncio.sleep(1)
        await state.set_state(CreatingAds.adding_text)  # И сразу установим стэйт обратно,
        # что бы пользователь мог повторить ввод текста для публикации

    else:
        #
        # if content_type == 'text':
        #     await msg.answer(text="Теперь введите желаемое время и дату для публикации в следующем формате:\n"
        #                           "<b>11:00 13.03.2024</b>\n\n"
        #                           "❗Учтите, что модератор может изменить данное время! Особенно, "
        #                           "если к моменту прохождения модерации данное время и дата уже истекут❗",
        #                      reply_markup=user_cancel)
        #     await state.set_state(CreatingAds.time_for_publication)

        # elif content_type in ['photo', 'video']:
        # await msg.answer(text='Теперь скиньте фото (до 7), после чего нажмите кнопку "Дальше ▶️"'
        #                  if content_type == 'photo'
        #                  else 'Теперь скиньте видео (до 7), после чего нажмите кнопку "Дальше ▶️"')
        await msg.answer(text='Теперь скиньте фото или видео (до 7 файлов) и/или нажмите кнопку "Дальше ▶️"',
                         reply_markup=user_file)
        await state.set_state(CreatingAds.adding_mediafile)
        await state.update_data({'mediafile': []})

        await state.update_data({'text': msg.text, 'user_id': msg.from_user.id})


@users_router.message(CreatingAds.adding_mediafile, F.text != 'Дальше ▶️')
async def mediafile_input(msg: Message, state: FSMContext):
    """Здесь пользователь добавляет медиафайлы"""
    # content_type = (await state.get_data())['content_type']

    # Так как, при скидывании более одного файла, бот воспринимает это как сразу несколько отдельных
    # сообщений, то будем использовать эту причудливую конструкцию с заранее созданным списком

    file_id_list = (await state.get_data())['mediafile']

    if msg.photo:
        file_id_list.append((msg.photo[-1].file_id, 'photo'))
    elif msg.video:
        file_id_list.append((msg.video.file_id, 'video'))

    await state.update_data({'mediafile': file_id_list})


@users_router.message(CreatingAds.adding_mediafile, F.text == 'Дальше ▶️')
async def end_mediafile_input(msg: Message, state: FSMContext):
    """Здесь заканчиваем ловлю файлов и переходим к установке времени публикации"""
    file_id_list = (await state.get_data())['mediafile']
    # смотрим, что бы файлов было не больше разрешенного
    if len(file_id_list) > 7:
        await msg.answer(text='Фалов слишком много, повторите попытку', reply_markup=user_file)
        await state.update_data({'mediafile': []})
    else:
        await msg.answer(text="Теперь введите желаемое время и дату для публикации в следующем формате:\n"
                              "<b>11:00 13.03.2024</b>\n\n"
                              "❗Учтите, что модератор может изменить данное время! Особенно, "
                              "если к моменту прохождения модерации данное время и дата уже истекут❗",
                         reply_markup=user_cancel)
        await state.set_state(CreatingAds.time_for_publication)


@users_router.message(CreatingAds.time_for_publication,
                      F.text.regexp(r'\d{1,2}[:]\d{2}\s\d{1,2}.\d{1,2}.\d{4}$'), F.text != '🚫 Отмена')
async def setting_the_desired_time(msg: Message, state: FSMContext):
    """Здесь происходит установка желаемого времени и даты публикации"""
    await state.update_data({'public_time': msg.text})
    await msg.answer(text='Теперь введите срок действия объявления (от 1 до 30 суток)', reply_markup=user_cancel)
    await state.set_state(CreatingAds.validity)


@users_router.message(CreatingAds.time_for_publication)
async def time_error_input(msg: Message):
    """Хэндлер неверного ввода времени публикации"""
    await msg.answer(text='Неверный формат времени или даты!\nПовторите попытку\n'
                          'Необходимый формат <b>11:00 13.03.2024</b>')


@users_router.message(CreatingAds.validity, F.text.regexp(r'\d{1,2}'))
async def validity_input(msg: Message, state: FSMContext):
    """Здесь пользователь вводит желаемый срок действия объявления"""
    if 1 <= int(msg.text) <= 30:
        await state.update_data({'validity': int(msg.text)})
        ads_items = await state.get_data()

        await msg.answer(text='Предпросмотр:', reply_markup=preview_keyboard)
        msg_with_time = (f'Желаемое время публикации: <b>{ads_items["public_time"]}</b>\n'
                         f'Желаемое время действия: <b>{msg.text}</b>')
        if len(ads_items['mediafile']) > 0:
            media_group = MediaGroupBuilder(caption=ads_items['text'])
            for mediafile in ads_items['mediafile']:
                media_group.add(type=mediafile[1], media=mediafile[0])
            await bot.send_media_group(chat_id=msg.from_user.id, media=media_group.build())

        else:
            await msg.answer(text=ads_items['text'])

        await msg.answer(text=msg_with_time)
        await state.set_state(CreatingAds.preview)

        # ads = ContainerForAds(
        #     text=ads_items['text'],
        #     user_id=ads_items['user_id'],
        #     public_time=ads_items['public_time'],
        #     validity=int(msg.text),
        #     file_id=ads_items['mediafile'] if len(ads_items['mediafile']) > 0 else None
        # )
        # # Здесь будет предпросмотр
        # await editing_function(ads=ads, from_user_id=msg.from_user.id)

        # ads_items = await state.get_data()
        # await queue_for_moderation.add_ads_in_queue(
        #     user_id=ads_items['user_id'],
        #     text=ads_items['text'],
        #     mediafile=ads_items['mediafile'],
        #     public_time=ads_items['public_time'],
        #     validity=ads_items['validity']
        # )
        # await msg.answer(text='Объявление отправлено на модерацию!', reply_markup=main_user_keyboard)


@users_router.message(F.text == 'Отправить на модерацию')
async def send_ads_for_moderation(msg: Message, state: FSMContext):
    """Здесь мы отправляем созданное объявление на модерацию"""
    ads_items = await state.get_data()
    await queue_for_moderation.add_ads_in_queue(
        user_id=ads_items['user_id'],
        text=ads_items['text'],
        mediafile=ads_items['mediafile'],
        public_time=ads_items['public_time'],
        validity=ads_items['validity']
    )
    await msg.answer(text='Объявление отправлено на модерацию!', reply_markup=main_user_keyboard)


@users_router.message(F.text == 'Удалить объявление')
async def delete_created_ads(msg: Message, state: FSMContext):
    """Данный хэндлер удаляет только что созданное объявление"""
    await msg.answer(text='Объявление удалено!', reply_markup=main_user_keyboard)
    await state.clear()


@users_router.message(CreatingAds.preview)
async def action_after_preview(msg: Message, state: FSMContext):
    """Здесь пользователь выбирает действие для редактирования"""
    actions = {
        'Редактировать текст': (CreatingAds.adding_text, 'Введите новый текст:'),
        'Редактировать фото': (CreatingAds.edit_mediafile, 'Добавьте фото или видео (до 7 файлов) '
                                                           'и/или нажмите кнопку "Дальше ▶️"', user_file),
        'Редактировать время публикации': (CreatingAds.edit_time_for_publication, 'Введите желаемое время в формате\n'
                                                                                  '<b>11:00 13.03.2024</b>'),
        'Редактировать время действия': (CreatingAds.edit_validity, 'Ведите желаемое время действия '
                                                                    'объявления (от 1 до 30 суток)'),
    }

    await state.set_state(actions[msg.text][0])
    await msg.answer(text=actions[msg.text][1], reply_markup=actions[msg.text][2] if actions[msg.text][2] else None)


@users_router.message(F.text == '🚫 Отмена')
async def cancel(msg: Message, state: FSMContext):
    """Кнопка отмены"""
    await msg.answer(text='Действие отменено', reply_markup=main_user_keyboard)
    await state.clear()
