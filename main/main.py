from configparser import ConfigParser
from finance_api_client import YahooClient
from transaction_parser import TransactionParser
import pandas as pd

config = ConfigParser()
config.read("config.ini")
api_key = config["apiconfig"]["rapid_api_key"]
yahoo = YahooClient(api_key)


def print_transaction_table_for_symbol(symbol, country, start_date, end_date):
    kws_data = yahoo.get_insider_data_for_symbol(symbol, country, start_date, end_date)
    transact_parser = TransactionParser(kws_data)
    kws_data_filtered = transact_parser.get_filtered_data()
    frame = pd.DataFrame(kws_data_filtered)
    print(frame.to_string())


escape = None
while escape != "n":
    symbol = input(f"Please enter the desired RIC code: ")
    country_code = input("Please enter the 2-digit country code: ")
    start_date = input("Please enter the initial date for the period (yyyy-mm-dd): ")
    end_date = input("Please enter the end date for the period (yyyy-mm-dd): ")

    print_transaction_table_for_symbol(symbol, country_code, start_date, end_date)
    escape = input("Request another symbol? ('n' to quit or enter any other value to continue: ")
