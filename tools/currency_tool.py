import requests


def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str
):

    try:

        url = (
            f"https://open.er-api.com/v6/latest/"
            f"{from_currency.upper()}"
        )

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        rate = data["rates"][
            to_currency.upper()
        ]

        converted_amount = (
            amount * rate
        )

        return {

            "amount": amount,

            "from_currency":
                from_currency.upper(),

            "to_currency":
                to_currency.upper(),

            "exchange_rate": rate,

            "converted_amount":
                round(converted_amount, 2)
        }

    except Exception as e:

        return {
            "error": str(e)
        }