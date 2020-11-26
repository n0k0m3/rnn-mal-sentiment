from utils.token_gen import MAL_auth
import os

MAL_auth=MAL_auth()

if not os.path.isfile("token.json"):
    print(">>> Token not found <<<")
    access_token = MAL_auth.initialize()
else:
    print(">>> Token found <<<")
    access_token = MAL_auth.refresh_token("token.json")

