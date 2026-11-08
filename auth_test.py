import base64
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

auth_user = os.environ.get("AUTH_USER")
auth_pass = os.environ.get("AUTH_PASS")

if not auth_user or not auth_pass:
    sys.exit("Missing AUTH_USER or AUTH_PASS environment variables!")

credentials = base64.b64encode(
    f"{auth_user}:{auth_pass}".encode("utf-8")
).decode("ascii")

url = (
    "https://httpbin.org/basic-auth/"
    f"{quote(auth_user, safe='')}/{quote(auth_pass, safe='')}"
)
request = Request(url, headers={"Authorization": f"Basic {credentials}"})

print("Attempting authentication...")

try:
    with urlopen(request, timeout=30) as response:
        result = json.load(response)
        print("Authentication successful!")
        print("Response status:", response.status)
        print("Authenticated:", result.get("authenticated"))
except HTTPError as error:
    sys.exit(f"Authentication failed: HTTP {error.code}")
except (URLError, ValueError):
    sys.exit("Authentication request failed.")