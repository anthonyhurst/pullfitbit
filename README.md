# pullfitbit
The purpose of this application is to allow you to pull down your fitbit data with little to no effort.
# Requirements
You will likely need to install
* pandas
* matplotlib
* requests_oauthlib

# Usage
This is still a work in progress but to authorize:
```bash
python3 pull.py $APPID
```
You will then need to go through the prompts and instructions.

Once you have a token you can then pull your data by running:
```bash
python3 pull.py $APPID --use_token_file
```

