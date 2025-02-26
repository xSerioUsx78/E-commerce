import requests


class BrsAPI:

    def __init__(self):
        self.url = "https://brsapi.ir/FreeTsetmcBourseApi/Api_Free_Gold_Currency.json"

    def get_currency_rate(
        self,
        key: str = "currency",
        name: str = None
    ) -> dict:
        """
        Args:
            key: gold, currency or cryptocurrency, default is "currency".
            name: can be any gold, currency or cryptocurrency name to filter on.
        """

        if name and not key:
            raise ValueError(
                "For filtering by name, you should provide a key first."
            )

        res = requests.get(self.url)
        if not res.ok:
            return {}

        json = res.json()

        if key:
            json = json.get(key)

            if name and json:
                json = list(filter(
                    lambda obj: obj.get('name') == name,
                    json
                ))
                if json:
                    json = json[0]

        return json
