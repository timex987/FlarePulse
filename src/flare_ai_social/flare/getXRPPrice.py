import requests
import json
from flare_ai_social.settings import settings


def get_xrp_price_fdc():
    """
    Retrieves the XRP (Ripple) price in USD from Financial Data Cloud (FDC) API.

    Args:
        api_key: Your FDC API key.  You MUST obtain this from FDC.

    Returns:
        The XRP price as a float, or None if there was an error.
    """

    url = "https://financialmodelingprep.com/api/v3/quote/XRPUSD"  # XRP to USD
    params = {
        "apikey": settings.FINANCIALMODELING_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        data = response.json()

        if data and isinstance(data, list) and len(data) > 0:
            # Correctly access the price. Key is "price"
            price = data[0].get("price")
            if price is not None:
                return float(price)
            else:
                print("Error: Price not found in the response.")
                return None  # Or raise an exception if price is mandatory
        else:
            print("Error: Invalid response format or no data returned.")
            print(data)  # Print the received data for debugging.
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(response.text)  # Print the raw response text for debugging
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


if __name__ == '__main__':
    # Replace "YOUR_API_KEY" with your actual Financial Data Cloud API key

    xrp_price = get_xrp_price_fdc()

    if xrp_price is not None:
        print(f"The current XRP/USD price is: {xrp_price}")
    else:
        print("Failed to retrieve the XRP/USD price.")
