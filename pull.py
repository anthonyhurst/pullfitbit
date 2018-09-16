import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import MobileApplicationClient
import argparse
import datetime
import json

def get_endpoint(fitbit, url, filename, headers):
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    result = fitbit.get(url.format(DATE=date_str), headers=headers)
    json_result = json.loads(result.content)
    output = json.dumps(json_result, indent=4, sort_keys=True)
    fh = open(filename, "w")
    fh.write(output + "\n")
    fh.close()

def authorize(client_id, client, scope=None):
    fitbit = OAuth2Session(client_id, client=client, scope=scope)
    auth_url = "https://www.fitbit.com/oauth2/authorize"
    auth_url, state = fitbit.authorization_url(auth_url, expires_in=31536000)
    print("Visit this url to authorize: {}".format(auth_url))
    callback_url = input("Please paste the URL you were redirected to here: ")
    result=fitbit.token_from_fragment(callback_url)
    token = result["access_token"]
    print("Please use this in the future!  Token={}".format(token))
   
    token_saver(result)

    return fitbit


def token_saver(token):
    output = json.dumps(token, indent=4, sort_keys=True)
    fh = open("token.txt", "w")
    fh.write(str(output) + "\n")
    fh.close()
    


def get_token_from_file():
    fh = open("token.txt", "r")
    content = fh.read()
    fh.close()
    result = content.strip()
    obj = json.loads(result)
    return obj["access_token"]
    



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pull your data from fitbit")
    parser.add_argument("client_id", help="Supply the client_id of the application.")
    parser.add_argument("--token", default=None, help="If you already have a token, supply it here.")
    parser.add_argument("--use_token_file", default=False, action="store_true", help="If you already have a token, supply it here.")
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
    if args.token is None and not args.use_token_file:
        fitbit = authorize(client_id, client, scope)
    else:
        if args.token is not None:
            token = {
                    "access_token": args.token,
                    "token_type": "Bearer",
                    }
        else:
            token = {
                    "access_token": get_token_from_file(),
                    "token_type": "Bearer",
                    }
        fitbit = OAuth2Session(client_id, client=client, scope=scope, token=token)




    get_endpoint(fitbit, "https://api.fitbit.com/1/user/-/body/log/weight/date/{DATE}/1m.json", "weight.json", headers=headers)
    get_endpoint(fitbit, "https://api.fitbit.com/1/user/-/activities/steps/date/{DATE}/1d/15min.json", "steps.json", headers=headers) # note that the detail level only works for Personal OAuth or Fitbit approved apps
    get_endpoint(fitbit, "https://api.fitbit.com/1/user/-/activities/heart/date/{DATE}/1d/1sec.json", "heart.json", headers=headers) # note that the detail level only works for Personal OAuth or Fitbit approved apps
    get_endpoint(fitbit, "https://api.fitbit.com/1.2/user/-/sleep/date/{DATE}.json", "sleep.json", headers=headers) 

