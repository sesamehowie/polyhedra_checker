from time import sleep
import csv
from random import randint
from itertools import cycle
from loguru import logger
import requests


with open("proxies.txt", "r") as file:
    proxies = file.read().splitlines()


def check(address: str, proxy: str) -> float:
    addr_prefix = address.lower()[2:5]
    url_1 = f"https://pub-88646eee386a4ddb840cfb05e7a8d8a5.r2.dev/eth_data/{addr_prefix.lower()}.json"

    while True:
        resp_1 = requests.get(
            url_1, proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'})
        sleep(randint(1, 2))

        if resp_1.status_code == 200:
            json_1 = resp_1.json()
            break

    if json_1:
        for item in json_1.keys():
            if address.lower() == item.lower():
                addr = item
                val_1 = int(json_1[addr]['amount'], 16)
                break
        else:
            val_1 = 0

    return val_1 / 10 ** 18 if val_1 is not None else 0


if __name__ == '__main__':
    rows = []
    results = []
    proxy_cycle = cycle(proxies)
    proxy = next(proxy_cycle)

    with open('wallets.txt') as file:
        wallets = file.read().splitlines()

    rows = tuple(enumerate(wallets, start=1))

    if len(rows) > 0:
        for row in rows:
            proxy = next(proxy_cycle)
            ind, wallet = row
            result = check(wallet, proxy)
            logger.info(f'{ind} - {wallet} - {result}')
            res = [ind, wallet, result]
            results.append(res)

    if len(results) > 0:
        with open('results.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            for r in results:
                writer.writerow(r)
