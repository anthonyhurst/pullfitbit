import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import MobileApplicationClient
import argparse
import datetime
import json

parser = argparse.ArgumentParser(description="Pull your data from fitbit")
parser.add_argument('client_id', help='Supply the client_id of the application.')
parser.add_argument('--token', default=None, help='If you already have a token, supply it here.')
args = parser.parse_args()

client_id = args.client_id

scope = [
        "activity",
        "weight",
        "heartrate",
        "nutrition",
        "sleep",
        ]

headers = {
        "Accept-Language": "en_US",
        }

client = MobileApplicationClient(client_id)
if args.token is None:
    fitbit = OAuth2Session(client_id, client=client, scope=scope)
    auth_url = "https://www.fitbit.com/oauth2/authorize"
    auth_url, state = fitbit.authorization_url(auth_url)
    print("Visit this url to authorize: {}".format(auth_url))
    callback_url = input("Please paste the URL you were redirected to here: ")
    result=fitbit.token_from_fragment(callback_url)
    token = result["access_token"]
    print("Please use this in the future!  Token={}".format(token))


    fh = open("token.txt", "w")
    fh.write(str(token) + "\n")
    fh.close()

else:
    token = {
            "access_token": args.token,
            "token_type": "Bearer",
            }
    fitbit = OAuth2Session(client_id, client=client, scope=scope, token=token)



date_str = datetime.datetime.now().strftime("%Y-%m-%d")

weight_result = fitbit.get("https://api.fitbit.com/1/user/-/body/log/weight/date/{}/1m.json".format(date_str), headers=headers)

json_result = json.loads(weight_result.content)
output = json.dumps(json_result, indent=4, sort_keys=True)



fh = open("weight.json", "w")
fh.write(str(output) + "\n")
fh.close()

