import random
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError, RPCError
import time

api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'

def human_delay():
    time.sleep(random.randint(5, 7))

def get_accumulator_list():
    with open("list_of_accumulators.txt", "r") as file:
        return file.readlines()

def save_accumulator_list(accumulators):
    with open("list_of_accumulators.txt", "w") as file:
        file.writelines(accumulators)

def main():
    accumulators = get_accumulator_list()
    midpoint = len(accumulators) // 2

    client = TelegramClient('my_session', api_id, api_hash,
                            device_model="Desktop",
                            system_version="4.16.30-vxCUSTOM",
                            app_version="4.9")

    try:
        client.start(phone='YOUR_PHONE_NUMBER')
        human_delay()

        # Прогрев сессии
        print("Preparing the session...")
        public_chats = ['CHANNEL_1', 'CHANNEL_2', 'CHANNEL_3']
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
                human_delay()
                messages = client.get_messages('ScooterAccumulatorBot', limit=1)
                response_message = messages[0]

                if "Укажите заряд" in response_message.text:
                    for button_row in response_message.reply_markup.rows:
                        for button in button_row.buttons:
                            if button.text == charge_value:
                                response_message.click(data=button.data)
                                break
                human_delay()

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