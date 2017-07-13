# Hawkeye (alpha)
A tool for monitoring machines in an intranet. 

## Features
1. The tool can run python script over any number of clients. 
2. The server loops across all clients asynchornously to run the given
script
3. Data transferred between the server and the clients is encrypted using RSA
s `PKCS1_OAEP` standards (asymmetric encryption/decryption using an RSA key pair)

## Assumptions
1. Clients config will be passed in one XML file
2. The server script will be excute either by hand or using a cronjob
3. Data encryption is Asymmetric. All clients have the public encryption key
4. All client nodes in the network have the dependencies needed for the client script to run successfully

## Installation Instructions
1. Install `virtualenv` by running this command: `pip install virtualenv` [refer to virtualenv docs](https://virtualenv.pypa.io/en/stable/installation/)

2. Create a new virtualenv: `virtualenv env_hawkeye -ppython3`

3. Install requirements: `pip install -r requirements`

4. Add hawkeye dir to python path: `export PYTHONPATH="${PYTHONPATH}:/path/to/hawkeye"`

## Usage

### Run the demo
1. Activate the virtualenv: `source /path/to/env_hawkeye/bin/activate`
2. Change credentials in `main()` function in `hawkeye.py` to valid credentials
3. Run `python /path/to/hawkeye/source/hawkeye.py`

IMPORTANT NOTE: make sure the requirements for the client script are met on all clients to be monitored as mentioned in the Assumptions section above.

### Use Hawkeye module

1. Create a config file with all your clients credentials. Use the following example as a reference:
```
<root>
    <client ip="127.0.0.1" port="22" username="user" password="password" mail="asa@asda.com">

        <alert type="memory" limit="50%" />
        <alert type="cpu" limit="20%" />
    </client>

    <client ip="127.0.0.1" port="22" username="user" password="pasword" mail="asa@asda3.com">

        <alert type="memory" limit="50%" />
        <alert type="cpu" limit="20%" />
    </client>
</root>
```
2. Import `hawkeye` into your application:
```
from hawkeye.source.hawkeye import Hawkeye

hawkeye = Hawkeye(xml_config) # config created in step 1
hawkeye.run()

```

## Enhancements/Requirements:
(Enhancements that weren't implemented due to lack of time)

1. More unit tests
2. Integration tests
3. Mail Client `emailer.py` that supports multiple email protocols
4. Default alert limit for different metrics
5. OS-specific metrics and statistics
6. Run multiple scripts
7. Add Async. event loop to enhance performance
