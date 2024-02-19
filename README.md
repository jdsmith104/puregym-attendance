# puregym-attendance

puregym-attendance is a Python client to query the PureGym Mobile API for live gym attendance statistics.

## Dependancies

TextDistance -- pip install textdistance

## Setup
``` sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt 
```

Create `credentials.json` in the root directory. This is picked up by `server.py` and should not be tracked.
``` json
// credentials.json
{
    "email": "john@email.com",
    "pin": "31415926"
}
```

## Running the server
``` sh
python3 server.py
```

## Getting the list of all gyms
``` sh
python3 update_all_gyms.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
