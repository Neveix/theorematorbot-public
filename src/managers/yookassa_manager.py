class Confirmation:
    def __init__(self):
        self.confirmation_url: str | None = None
    @staticmethod
    def from_json(json: str) -> "Confirmation":
        self = Confirmation()
        self.confirmation_url = json["confirmation_url"]
        return self
class Amount:
    def __init__(self):
        self.value: str | None = None
    def get_value_int(self) -> int:
        return int(float(self.value))
    @staticmethod
    def from_json(json: str) -> "Amount":
        self = Amount()
        self.value = json["value"]
        return self
class Payment:
    def __init__(self):
        self.id: str | None = None
        self.amount: Amount | None = None
        self.status: str | None = None
        self.confirmation : Confirmation | None = None
    @staticmethod
    def from_json(json: str) -> "Payment":
        self = Payment()
        try:
            self.id = json["id"]
            self.amount = Amount.from_json(json["amount"])
            self.status = json["status"]
            confirmation = json.get("confirmation")
            if confirmation is not None:
                self.confirmation = Confirmation.from_json(confirmation)
        except KeyError as e:
            print(f"from_json KeyError, {json=}")
        return self
    
class YookassaManager:
    def __init__(self, shop_id: str, secret_key: str):
        self.shop_id = shop_id
        self.secret_key = secret_key
        from aiohttp import BasicAuth
        self.auth = BasicAuth(
            login = shop_id, 
            password = secret_key)
        self.return_url: str | None = None
        self.api_url = "https://api.yookassa.ru/v3/payments"
        self.last_cursor: str | None = None
    async def fetch(self, url: str, params: dict | None = None) -> dict:
        from aiohttp import ClientSession
        async with ClientSession(
                auth=self.auth) as session:
            async with session.get(url, params = params) as response:
                return await response.json()
    async def post(self, url: str, headers: dict, json_data: dict) -> dict:
        from aiohttp import ClientSession
        async with ClientSession(
                auth=self.auth, headers=headers) as session:
            async with session.post(url, json=json_data) as response:
                return await response.json()
    async def payment_find(self, payment_id: str) -> Payment:
        return Payment.from_json(await self.fetch(
            self.api_url + f"/{payment_id}"
        ))
    async def payment_create(self, 
            description: str, 
            amount: int, 
            save_payment_method: bool = False,
            payment_method_id: str | None = None
            ) -> Payment:
        json_data = {
            "amount": {
                "value": f"{int(amount)}.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": self.return_url
            },
            "description": description,
            "capture": True,
            "save_payment_method": save_payment_method
        }
        if payment_method_id:
            json_data["payment_method_id"] = payment_method_id
        from uuid import uuid4
        headers = {
            "Idempotence-Key": str(uuid4()),
            "Content-Type": "application/json"
        }
        return Payment.from_json(
            await self.post(self.api_url, headers, json_data)
        )
    async def payments_succeeded_list(
            self, 
            created_at_gte: str
        ) -> dict:
        params = {
             "limit" : 100
            ,"created_at.gte" : created_at_gte
            ,"status" : "succeeded"
        }
        return await self.fetch(
            self.api_url,
            params = params
        )