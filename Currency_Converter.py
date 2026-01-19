import os
import requests
from dotenv import load_dotenv

# 1. Load the secrets from the .env file into the system
load_dotenv()

def fetch_data():
    # 2. Grab the key from the environment instead of hardcoding it
    api_key = os.getenv('CURRENCY_API_KEY')
    
    # 3. Handle case where the key might be missing from .env
    if not api_key:
        return "Error: API Key not found in .env file."

    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"

    try:
        response = requests.get(url)
        # Raise an exception for bad status codes (401, 404, etc.)
        response.raise_for_status() 
        data = response.json()
        return data['conversion_rates']
    except requests.exceptions.RequestException as e:
        return f"Connection Error: {e}"

def conversion():
    rates = fetch_data()
    
    # If fetch_data returned a string, it means an error happened
    if isinstance(rates, str):
        print(rates)
        return

    try:
        amount = float(input('Enter the amount in USD: $').strip())
        target_currency = input('Enter target currency (e.g., INR): ').strip().upper()

        if target_currency in rates:
            exchange_value = rates[target_currency]
            result = exchange_value * amount
            print(f"\nResult: {amount} USD = {result:.2f} {target_currency}")
        else:
            print(f"Error: {target_currency} is not a valid currency code.")
            
    except ValueError:
        print("Error: Please enter a valid numeric amount.")

if __name__ == "__main__":
    conversion()
