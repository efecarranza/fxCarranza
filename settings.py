from decimal import Decimal
import os


ENVIRONMENTS = {
    "streaming": {
        "practice": "stream-fxpractice.oanda.com",
        "sandbox": "stream-sandbox.oanda.com"
    },
    "api": {
        "practice": "api-fxpractice.oanda.com",
        "sandbox": "api-sandbox.oanda.com"
    }
}

# CSV_DATA_DIR = os.environ.get('QSFOREX_CSV_DATA_DIR', None)
CSV_DATA_DIR = 'csv-generated'
OUTPUT_RESULTS_DIR = 'output-results'
# OUTPUT_RESULTS_DIR = os.environ.get('QSFOREX_OUTPUT_RESULTS_DIR', None)

DOMAIN = "practice"
STREAM_DOMAIN = ENVIRONMENTS["streaming"][DOMAIN]
API_DOMAIN = ENVIRONMENTS["api"][DOMAIN]
ACCESS_TOKEN = os.environ.get('OANDA_API_ACCESS_TOKEN', None)
ACCOUNT_ID = os.environ.get('OANDA_API_ACCOUNT_ID', None)

BASE_CURRENCY = "USD"
EQUITY = Decimal("100000.00")
