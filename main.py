import configparser
import asyncio
import logging
import sys

# Импортируем наши модули
from modules.auth import get_client
from modules.handlers import register_handlers

logging.basicConfig(level=logging.WARNING)


async def main():
    config = configparser.ConfigParser()
    config.read("config.ini")

    try:
        api_id = int(config['Telegram']['api_id'])
        api_hash = config['Telegram']['api_hash']
        phone = config['Telegram']['phone_number']
    except KeyError as e:
        print(f"Ошибка в config.ini: не найдено поле {e}")
        return

    print("--- Запуск юзербота ---")
    client = await get_client(api_id, api_hash, phone)

    if client:
        register_handlers(client)
        print("Статус: Работает. Нажмите Ctrl+C для остановки.")
        await client.run_until_disconnected()
    else:
        print("Не удалось инициализировать клиент. Проверьте данные.")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nБот остановлен вручную.")
        sys.exit(0)