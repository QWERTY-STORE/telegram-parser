import csv
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipants
from telethon.tl.types import ChannelParticipantsSearch


#   Сюда нужно вставить API ID и API HASH c сайта https://my.telegram.org/auth
api_id = ''
api_hash = ''
phone = ''


#   Имя файла сессии
session_name = 'session_name'


#   Инициализация клиента
client = TelegramClient(session_name, api_id, api_hash)


async def main():
    #   Подключение к аккаунту
    await client.start(phone)
    print('Connected to account')

    #   Указывает ссылку на группу или канал
    group_link = 'https://t.me/Kali_Linux_Pentest'
    entity = await client.get_entity(group_link)


    #   Получение всех участников группы
    all_participants = []

    offset = 0
    litim = 100

    while True:
        participants = await client(GetParticipants(
            entity, ChannelParticipantsSearch(''), offset, litim,))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset += len(participants.users)

    #  Запись всех участников в файл
    with open('participants.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Username', 'First Name', 'Last Name', 'Phone'])   # Заголовок столбцов
        for participant in all_participants:
            writer.writerow([participant.ID, participant.username, participant.firstname, participant.lastname, participant.phone])

    
    print(f"Всего участников: {len(all_participants)}")


with client:
    client.loop.run_until_complete(main())