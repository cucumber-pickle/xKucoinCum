   # xKuCoin Farming Bot 
A Python-based automation scripts that uses no API Telegram for interacting with the xKuCoin API

[![Join our Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/cucumber_scripts)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/cucumber-pickle/Cucumber)

# REGISTRATIONS 
1. Visit - [https://t.me/xkucoinbot/](https://t.me/xkucoinbot/kucoinminiapp?startapp=cm91dGU9JTJGdGFwLWdhbWUlM0ZpbnZpdGVyVXNlcklkJTNENzI2ODM3NjIxJTI2cmNvZGUlM0Q=)
2. press continue until you log in to the app

## Installation
1. **Clone the Repository:**

   ```bash
   git clone https://github.com/cucumber-pickle/xKucoinCum.git
   cd xKucoinCum
   ```

2. **Create a virtual environment (optional but recommended)**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

   
3. **Install Dependencies:**

The bot uses Python 3 and requires some external libraries. You can install them using:

  ```bash
    pip install -r requirements.txt
  ```


## Configuration Setup:

Create a config.json file in the project root directory:

   ```json

{
    "use_proxy": true,
    "min_click": 50,
    "max_click": 70,
    "min_delay_click": 1,
    "max_delay_click": 3,
    "workers": 5,
    "countdown_loop": 1000
}
   ```
- `use_proxy`: Enable/disable use_proxy (true/false).
- `min_click`: minimum click per request
- `max_click`: maximum click per request
- `min_delay_click`: minimum delay (in seconds) between clicks
- `max_delay_click`: maximum  delay (in seconds) between clicks
- `workers`: how many accounts will be running at the same time
- `countdown_loop`: total duration (in seconds) for which the main loop will run before restarting or stopping

## Query Setup:

Add your xKuCoin account tokens to a file named `data.txt` in the root directory. Each token should be on a new line.

Example:
   ```txt
query_id=AA....
user=%7B%22id%....
   ```

## Usage
Run the script with:

   ```bash
python bot.py
   ```

## How to get tgWebAppData (query_id / user_id)

1. Login telegram via portable or web version
2. Launch the bot
3. Press `F12` on the keyboard 
4. Open console
5. Сopy this code in Console for getting tgWebAppData (user= / query=):

```javascript
copy(Telegram.WebApp.initData)
```

6. you will get data that looks like this

```
query_id=AA....
user=%7B%22id%....
```
7. add it to `data.txt` file or create it if you dont have one


## This bot helpfull?  Please support me by buying me a coffee: 
``` 0xc4bb02b8882c4c88891b4196a9d64a20ef8d7c36 ``` - BSC (BEP 20)

``` UQBiNbT2cqf5gLwjvfstTYvsScNj-nJZlN2NSmZ97rTcvKz0 ``` - TON

``` 0xc4bb02b8882c4c88891b4196a9d64a20ef8d7c36 ``` - Optimism

``` THaLf1cdEoaA73Kk5yiKmcRwUTuouXjM17 ``` - TRX (TRC 20)

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For questions or support, please contact [CUCUMBER TG CHAT](https://t.me/cucumber_scripts_chat)
