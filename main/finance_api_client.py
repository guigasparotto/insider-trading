import http.client
import json
import logging
import traceback
from datetime import datetime


class YahooClient:

    def __init__(self, api_key):
        self._connection = http.client.HTTPSConnection("apidojo-yahoo-finance-v1.p.rapidapi.com")

        self._headers = {
            "X-RapidAPI-Key": f"{api_key}",
            "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
        }

    def __send_request(self, method_type, endpoint):
        self._connection.request(method_type, endpoint, headers=self._headers)
        return self._connection.getresponse()

    def __is_response_valid(self, response):
        response_code = response.getcode()
        if response_code == 200:
            logging.info(f"{response.reason}: Request successfully completed")
            return True
        elif response_code == 204:
            logging.warning(f"{response.reason}: No data found for specified parameters")
            return False
        elif response_code == 400:
            logging.error(f"{response.reason}: Please verify the parameters of the request")
            return False
        else:
            logging.info(response.reason)
            return False

    def get_insider_data_for_symbol(self, symbol, region, start_date, end_date):
        try:
            uri = f"/stock/v2/get-insider-transactions?symbol={symbol}&region={region}"
            response = self.__send_request("GET", uri)
            if not self.__is_response_valid(response):
                return []

            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except Exception as exception:
            logging.error(f"Please verify parameters used - "
                          f"symbol: {symbol}, region: {region}, start_date: {start_date}, end_date: {end_date}")
            traceback.print_exc()
            return []

        json_data = json.loads(response.read())
        transactions = json_data["insiderTransactions"]["transactions"]
        matched_transactions = []

        for t in transactions:
            trans_date = datetime.fromtimestamp(t["startDate"]["raw"])
            if start_date <= trans_date <= end_date:
                t["exchange"] = json_data["price"]["exchange"]
                t["currency"] = json_data["price"]["currency"]
                matched_transactions.append(t)

        return matched_transactions
