class TransactionParser:
    def __init__(self, data_set):
        self.__data_set = [] if data_set is None else data_set
        self.__filtered_data = None
        self.__transaction_objects = None

    def get_filtered_data(self):
        if self.__filtered_data is None:
            self.__filtered_data = self.__filter_dictionary()
        return self.__filtered_data

    def get_transaction_objects_list(self):
        if self.__transaction_objects is None:
            self.__transaction_objects = self.__parse_to_objects()
        return self.__transaction_objects

    def __filter_dictionary(self):
        transactions = []
        for record in self.__data_set:
            self.__remove_unrequired_fields(record)
            record["startDate"] = record["startDate"]["fmt"]
            record["shares"] = record["shares"]["raw"]
            value = record.get("value")
            record["value"] = 0 if value is None else record["value"]["raw"]
            transactions.append(record)
        return transactions

    def __remove_unrequired_fields(self, record):
        record.pop("moneyText", None)
        record.pop("filerRelation", None)
        record.pop("filerUrl", None)
        record.pop("maxAge", None)
        record.pop("__len__", None)
        return record

    def __parse_to_objects(self):
        transactions = []
        for record in self.get_filtered_data():
            transactions.append(
                Transaction(
                    record["filerName"],
                    record["ownership"],
                    record["startDate"],
                    float(record["value"]),
                    int(record["shares"]),
                    record["currency"],
                    record["exchange"]
                )
            )
        return transactions


class Transaction:
    def __init__(self, filer_name, ownership, start_date, value, shares, currency, exchange):
        self.filer_name = filer_name
        self.ownership = ownership
        self.start_date = start_date
        self.value = value
        self.shares = shares
        self.currency = currency
        self.exchange = exchange
        self.total = value * shares
