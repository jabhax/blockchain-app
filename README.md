**Blockchain-App**

**Commands**

**Activate the virtual environment**
- This runs the venv needed to start the servers on localhost.
```
source blockchain-env/bin/activate
```

**Install all packages**
- This installs the dependancies in the requirements.txt (see python-blockchain/requirements.txt for full list of packages).
```
pip install -r requirements.txt
```

**Run the tests**
- Runs all tests suites for the backend.
- Make sure to activate the virtual environment. (does not require server to be started)
```
python -m pytest backend/tests
```

**Run the application and API**
- Runs the server on http://localhost:5000.
- Make sure to activate the virtual environment.
```
python -m backend.app
```

**Run a peer instance**
- Exactly like the previous command to python -m backend.app but specifying the PEER=True to run server on a different localhost port.
- Make sure to activate the virtual environment.
```
export PEER=True && python -m backend.app
```
