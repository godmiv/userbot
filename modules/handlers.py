import json
import os
from telethon import events, types


def register_handlers(client):
    @client.on(events.NewMessage(pattern=r'\.ping', outgoing=True))
    async def ping(event):
        await event.edit('**Pong!** 🏓')

    @client.on(events.NewMessage(pattern=r'\.chats', outgoing=True))
    async def chats(event):
        await event.edit('⌛ Сбор данных...')
        chats_list = []
        async for dialog in client.iter_dialogs():
            entity = dialog.entity
            chat_type = 'Channel' if isinstance(entity, types.Channel) and entity.broadcast else 'Group'
            if isinstance(entity, types.User): chat_type = 'Private'

            chats_list.append({
                'name': dialog.name,
                'id': entity.id,
                'type': chat_type,
                'username': getattr(entity, 'username', None)
            })

        os.makedirs('data', exist_ok=True)
        with open('data/chats_list.json', 'w', encoding='utf-8') as f:
            json.dump(chats_list, f, ensure_ascii=False, indent=4)

        await event.edit(f'✅ Файл `data/chats_list.json` обновлен! ({len(chats_list)} записей)')