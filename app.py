import flask
from flask import request
import json
import datetime
from web3 import Web3
import os

app = flask.Flask(__name__)
infura_url = os.environ.get("INFURA_URL")
w3 = Web3(Web3.HTTPProvider(infura_url))

@app.route("/ethaddress/", methods=["GET"])
def ethaddress():
    address = request.args["address"]

    data = {
        "timestamp": str(datetime.datetime.now()),
        "input_address": address
    }

    if w3.isConnected():
        if w3.isAddress(address) and w3.isChecksumAddress(address):
            data["status"] = 200
            data["message"] = "Valid request"
            data["ens_address"] = w3.ens.name(address)

            eth_balance = w3.eth.getBalance(address)
            data["balances"] = {
                "ethereum_mainnet": {
                    "wei": str(eth_balance),
                    "eth": str(w3.fromWei(eth_balance, "ether"))
                }
            }

        else:
            data["status"] = 400
            data["message"] = "Invalid address"
    else:
        data["status"] = 500
        data["message"] = "Unable to connect to Ethereum node"

    return app.response_class(
        response = json.dumps(data),
        status = data["status"],
        mimetype = "application/json"
    )