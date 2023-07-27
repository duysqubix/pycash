import typer
import os
import requests

from typing_extensions import Annotated
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()

APIS = {
    "CoinBaseAPI": {
        "base": "https://rest.coinapi.io/v1/",
        "headers": {"X-CoinAPI-Key": os.environ["COINBASE_API_KEY"]},
        "uris": {"exchangerate": "exchangerate/{f}/{t}"},
    }
}

API = APIS["CoinBaseAPI"]  # change later to support multiple apis
main_app = typer.Typer()
convert_app = typer.Typer()


class Currency:
    def __init__(self, ticker, symbol, before=True) -> None:
        self.ticker = ticker.upper()
        self.symbol = symbol
        self.before = before

    def format_number(self, num):
        if isinstance(num, float):
            str_num = str(num)
            if "." in str_num:
                decimal_part = str_num.split(".")[1]
                if len(decimal_part) > 2:
                    for i in range(2, len(decimal_part)):
                        if decimal_part[i] != "0":
                            return round(num, i + 1)
            return round(num, 2)
        else:
            return num

    def format(self, amount):
        amount = self.format_number(amount)
        if self.before:
            return f"{self.symbol}{amount:,}"
        else:
            return f"{amount:,} {self.symbol}"


CURRENCIES = {
    "USD": Currency("USD", "$", before=True),
    "ETH": Currency("ETH", "⟠", before=False),
    "BTC": Currency("BTC", "₿", before=False),
    "XRP": Currency("XRP", "✕", before=False),
    "DOGE": Currency("DOGE", "Ð", before=False),
    "LTC": Currency("LTC", "Ł", before=False),
    "USDT": Currency("USDT", "₮", before=False),
    "RPL": Currency("RPL", ""),
}


def prettify_value(value: float) -> str:
    return f"{value:,.2f}"


@main_app.command("rate")
def rate():
    pass


@main_app.command("convert")
def convert(
    f: Annotated[str, typer.Argument(help="From format, supply ticker")],
    t: Annotated[str, typer.Argument(help="To format, supply ticker")],
    amount: Annotated[
        float, typer.Argument(help="Amount to convert the from value")
    ] = 1.0,
):
    """
    Convert from one currency to another
    """
    f = CURRENCIES[f.upper()]
    t = CURRENCIES[t.upper()]

    url = API["base"] + API["uris"]["exchangerate"].format(f=f.ticker, t=t.ticker)
    try:
        resp = requests.get(url, headers=API["headers"])
    except Exception as e:
        print("error in calling API")
        return

    rate = resp.json()["rate"]

    price = rate * amount

    headers = [
        f"{f.ticker}",
        f"{t.ticker}",
        f"{t.ticker}/{f.ticker}",
    ]
    values = (
        (
            f.format(amount),
            t.format(price),
            t.format(rate),
        ),
    )

    result = tabulate(values, headers=headers, tablefmt="fancy_grid")
    print(result)


if __name__ == "__main__":
    main_app()
