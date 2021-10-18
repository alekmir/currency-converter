import requests, json


cached_currencies = []


def get_currency(currency_code):
    global cached_currencies

    currency_code = currency_code.lower()
    currency_data = dict(eval(requests.get(f'http://www.floatrates.com/daily/{currency_code}.json').text))
    new_currency = {currency_code: currency_data}
    with open(f'{currency_code}.json', 'w', encoding='utf-8') as currency:
        json.dump(new_currency, currency, indent=4)
    cached_currencies.append(currency_code)


get_currency("usd")
get_currency("eur")


def exchange(sell_currency, buy_currency, amount):
    sell_currency = sell_currency.lower()
    buy_currency = buy_currency.lower()
    print("Checking the cache...")
    if sell_currency not in cached_currencies:
        get_currency(sell_currency)
    if buy_currency not in cached_currencies:
        print("Sorry, but it is not in the cache!")
        get_currency(buy_currency)
    else:
        print("Oh! It is in the cache!")
    with open(f"{sell_currency}.json", 'r') as file:
        currencies = json.load(file)
        result = round(amount * currencies[sell_currency][buy_currency]['rate'], 2)
    return result


sell_currency = input().upper()
buy_currency = input().upper()
amount = float(input())
while True:
    print(f"You received {exchange(sell_currency, buy_currency, amount)} {buy_currency}.")
    buy_currency = input().upper()
    if buy_currency == "":
        break
    amount = float(input())
    if amount == "":
        break
