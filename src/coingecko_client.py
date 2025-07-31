from coingecko_sdk import Coingecko
from utils import load_config

config = load_config()

client = Coingecko(
    # pro_api_key=os.environ.get("COINGECKO_PRO_API_KEY"),
    demo_api_key=config["coin_gecko_key"], # Optional, for Demo API access
    environment="demo", # "pro"; "demo" to initialize the client with Demo API access
)

price = client.simple.price.get(
    vs_currencies="usd",
    ids="bitcoin",
)

print(price["bitcoin"])
