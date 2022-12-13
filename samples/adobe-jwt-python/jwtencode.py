import datetime
import jwt
import requests
from urllib.parse import urlencode

# CONFIG DATA - update these items
ORG_ID = "Your organization ID, e.g. 12345@AdobeOrg"
CLIENT_ID = "Your client ID aka API Key"
CLIENT_SECRET = "Your client Secret"
TECH_ACCT_ID = "The ID of the technical account associated with the integration"
PRIV_KEY_PATH = "private.key" # update with full path to your private key if needed
# list of scope URI strings - refer to the page for your credentials in the Developer Console
# this will differ depending on which services are associated with the credentials
# example: SCOPES = ["https://ims-na1.adobelogin.com/s/ent_user_sdk"]
SCOPES = []

# prepare JWT payload
jwt_payload = {
    "iss": ORG_ID,
    "sub": TECH_ACCT_ID,
    "aud": CLIENT_ID,
    "aud": f"https://ims-na1.adobelogin.com/c/{CLIENT_ID}",
    "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
}

# add scope claims to payload
for scope in SCOPES:
    jwt_payload[scope] = True

private_key = open(PRIV_KEY_PATH).read()

# Encode the jwt with the private key
jwt_token = jwt.encode(jwt_payload, private_key, algorithm='RS256')

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Cache-Control": "no-cache",
}

# encodw access request parameters
body = urlencode({
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "jwt_token": jwt_token
})

auth_url = 'https://ims-na1.adobelogin.com/ims/exchange/jwt'

res = requests.post(auth_url, headers=headers, data=body)

print(res.json()["access_token"])
