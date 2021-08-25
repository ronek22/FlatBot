from crawler import Flat, OtoDom
import requests
import psycopg2
import os
import schedule
from loguru import logger

api = 'https://api.telegram.org/'
bot_token = os.environ['FLATS_TOKEN']
bot_chatID = os.environ['FLATS_CHAT_ID']

def send_message(chat_id, text):
    parameters = {'chat_id': chat_id, 'text': text, 'parse_mode':'markdown'}
    message = requests.post(f"{api}bot{bot_token}/sendMessage", data=parameters)

def fail_criteria(flat: Flat) -> bool:
    if flat.price and int(flat.price[:-2].replace(" ", "")) > 3000:
        logger.info("Price is too high", flat.price)
        return True
    if "zwierz" in flat.description:
        logger.info("Zwierzeta in description", flat.link)
        return True
    if "2022" in flat.description:
        logger.info("Too short rent time", flat.link)
        return True
    logger.success("Awesome offer", flat.link)
    return False

def check_results_send_mess():
    print("Checking new flats...")

    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        flats_db = conn.cursor()
        flats_db.execute('CREATE TABLE IF NOT EXISTS flats (id SERIAL, link TEXT NOT NULL)')
    except Exception as e:
        return send_message(bot_chatID, f'The database could not be accessed\nError code: {e}')
    
    flats = OtoDom()

    for flat in flats:
        if fail_criteria(flat):
            continue
        flat_exists = flats_db.execute(f"SELECT link FROM flats WHERE link='{flat.link}'")
        if len(flats_db.fetchall()) != 1:
            mess_content = flat.print()
            send_message(bot_chatID, mess_content)
            flats_db.execute(f"INSERT INTO flats (link) VALUES ('{flat.link}')")
            conn.commit()
        else:
            continue

    flats_db.close()

schedule.every().hour.do(check_results_send_mess)

# infinte loop
while True:
    schedule.run_pending()


    

    
