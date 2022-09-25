import pytest
import names

from transaction_parser import TransactionParser


class TestTransactionParser:

    @pytest.fixture
    def parser(self):
        data = None
        parser = TransactionParser(data)
        return parser

    @pytest.mark.skip(reason="Skipped for demonstration")
    def test_sample_skippable_test(self):
        return

    @pytest.mark.transactions
    def test_get_filtered_data_when_empty_data_provided_returns_empty_list(self, parser):
        assert parser.get_filtered_data() == []

    @pytest.mark.transactions
    def test_get_filtered_data_when_valid_data_provided_returns_filtered_data(self):
        test_data = self.__create_test_data(1)
        parser = TransactionParser(test_data)
        expected_data = [
            {
                "filerName": "Hauck (Jon)",
                "transactionText": "Bought at price 0.01 per share.",
                "ownership": "D",
                "startDate": "2022-09-16",
                "value": 4,
                "shares": 410,
                "exchange": "LSE",
                "currency": "GBp"
            }]
        assert parser.get_filtered_data() == expected_data

    @pytest.mark.transactions
    @pytest.mark.parametrize('records, result', [
        (0, 0),
        (1, 1),
        (100, 100)
    ])
    def test_get_filtered_data_returns_correct_number_of_records(self, records, result):
        test_data = self.__create_test_data(records)
        parser = TransactionParser(test_data)
        transaction_list = parser.get_filtered_data()
        assert len(transaction_list) == result

    @pytest.mark.transactions
    def test_get_transaction_objects_list_when_empty_data_provided_returns_empty_list(self):
        data = None
        parser = TransactionParser(data)
        assert parser.get_transaction_objects_list() == []

    @pytest.mark.transactions
    def test_get_transaction_objects_list_when_valid_data_provided_returns_objects_list(self):
        test_data = self.__create_test_data(1)
        parser = TransactionParser(test_data)
        transaction_list = parser.get_transaction_objects_list()
        transaction = transaction_list[0]
        assert transaction.filer_name == "Hauck (Jon)"
        assert transaction.ownership == "D"
        assert transaction.start_date == "2022-09-16"
        assert transaction.value == 4
        assert transaction.shares == 410
        assert transaction.currency == "GBp"
        assert transaction.exchange == "LSE"
        assert len(transaction_list) == 1

    @pytest.mark.transactions
    @pytest.mark.parametrize('records, result', [
        (0, 0),
        (1, 1),
        (100, 100)
    ])
    def test_get_transaction_objects_returns_correct_number_of_records(self, records, result):
        test_data = self.__create_test_data(records)
        parser = TransactionParser(test_data)
        transaction_list = parser.get_transaction_objects_list()
        assert len(transaction_list) == result

    def __create_test_data(self, num_records):
        data = []
        for i in range(num_records):
            record = self.__generate_test_record()
            data.append(record)
        return data

    # TODO: to auto-generate the main parameters that will be later checked:
    # filerName, transactionText, ownership, startDate, value, shares
    # then auto-generate the expected filtered record to be compared in the tests above,
    # this will make it possible to validate multiple records at once
    # 2 global lists could be used for that - input data and expected data, which would be
    # accessed and cleaned by the tests that use them
    def __generate_test_record(self):
        filerName = names.get_full_name()
        record = {
            "filerName": f"{filerName}",
            "transactionText": "Bought at price 0.01 per share.",
            "moneyText": "",
            "ownership": "D",
            "startDate": {
                "raw": 1663286400,
                "fmt": "2022-09-16"
            },
            "value": {
                "raw": 4,
                "fmt": "4",
                "longFmt": "4"
            },
            "filerRelation": "",
            "shares": {
                "raw": 410,
                "fmt": "410",
                "longFmt": "410"
            },
            "filerUrl": "",
            "maxAge": 1,
            "exchange": "LSE",
            "currency": "GBp"
        }
        return record
