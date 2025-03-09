import os
from flare_ai_social.ai.base import BaseAIProvider
from web3 import Web3
import json

# Replace with your actual values
FLARE_RPC_URL = "https://flare-api.flare.network/ext/C/rpc"
FTSO_CONTRACT_ADDRESS = "0xB18d3A5e5A85C65cE47f977D7F486B79F99D3d32"
FTSO_CONTRACT_ABI_FILE = "./src/data/Flare_ABI.json"
# Replace with the *actual* bytes21 feed ID for FLR!
FLR_FEED_ID = '0x01464c522f55534400000000000000000000000000'
PRICE_RESOLUTION = 10000000  # Replace with the actual number!


class FTSOService:

    def __init__(self) -> None:
        pass

    def get_flr_price(self):
        """Retrieves the current price of the Flare token from the FTSO."""
        # Print the current working directory
        print("Current Path:", os.getcwd())

        # 1. Connect to the Flare network
        w3 = Web3(Web3.HTTPProvider(FLARE_RPC_URL))
        if not w3.is_connected():
            raise ConnectionError("Failed to connect to Flare network.")

        # 2. Load the FTSO contract ABI
        with open(FTSO_CONTRACT_ABI_FILE, 'r') as f:
            ftso_abi = json.load(f)

        # 3. Create the FTSO contract instance
        ftso_contract = w3.eth.contract(
            address=FTSO_CONTRACT_ADDRESS, abi=ftso_abi)

        # 4. Query the contract for the price
        try:
            # Using getFeedById
            price, decimals, timestamp = ftso_contract.functions.getFeedById(
                FLR_FEED_ID).call()

            # Price in Wei example
            # price_in_wei, timestamp = ftso_contract.functions.getFeedByIdInWei(FLR_FEED_ID).call()

        except Exception as e:
            print(f"Error getting price: {e}")
            return None

        # 5. Handle price resolution
        actual_price = price / PRICE_RESOLUTION  # or price_in_wei / PRICE_RESOLUTION

        return actual_price, timestamp


if __name__ == "__main__":
    try:
        ftso_service = FTSOService()
        flr_price, timestamp = ftso_service.get_flr_price()
        if flr_price is not None:
            print(f"Current FLR price: {flr_price}")
            print(f"Timestamp: {timestamp}")
        else:
            print("Failed to retrieve FLR price.")
    except Exception as e:
        print(f"An error occurred: {e}")
