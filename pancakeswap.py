import decimal
from web3 import Web3
import time
import requests
import json
import math
from datetime import datetime
from webapi import ApiBSCScan, Api0X

class PancakeSwap:
    def __init__(self):
        self.BscScan = ApiBSCScan()

        self.wallet_balance = 0
        self.WBNB_CONTRACT = "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"

        self.PANCAKESWAP_API_URL = "https://api.pancakeswap.info/api/v2/"
        self.PANCAKESWAP_ROUTER_ADDRESS = "0x10ED43C718714eb63d5aA57B78B54704E256024E"

        self.BINANCE_RPC_URL = "https://bsc-dataseed.binance.org/"
        self.DEFIBIT_RPC_URL = "https://bsc-dataseed1.defibit.io"

        self.PANABI = '[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'

    def getTokenPrice(self, token_adress):
        try:
            response = requests.get(self.PANCAKESWAP_API_URL + "tokens/" + token_adress)
        except Exception as error:
            return {
                "error": True,
                "message": error.args[0],
                "data": {"name": "", "symbol": "", "price_USDT": "", "price_BNB": ""},
                "updated_at": 0
            }

        if response.status_code == 200:
            data_json = json.loads(response.text)
            return {
                "error": False,
                "message": "OK",
                "data": data_json["data"],
                "updated_at": data_json["updated_at"]
            }
        else:
            return None

    def startWeb3(self):
        try:
            self.web3 = Web3(Web3.HTTPProvider(self.DEFIBIT_RPC_URL))
            print("Web3 Connection:" + str(self.web3.isConnected()))
            # self.web3.eth.get_balance(self.WALLET_ADDRESS)
            return '{"error": False, "message": "OK", "connection":'+self.web3.isConnected()+'}'
        except Exception as error:
            return '{"error": False, "message": "'+ error.args[0] +'"}'

    def web3_isConnected(self):
        return self.web3.isConnected()

    def startWeb3____eski(self):
        try:
            self.web3 = Web3(Web3.HTTPProvider(self.BINANCE_RPC_URL))
            print("Web3 Connection:" + str(self.web3.isConnected()))
            self.web3.eth.get_balance(self.WALLET_ADDRESS)
            return self.web3.isConnected()
        except Exception as error:
            return False

    def getWalletBalance(self, wallet_address):
        try:
            balance = self.web3.eth.get_balance(wallet_address)
            self.wallet_balance = self.web3.fromWei(balance, 'ether')
            return str(self.wallet_balance)

        except Exception as error:
            return 0

    def getTokenInfo(self, token_address, wallet_address):
        abi = self.BscScan.getABI(token_address)
        if abi["error"]:
            return abi
        
        try:
            contract = self.web3.eth.contract(address=self.web3.toChecksumAddress(token_address), abi=abi["abi"])
            decimals = contract.functions.decimals().call()
            check_approve = self.BscScan.checkApprove(token_address, wallet_address)

            token_info = {
                "name": contract.functions.name().call(),
                "symbol": contract.functions.symbol().call(),
                "decimals": decimals,
                "balance": contract.functions.balanceOf(wallet_address).call() / math.pow(10, decimals),
                "address": token_address,
                "approved": check_approve["approve"]
            }
            
            return {
                "error": False,
                "message": "OK",
                "token_info": token_info
            }
        except Exception as error:
            print(error)
            return {
                "error": True,
                "message": "There is a problem with the BSC network. Please try again later.",
                "error_message": error.args[0]
            }

    def getTokenBalance(self, token_address, wallet_address):
        balance = 0
        abi = self.BscScan.getABI(token_address)
        
        if abi["error"]:
            None
        try:
            contract = self.web3.eth.contract(address=self.web3.toChecksumAddress(token_address), abi=abi["abi"])
            decimals = contract.functions.decimals().call()
            balance = contract.functions.balanceOf(wallet_address).call() / math.pow(10, decimals)
        except Exception as error:
            print("ps.getTokenBalance: " + error.args[0])

        return balance
    
    def buyToken(self, token_address, bnb_amount=0.00001, slippage=12, gas=5, wallet_address = "", wallet_private_key = ""):
        token_to_buy = self.web3.toChecksumAddress(token_address)
        token_to_spend = self.web3.toChecksumAddress(self.WBNB_CONTRACT)
        contract = self.web3.eth.contract(address=self.PANCAKESWAP_ROUTER_ADDRESS, abi=self.PANABI)

        min_amount_of_target_token_to_buy = bnb_amount * ((100 - slippage) / 100)

        print(f"gas: {gas} gwei = {self.web3.toWei(gas, 'ether')}")
        print(f"bnb_amount: {bnb_amount} | min_bnb_amount: {min_amount_of_target_token_to_buy} | slippage: {slippage}")

        nonce = self.web3.eth.get_transaction_count(wallet_address)
        estimated_gas = self.getEstimatedGas(buy_token_address=token_address, sell_token_address=self.WBNB_CONTRACT, amount=bnb_amount)

        try:
            pancakes2_txn = contract.functions.swapExactETHForTokens(
                self.web3.toWei(min_amount_of_target_token_to_buy, 'ether'),
                [token_to_spend, token_to_buy],
                wallet_address,
                (int(time.time()) + 10000)
            ).buildTransaction({
                'from': wallet_address,
                'value': self.web3.toWei(bnb_amount, 'ether'),
                'gas': int(estimated_gas["estimatedGas"]),
                'gasPrice': int(self.web3.toWei(gas, 'gwei')),
                'nonce': nonce,
            })
        except Exception as error:
            print("Hata! Token alınamadı!", error, token_address)
            return None

        try:
            signed_txn = self.web3.eth.account.sign_transaction(pancakes2_txn, private_key=wallet_private_key)
        except Exception as error:
            print(error)

        try:
            tx_token = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        except Exception as error:
            result = error.args[0]
            print("buyToken: " + str(result))

            if result["code"] == -32000:
                message = "There is not enough balance for fee."
            else:
                message = str(result["code"]) + " - " + result["message"]

            return {
                "error": True,
                "message": message
            }

        return {
            "error": False,
            "message": "The contract has been sent. Waiting for transaction response...",
            "hex": self.web3.toHex(tx_token)
        }

    def sellToken(self, token_address, token_balance=0, slippage=12, gas=5, wallet_address = "", wallet_private_key = ""):
        contract_id = self.web3.toChecksumAddress(token_address)
        contract = self.web3.eth.contract(address=self.PANCAKESWAP_ROUTER_ADDRESS, abi=self.PANABI)

        result_abi = self.getABI(token_address)
        if result_abi["error"]:
            return result_abi

        sell_token_contract = self.web3.eth.contract(contract_id, abi=result_abi["abi"])
        if token_balance == 0:

            token_balance = sell_token_contract.functions.balanceOf(wallet_address).call()
        print(sell_token_contract.functions.balanceOf(wallet_address).call())
        print(self.web3.toWei(token_balance, 'ether'))
        min_amount_of_target_token_to_sell = token_balance * ((100 - slippage) / 100)

        result_approve = self.approveToken(token_address, token_balance)
        if result_approve["error"]:
            return result_approve

        try:
            pancakeswap2_txn = contract.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
                self.web3.toWei(token_balance, 'ether'), self.web3.toWei(min_amount_of_target_token_to_sell, 'ether'),
                [contract_id, self.web3.toChecksumAddress(self.WBNB_CONTRACT)],
                wallet_address,
                (int(time.time()) + 10000)
            ).buildTransaction({
                'from': wallet_address,
                # 'gas': 100000,
                'gasPrice': self.web3.toWei('5', 'gwei'),
                'nonce': self.web3.eth.get_transaction_count(wallet_address)
            })
        except Exception as error:
            print("\nHata! Token satılamadı!", error)
            return {
                "error": True,
                "message": error.args[0]
            }

        signed_txn = self.web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=wallet_private_key)
        tx_token = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return self.web3.toHex(tx_token)

    def approveToken(self, token_address, token_balance, wallet_address, wallet_private_key):
        approve_result = self.BscScan.checkApprove(token_address, wallet_address)
        if approve_result["error"] is False and approve_result["approve"] is True:
            return {
                "error": False,
                "message": "",
                "approve": True
            }

        sell_abi = self.getABI(token_address)
        if sell_abi is None:
            return {
                "error": True,
                "message": "Unable to get abi information from bscscan.com",
                "approve": False
            }

        sell_token_contract = self.web3.eth.contract(self.web3.toChecksumAddress(token_address), abi=sell_abi["abi"])

        approve = sell_token_contract.functions.approve(self.PANCAKESWAP_ROUTER_ADDRESS, self.web3.toWei(token_balance, "ether")).buildTransaction({
            'from': wallet_address,
            'gasPrice': self.web3.toWei('5', 'gwei'),
            'nonce': self.web3.eth.get_transaction_count(wallet_address),
        })

        try:
            signed_txn = self.web3.eth.account.sign_transaction(approve, private_key=wallet_private_key)
            tx_token = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        except Exception as error:
            return {
                "error": True,
                "message": error.args[0],
                "approve": False
            }

        print("approve_hash - ", self.web3.toHex(tx_token))

        return {
            "error": False,
            "message": "The contract for the token has been submitted for approval. Waiting for response.",
            "approve": True,
            "approve_hex": self.web3.toHex(tx_token)
        }

    def getTransactionDetails(self, tx_hash):
        tx_data = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        tx_json = tx_data.__dict__
        # print(self.web3.eth.getTransaction(tx_hash))
        # tx_json["value"] = float(self.web3.fromWei(tx_data["value"], "ether"))
        gas_price = self.web3.eth.getTransaction(tx_hash).gasPrice
        gas_used = self.web3.eth.getTransactionReceipt(tx_hash).gasUsed
        transaction_cost = gas_price * gas_used

        tx_json["fee"] = float(self.web3.fromWei(transaction_cost, "ether"))

        print("Transaction Details 1. ", tx_json)
        print("Transaction Details 2. ", self.web3.eth.getTransaction(tx_hash))
        return tx_json

    def getEstimatedGas(self, buy_token_address, sell_token_address, amount):
        return {
            "error": False,
            "gas": 110000,
            "estimatedGas": 110000,
            "gasPrice": 5000000000
        }

    def calcBNBPrice(self):
        bnbToSell = self.web3.toWei("1", "ether")

        WBNB = self.web3.toChecksumAddress(self.WBNB_CONTRACT)
        USDT = self.web3.toChecksumAddress('0x55d398326f99059fF775485246999027B3197955')

        router = self.web3.eth.contract(address=self.PANCAKESWAP_ROUTER_ADDRESS, abi=self.PANABI)

        try:
            amount_out = router.functions.getAmountsOut(bnbToSell, [WBNB, USDT]).call()
            amount_wbnb = self.web3.fromWei(amount_out[0], 'ether')
            amount_usdt = self.web3.fromWei(amount_out[1], 'ether')

        except Exception as error:
            print("\ncalcBNBPrice error")
            print(error)
            return 0

        return amount_usdt

    def calcTokenPrice(self, token_address):
        bnb_to_sell_amount = self.web3.toWei("1", "ether")
        router = self.web3.eth.contract(address=self.PANCAKESWAP_ROUTER_ADDRESS, abi=self.PANABI)

        try:
            wbnb = self.web3.toChecksumAddress(self.WBNB_CONTRACT)
            custom_token = self.web3.toChecksumAddress(token_address)

            # standard_token_abi = self.BscScan.getABI(token_address)["abi"]
            standard_token_abi = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"}]'

            token_router = self.web3.eth.contract(address=custom_token, abi=standard_token_abi)
            token_decimals = token_router.functions.decimals().call()

            amount_out = router.functions.getAmountsOut(bnb_to_sell_amount, [wbnb, custom_token]).call()
            amount_wbnb = self.web3.fromWei(amount_out[0], 'ether')

        except Exception as error:
            return {
                "error": True,
                "message": "calcTokenPrice | " + str(error.args[0]),
                "data": {
                    "price_USDT": "0",
                    "price_BNB": "0",
                },
                "updated_at": "0"
            }

        amount_custom_token = str(amount_out[1])[:len(str(amount_out[1]))-token_decimals] + "." + str(amount_out[1])[-1*token_decimals:]

        bnb_usdt_price = self.calcBNBPrice()

        return {
            "error": False,
            "message": None,
            "data": {
                "price_USDT": float(bnb_usdt_price) / float(amount_custom_token),
                "price_BNB": 1 / float(amount_custom_token),
            },
            "updated_at": str(datetime.now())
        }