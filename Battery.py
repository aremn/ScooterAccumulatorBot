import random
import hashlib
from telethon.sync import TelegramClient
from telethon.errors import RPCError
import time
from database import setup_db, add_user, get_user, update_user_data

setup_db()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def register_new_user():
    username = input("Enter a new username: ")
    password = input("Enter a password: ")
    hashed_password = hash_password(password)
    add_user(username, hashed_password)
    print(f"User {username} registered!")


def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    hashed_password = hash_password(password)

    user_data = get_user(username)
    if not user_data or user_data[2] != hashed_password:
        print("Incorrect username or password!")
        return None

    if not user_data[3]:  # Check if app_id is not set
        app_id = input("Enter your app_id: ")
        app_hash = input("Enter your app_hash: ")
        phone = input("Enter your phone number (with country code, e.g., +1234567890): ")
        session_file = f"session_{username}"
        update_user_data(username, app_id, app_hash, phone, session_file)
        return username, app_id, app_hash, phone, session_file
    else:
        return user_data[1], user_data[3], user_data[4], user_data[5], user_data[6]


def user_interaction():
    while True:
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option (1/2/3): ")

        if choice == "1":
            register_new_user()
        elif choice == "2":
            user_data = login()
            if user_data:
                return user_data
        elif choice == "3":
            print("Exiting...")
            exit()
        else:
            print("Invalid choice!")


def human_delay():
    time.sleep(random.randint(5, 7))


def get_accumulator_list():
    with open("list_of_accumulators.txt", "r") as file:
        return file.readlines()


def save_accumulator_list(accumulators):
    with open("list_of_accumulators.txt", "w") as file:
        file.writelines(accumulators)


def main():
    user_data = user_interaction()
    if not user_data:
        print("Exiting...")
        return

    username, api_id, api_hash, phone, session_file = user_data

    accumulators = get_accumulator_list()
    midpoint = len(accumulators) // 2

    client = TelegramClient(session_file, api_id, api_hash,
                            device_model="Desktop",
                            system_version="4.16.30-vxCUSTOM",
                            app_version="4.9")

    try:
        client.start(phone=phone)
        human_delay()

        # Прогрев сессии
        print("Preparing the session...")
        public_chats = ['bbcrussian', 'topor', 'ru2ch']
        for chat in public_chats:
            client.get_messages(chat, limit=2)
            human_delay()

        print("Session is ready!")

        confirmation = input("Enter CONFIRM to start the script: ")
        if confirmation != "CONFIRM":
            print("Confirmation not received. Exiting.")
            return

        for index, acc_id in enumerate(accumulators):
            charge_value = "25-50%" if index < midpoint else "50-75%"

            try:
                client.send_message('ScooterAccumulatorBot', acc_id.strip())
                time.sleep(0.5)
                messages = client.get_messages('ScooterAccumulatorBot', limit=1)
                response_message = messages[0]

                if "Укажите заряд" in response_message.text:
                    for button_row in response_message.reply_markup.rows:
                        for button in button_row.buttons:
                            if button.text == charge_value:
                                response_message.click(data=button.data)
                                break

                # Проверка на наличие слова "установлено" перед отправкой следующего аккумулятора
                while True:
                    time.sleep(0.5)
                    confirmation_message = client.get_messages('ScooterAccumulatorBot', limit=1)[0]
                    if "установлено" in confirmation_message.text:
                        break

            except (RPCError, TimeoutError) as e:
                print(f"Error with {acc_id.strip()}: {str(e)}")
                save_accumulator_list(accumulators[index:])
                break

    finally:
        client.disconnect()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
