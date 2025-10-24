import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dataClasses.Ticker import Ticker
from dataClasses import Option
from dataClasses import OptionChain
from apiConn import polygonAPI
from apiConn.alphaVantage import alphaVantage
from analysis.analytics import analytics


api_key = os.environ.get('POLYGON_API_KEY')
alpha_vantage_key = os.environ.get('ALPHA_VANTAGE_API_KEY')

if not api_key:
    print("Error: POLYGON_API_KEY not found in environment variables")
    print("Please set it in a .env file or export it in your shell")
    exit(1)

if not alpha_vantage_key:
    print("Error: ALPHA_VANTAGE_API_KEY not found in environment variables")
    print("Please set it in a .env file or export it in your shell")
    exit(1)

ticker_symbol = input("What ticker to look at: ")
expiration = input("What expiration for the option chain in format (YYYY-MM-DD): ")
num_strikes = int(input("How many strikes to be shown: "))

# First, get the stock data to create a Ticker object
print(f"\n{'='*60}")
print(f"Fetching stock data for {ticker_symbol}...")
print(f"{'='*60}")
alpha_api = alphaVantage(alpha_vantage_key, ticker_symbol)
stock = alpha_api.get_stock_data()

if stock is None:
    print(f"Failed to fetch stock data for {ticker_symbol}")
    exit()

print(f"Stock: {stock.get_symbol()} - Price: ${stock.get_price()} - Volume: {stock.get_volume()}")

# Now fetch the option chain data
print(f"\n{'='*60}")
print(f"Fetching option chain data...")
print(f"{'='*60}")
obj = polygonAPI.polygonAPI(api_key)

try:
    option_chain_data = obj.get_optionchain_data(stock, expiration, num_strikes=num_strikes)

    if option_chain_data:
        print(f"\nSuccessfully got option chain of ticker {stock.get_symbol()}")
        call_count = len(option_chain_data.get_call_chain())
        put_count = len(option_chain_data.get_put_chain())
        total_options = call_count + put_count
        print(f"Total options: {total_options} (Calls: {call_count}, Puts: {put_count})")

        # Test analytics functions
        print(f"\n{'='*60}")
        print(f"RUNNING ANALYTICS")
        print(f"{'='*60}")

        analyzer = analytics(option_chain_data)

        # 1. Put/Call Volume Ratio
        print(f"\n--- Put/Call Volume Ratio ---")
        pc_ratio = analyzer.put_call_volume_ratio(option_chain_data)
        if pc_ratio:
            print(f"P/C Ratio: {pc_ratio:.2f}")
            if pc_ratio > 1:
                print("  → More put volume (bearish sentiment)")
            elif pc_ratio < 1:
                print("  → More call volume (bullish sentiment)")
            else:
                print("  → Equal put/call volume (neutral)")
        else:
            print("Unable to calculate P/C ratio (no call volume)")

        # 2. Strike-by-Strike Volume Ratio
        print(f"\n--- Volume Analysis by Strike ---")
        strike_volumes = analyzer.strikes_volume_ratio(option_chain_data)
        print(f"{'Strike':<10} {'Call Vol':<12} {'Put Vol':<12} {'Total Vol':<12} {'P/C Ratio':<10}")
        print("-" * 60)
        for strike in sorted(strike_volumes.keys()):
            data = strike_volumes[strike]
            ratio_str = f"{data['ratio']:.2f}" if data['ratio'] is not None else "N/A"
            print(f"{strike:<10.2f} {data['call_vol']:<12} {data['put_vol']:<12} {data['total_vol']:<12} {ratio_str:<10}")

        # 3. Gamma Exposure (GEX) by Strike
        print(f"\n--- Gamma Exposure (GEX) by Strike ---")
        gex_data = analyzer.gex_per_strike(option_chain_data)
        print(f"{'Strike':<10} {'Call GEX':<15} {'Put GEX':<15} {'Net GEX':<15} {'Abs GEX':<15}")
        print("-" * 75)
        total_net_gex = 0
        total_abs_gex = 0
        for strike in sorted(gex_data.keys()):
            data = gex_data[strike]
            total_net_gex += data['direction_gex']
            total_abs_gex += data['abs_gex']
            print(f"{strike:<10.2f} {data['call_gex']:<15.2f} {data['put_gex']:<15.2f} {data['direction_gex']:<15.2f} {data['abs_gex']:<15.2f}")

        print("-" * 75)
        print(f"{'TOTAL':<10} {'':<15} {'':<15} {total_net_gex:<15.2f} {total_abs_gex:<15.2f}")
        print(f"\nNet GEX Interpretation:")
        if total_net_gex > 0:
            print("  → Positive Net GEX: Market makers likely to sell into rallies and buy dips (stabilizing)")
        elif total_net_gex < 0:
            print("  → Negative Net GEX: Market makers likely to amplify price movements (volatile)")
        else:
            print("  → Zero Net GEX: Neutral gamma exposure")

    else:
        print(f"Failed to fetch option chain for ticker: {stock.get_symbol()}")

except Exception as e:
    print(f"An error has occured during the API test: {e}")
    import traceback
    traceback.print_exc()
    exit()
