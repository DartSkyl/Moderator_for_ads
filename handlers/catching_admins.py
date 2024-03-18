from config_data.config import MAIN_GROUP_ID
from loader import admins_id, dp
from aiogram import F
from aiogram.types import ChatMember
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, ADMINISTRATOR, MEMBER


@dp.chat_member(F.chat.id == MAIN_GROUP_ID,
                ChatMemberUpdatedFilter(
                    member_status_changed=(MEMBER | IS_NOT_MEMBER) >> ADMINISTRATOR)
                )
async def new_administrator(chat_member: ChatMember):
    """Ловим новых администраторов бота только из основной группы"""
    admins_id.append(chat_member.new_chat_member.user.id)


@dp.chat_member(F.chat.id == MAIN_GROUP_ID,
                ChatMemberUpdatedFilter(
                    member_status_changed=(MEMBER | IS_NOT_MEMBER) << ADMINISTRATOR)
                )
async def remove_administrator(chat_member: ChatMember):
    """Удаляем администратора из списка с ID администраторов"""
    admins_id.remove(chat_member.new_chat_member.user.id)
