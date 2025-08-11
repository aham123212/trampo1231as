import asyncio
import os
from pyrogram import Client, idle, enums
from pyrogram.session import Session

from config import API_HASH, API_ID, BOT_TOKEN, WORKERS
from database import db, save

# Inicializa o cliente.
client = Client(
    "bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    workers=WORKERS,
    parse_mode=enums.ParseMode.HTML,
    plugins={"root": "plugins"},
)

# Desativa a mensagem do Pyrogram no início.
Session.notice_displayed = True


async def main():
    try:
        await client.start()
        print("Bot rodando...")
        client.me = await client.get_me()

    except TypeError as e:
        if "'NoneType' object is not subscriptable" in str(e):
            print("\nERRO: Ocorreu um TypeError, que geralmente é causado por um arquivo de sessão corrompido.")
            print("SOLUÇÃO: Apague o arquivo 'bot.session' e reinicie o bot.")
            return
        else:
            raise e
    
    # Adicionando um tratamento para o ValueError que você está vendo
    except ValueError as e:
        print(f"\nERRO DE VALOR: {e}")
        print("Isso geralmente está relacionado a um parâmetro inválido, como o 'parse_mode'.")
        print("Verifique se você está usando 'enums.ParseMode.HTML' na inicialização do cliente.")
        return


    await idle()

    print("\nParando o bot...")
    await client.stop()
    save()
    db.close()


loop = asyncio.get_event_loop()

if __name__ == "__main__":
    try:
        print("Iniciando o bot...")
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\nBot parado pelo usuário.")
    finally:
        if loop.is_running() and not loop.is_closed():
            loop.stop()