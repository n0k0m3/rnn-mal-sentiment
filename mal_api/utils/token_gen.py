import json
import requests
import secrets
import getpass

class MAL_auth:
    def __init__(self,*args):
        if args:
            credpath = args
        else:
            credpath = "credentials.json"
        with open(credpath,"r") as f:
            client = json.load(f)
            self.CLIENT_ID = client["CLIENT_ID"]
            self.CLIENT_SECRET = client["CLIENT_SECRET"]


    # 1. Generate a new Code Verifier / Code Challenge.
    @staticmethod
    def get_new_code_verifier() -> str:
        token = secrets.token_urlsafe(100)
        return token[:128]


    # 2. Print the URL needed to authorise your application.
    def print_new_authorisation_url(self,code_challenge: str):

        url = f'https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={self.CLIENT_ID}&code_challenge={code_challenge}'
        print(f'Authorise your application by clicking here: {url}\n')


    # 3. Once you've authorised your application, you will be redirected to the webpage you've
    #    specified in the API panel. The URL will contain a parameter named "code" (the Authorisation
    #    Code). You need to feed that code to the application.
    def generate_new_token(self,authorisation_code: str, code_verifier: str) -> dict:

        url = 'https://myanimelist.net/v1/oauth2/token'
        data = {
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
            'code': authorisation_code,
            'code_verifier': code_verifier,
            'grant_type': 'authorization_code'
        }

        response = requests.post(url, data)
        response.raise_for_status()  # Check whether the requests contains errors

        token = response.json()
        response.close()
        print('Token generated successfully!')

        with open('token.json', 'w') as file:
            json.dump(token, file, indent = 4)
            print('Token saved in "token.json"')

        return token


    # 4. Test the API by requesting your profile information
    @staticmethod
    def print_user_info(access_token: str):
        url = 'https://api.myanimelist.net/v2/users/@me'
        response = requests.get(url, headers = {
            'Authorization': f'Bearer {access_token}'
            })
        
        response.raise_for_status()
        user = response.json()
        response.close()

        print(f"\n>>> Greetings {user['name']}! <<<\n")

    def initialize(self):
        code_verifier = code_challenge = self.get_new_code_verifier()
        self.print_new_authorisation_url(code_challenge)

        authorisation_code = getpass.getpass('Copy-paste the Authorisation Code/URL: ').split(r"oauth?code=")[-1].strip()
        token = self.generate_new_token(authorisation_code, code_verifier)

        self.print_user_info(token['access_token'])

        return token['access_token']

    def request_new_token(self,refresh_token):
        url = 'https://myanimelist.net/v1/oauth2/token'
        data = {
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        response = requests.post(url, data)
        response.raise_for_status()  # Check whether the requests contains errors

        token = response.json()
        response.close()
        print('Token refreshed successfully!')

        with open('token.json', 'w') as file:
            json.dump(token, file, indent = 4)
            print('New token saved in "token.json"')

        return token


    def refresh_token(self,tokenpath):
        with open(tokenpath,"r") as f:
            token = json.load(f)
        refresh_token=token['refresh_token']
        token = self.request_new_token(refresh_token)
        self.print_user_info(token['access_token'])
        return token["access_token"]
