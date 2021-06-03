### Installation tests
 ```
git clone https://github.com/GenesisKernel/genesis-tests.git tests
virtualenv -p python3 tests
cd tests
source bin/activate
pip install -r requirements.txt
```

### Example start test
 ```
py.test -s block_chain_test.py
 ```

 ### hostConfig.json
For each node:
* url:url of api
* private_key:private key of user
* dbHost: host name of data base
* dbName: name of data base
* login: login of data base,
* pass: password of data base,
* time_wait_tx_in_block:time in seconds to wait, while transaction will be writed to block

 ### Config
 * url:url of api
* private_key:private key of user
* time_wait_tx_in_block:time in seconds to wait, while transaction will be writed to block






D:\dev\Scoop\apps\python\3.8.6\Lib\site-packages\genesis-blockchain-api-client>pip install -r requirements.txt
D:\dev\Scoop\apps\python\3.8.6\Lib\site-packages\genesis-blockchain-api-client>python setup.py install

D:\project\gachain\lib.gachain.io\lahaer-gachain-test-performance>pip3 install -U --force-reinstall --no-binary :all: gevent --use-feature=2020-resolver
D:\project\gachain\lib.gachain.io\lahaer-gachain-test-performance>pip install -r requirements.txt
D:\project\gachain\lib.gachain.io\lahaer-gachain-test-performance>locust -f gac_sendtokens.py --no-web -c 1 -r 1




