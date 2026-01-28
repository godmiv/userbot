from telethon import TelegramClient, errors


async def get_client(api_id, api_hash, phone):
    client = TelegramClient('my_session', api_id, api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone)
            code = input(f'Введите код подтверждения для {phone}: ')
            await client.sign_in(phone, code)
        except errors.SessionPasswordNeededError:
            password = input('Обнаружена 2FA. Введите ваш облачный пароль: ')
            await client.sign_in(password=password)
        except Exception as e:
            print(f"Ошибка при входе: {e}")
            return None

    return client