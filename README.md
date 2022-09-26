# insider-trading 

This is a personal project to practice my python skills. The project follows an object orientation approach and at the moment includes the following files:
* *finance_api_client.py* - used to query the [Yahoo Finance API](https://rapidapi.com/apidojo/api/yh-finance/) for a specific symbol and country code, which returns insider transaction data. The data is filtered given the initial and end dates provided by the method caller.
* *config.ini* - to use the api you will need an API key, which can be created using the above API link
* *transaction_parser.py* - this class contains a few methods to parse the data returned by the API call into something useful. The class includes methods to filter the data, removing fields that might not be useful for the intended purposes, and also to convert the list of dictionaries received in a list of objects, which can later be used for more easily manipulate the data.
* *test_transaction_parser.py* - includes unit tests for the *TransactionParser* class
* *pytest.ini* - configuration file that contains markers used by pytest to identify tests - these markers are used in the test classes as annotations in each of the tests

### Packages And Versions

The project was created and tested with [Python 3.8](https://www.python.org/downloads/release/python-380/), and the following additional packages were used:
* [pytest 7.1.3](https://pypi.org/project/pytest/) - for unit testing
* [pandas 1.5.0](https://pypi.org/project/pandas/) - to generate the table that contains insider trading information

### Prerequisites
* Clone the repository to your local machine
```
git clone https://github.com/guigasparotto/insider-trading.git
```

* An api key is required. If you don't have one, go to [Yahoo Finance API](https://rapidapi.com/apidojo/api/yh-finance/) and subscribe for free to get one

### Running the Program

Once you created your API key, update the config.ini file by replacing the filed description with your key, then either:
* run main/main.py from you preferred IDE - [PyCharm Community](https://www.jetbrains.com/pycharm/download/) was used during development
* run it from command line - make sure [Python 3.8](https://www.python.org/downloads/release/python-380/) is installed, then in navigate to the main folder and run 
```
python main.py 
```
* enter the desired symbol, country code and date ranges as exemplified below:
```
Please enter the desired RIC code: KWS.L
Please enter the 2-digit country code: GB
Please enter the initial date for the period (yyyy-mm-dd): 2022-01-01
Please enter the end date for the period (yyyy-mm-dd): 2022-12-31
```
* if data for the period exists, you should see a table as below
```
  filerName                              transactionText ownership   startDate   value   shares exchange currency
  Doe (Jon)  Exercise of Option at price 0.01 per share.         D  2022-01-22      10       10      LSE      GBp
  Doe (Jon)               Sold at price 26.30 per share.         D  2022-09-22    1000     1000      LSE      GBp

```

### Running the Tests

In order to run the unit tests, **no API key is required**, given the test data is generated in the test class and provided to the TransactionParser class. Once again, that are 2 main options to run the tests:
* from the IDE - using PyCharm, double-click on the *test_transaction_parser.py*, then right-click on the class name - *TestTransactionParser* - and select one of the available option (run or debug tests)
* from the command line, run one of the commands below (-v for verbose, will print additional information about the tests performed)
```
pytest test_transaction_parser.py
pytest test_transaction_parser.py -v
```
* you can also filter the tests using one of the available markers, configured in pytest.ini - filtertransactions / transactionobjects
```
pytest -m filtertransactions test_transaction_parser.py
pytest -m transactionobjects test_transaction_parser.py -v
```

### Additional Notes

* There are currently no tests for the API client code (YahooClient class in the finance_api_client.py file)
* There are some error handling in the YahooClient class, but it requires more testing
* No API key is required to run the unit tests 