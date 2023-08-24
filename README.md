# Battery Charge Updater for Telegram

This script automates the task of updating the charge of batteries in a Telegram bot.

## Setup

1. Clone this repository.
2. Install the requirements using `pip install -r requirements.txt`.
3. Replace the placeholders in `Battery.py`:
    - `YOUR_API_ID`: Obtain this from [Telegram's API Development Tools](https://my.telegram.org/auth).
    - `YOUR_API_HASH`: Obtain this from [Telegram's API Development Tools](https://my.telegram.org/auth).
    - `YOUR_PHONE_NUMBER`: Your phone number associated with your Telegram account in international format.
    - `CHANNEL_1`, `CHANNEL_2`, etc.: Replace these with actual public channel usernames for warming up the session.
4. Run the script using `python Battery.py`.

## Usage

1. When prompted, enter `CONFIRM` to start the script.
2. The script will go through the list of accumulators and update their charge based on the specified criteria.

## Possible Errors

- **Timeout or Long Delays**: Sometimes, the bot or Telegram servers might be slow to respond. The script is designed to handle such scenarios and will wait for a response. However, if the delay is too long, it might timeout.
- **Invalid Accumulator ID**: If the bot responds with an error indicating an invalid accumulator ID, the script will skip that accumulator and move to the next one.
- **Session Errors**: If there are issues with the session or if it becomes invalid, you might need to re-authenticate by entering the code sent to your Telegram account.

## Note

Always ensure that you are not violating Telegram's Terms of Service when using automation scripts.
