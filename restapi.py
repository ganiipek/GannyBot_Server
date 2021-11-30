from flask import Flask, request
from pancakeswap import PancakeSwap
from webapi import ApiBSCScan, Api0X
import json


restAPI = Flask(__name__)
ps = PancakeSwap()
ps.startWeb3()

BscScan = ApiBSCScan()

def checkParameter(parameters, requets):
    for parameter in parameters:
        if parameter not in requets:
            return json.dumps({
                "error": True,
                "response": 400,
                "message" : f"Missing Parameter '{parameter}'"
            }), 400

@restAPI.route("/api/v1.0/get_wallet_balance", methods=["GET"])
def get_wallet_balance():
    requests = request.args.to_dict()
    check_parameter = checkParameter(["wallet_address"], requests)
    if check_parameter: 
        return check_parameter

    return json.dumps(ps.getWalletBalance(requests["wallet_address"]))

@restAPI.route("/api/v1.0/get_token_info", methods=["GET"])
def get_token_info():
    requests = request.args.to_dict()
    check_parameter = checkParameter(["token_address", "wallet_address"], requests)
    if check_parameter: 
        return check_parameter

    return json.dumps(ps.getTokenInfo(requests["token_address"], requests["wallet_address"]))

@restAPI.route("/api/v1.0/get_token_price", methods=["GET"])
def get_token_price():
    requests = request.args.to_dict()
    check_parameter = checkParameter(["token_address"], requests)
    if check_parameter: 
        return check_parameter
    print(requests)
    return json.dumps(ps.calcTokenPrice(requests["token_address"]))

@restAPI.route("/api/v1.0/get_token_balance", methods=["GET"])
def get_token_balance():
    requests = request.args.to_dict()
    check_parameter = checkParameter(["token_address", "wallet_address"], requests)
    if check_parameter: 
        return check_parameter

    return json.dumps(ps.getTokenBalance(requests["token_address"], requests["wallet_address"]))

@restAPI.route("/api/v1.0/get_token_abi", methods=["GET"])
def get_token_abi():
    requests = request.args.to_dict()
    check_parameter = checkParameter(["token_address"], requests)
    if check_parameter: 
        return check_parameter

    return json.dumps(BscScan.getABI(requests["token_address"]))

@restAPI.route("/api/v1.0/buy_token", methods=["GET"])
def buy_token():
    requests = request.args.to_dict()
    check_parameter = checkParameter(["token_address", "bnb_amount", "slippage", "gas", "wallet_address", "wallet_private_key"], requests)
    if check_parameter: 
        return check_parameter

    return json.dumps(ps.buyToken(requests["token_address"], requests["bnb_amount"], requests["slippage"], requests["gas"], requests["wallet_address"], requests["wallet_private_key"]))

@restAPI.route("/api/v1.0/check_app rove", methods=["GET"])
def check_approve():
    requests = request.args.to_dict()
    check_parameter = checkParameter(["token_address", "wallet_address"], requests)
    if check_parameter: 
        return check_parameter

    return json.dumps(BscScan.checkApprove(requests["token_address"], requests["wallet_address"]))

@restAPI.route("/api/v1.0/approve", methods=["GET"])
def approve():
    requests = request.args.to_dict()
    check_parameter = checkParameter(["token_address", "token_balance", "wallet_address", "wallet_private_key"], requests)
    if check_parameter: 
        return check_parameter

    return json.dumps(ps.approveToken(requests["token_address"], requests["token_balance"], requests["wallet_address"], requests["wallet_private_key"]))

@restAPI.route("/api/v1.0/sell_token", methods=["GET"])
def sell_token():
    requests = request.args.to_dict()
    check_parameter = checkParameter(["token_address", "token_balance", "slippage", "gas", "wallet_address", "wallet_private_key"], requests)
    if check_parameter: 
        return check_parameter

    return json.dumps(ps.buyToken(requests["token_address"], requests["token_balance"], requests["slippage"], requests["gas"], requests["wallet_address"], requests["wallet_private_key"]))


if __name__ == "__main__":
    restAPI.run(host="127.0.0.1", port=5000)

    