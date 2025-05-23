from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from web3 import Web3
import json
import os

# Connect to local blockchain (Hardhat network)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))  # Change if needed

# Load ABI
abi_path = os.path.join(settings.BASE_DIR, 'backend/fir', 'contract_abi.json')
with open(abi_path, 'r') as f:
    abi = json.load(f)

# Blockchain details — from settings.py
contract_address = settings.CONTRACT_ADDRESS
public_address = settings.BLOCKCHAIN_ADDRESS
private_key = settings.BLOCKCHAIN_PRIVATE_KEY

contract = w3.eth.contract(address=contract_address, abi=abi)

# View to render FIR submission form
def fir(request):
    return render(request, "fir/template/fir.html")

# View to handle form submission
def submit_fir(request):
    if request.method == "POST":
        name = request.POST['name']
        desc = request.POST['desc']
        ipfs_hash = request.POST.get('ipfs', 'NA')

        nonce = w3.eth.get_transaction_count(public_address)

        txn = contract.functions.fileFIR(name, desc, ipfs_hash).build_transaction({
            'from': public_address,
            'nonce': nonce,
            'gas': 300000,
            'gasPrice': w3.to_wei('5', 'gwei')
        })

        signed_txn = w3.eth.account.sign_transaction(txn, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

        return render(request, 'fir/template/success.html', {'tx_hash': tx_hash.hex()} )

    # return render(request, "fir/fir_form.html")


def view_firs(request):
        firs = []
        fir_count = contract.functions.firCount().call()

        for i in range(fir_count):
            fir = contract.functions.getFIR(i).call()
            firs.append({
                "name": fir[0],
                "description": fir[1],
                "ipfs": fir[2],
                "timestamp": fir[3],
            })

        return render(request, "fir/template/view_fir.html", {"firs": firs})
