import requests


class ApiBSCScan:
    def __init__(self):
        self.API_URL = "https://api.bscscan.com/api"
        self.API_KEY = "ZVIBVJRNZ85H69RATX35JAHGFGA8YZ3YGP"

    def getABI(self, token_address):
        API_ENDPOINT = f"{self.API_URL}?module=contract&action=getabi&address={str(token_address)}&apikey={self.API_KEY}"

        try:
            r = requests.get(url=API_ENDPOINT)
            response = r.json()

        except Exception as error:
            return {
                "error": True,
                "message": error.args[0]
            }

        if response["message"] != "OK":
            return {
                "error": True,
                "message": response["result"]
            }
        else:
            return {
                "error": False,
                "message": "",
                "abi": response["result"]
            }

    def checkApprove(self, token_address, wallet_address):
        API_ENDPOINT = self.API_URL + f"?module=account&action=txlist&address={wallet_address}&startblock=1&endblock=999999999999&sort=desc&apikey={self.API_KEY}"
        try:
            r = requests.get(url=API_ENDPOINT)
            response = r.json()

        except Exception as error:
            return {
                "error": True,
                "message": "bscscan.com error. Please try again later.",
                "error_message": error,
                "approve": False
            }

        if response["status"] == 0:
            return {
                "error": True,
                "message": str(response["message"]),
                "approve": False
            }

        bsc_results = response["result"]
        for bsc_result in bsc_results:
            if bsc_result["from"] == wallet_address.lower() and bsc_result["to"] == token_address.lower() and (bsc_result["isError"] == '0' or bsc_result["isError"] == 0) and bsc_result["input"].lower()[:10] == "0x095ea7b3":
                return {
                    "error": False,
                    "approve": True,
                    "approve_hash": bsc_result["hash"]
                }
                break

        return {
            "error": False,
            "approve": False,
            "approve_hash": ""
        }


class Api0X:
    def __init__(self):
        self.API_URL = "https://bsc.api.0x.org/"

    def estimatedGas(self, sell_token_address, buy_token_address, amount):
        # f"https://bsc.api.0x.org/swap/v1/price?sellToken=0xa1cd598613ac657a27cdaa23b19ba715ab760cc4&buyToken=WBNB&sellAmount=776894863018"
        # f"https://bsc.api.0x.org/swap/v1/quote?sellToken=0xa1cd598613ac657a27cdaa23b19ba715ab760cc4&buyToken=WBNB&sellAmount=776894863018"
        response_url = f"{self.API_URL}swap/v1/quote?sellToken={sell_token_address}&buyToken={buy_token_address}&sellAmount={int(amount)}"
        try:
            r = requests.get(url=response_url)
            response = r.json()

        except Exception as error:
            return {
                "error": True,
                "message": "Gas quantity could not be predicted."
            }

        return {
            "error": False,
            "gas": response["gas"],
            "estimatedGas": response["estimatedGas"],
            "gasPrice": response["gasPrice"]
        }