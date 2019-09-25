# Install PIP REQUESTS & ASYNCIO
# REGISTER YOUR APPLICATION ON AZURE ACTIVE DIRECTORY AND GATHER YOUR TENANT ID, CLIENT ID, CLIENT SECRET
# THIS CODE WILL AUTHENTICATE YOUR APPLICATION AND GET YOUR USER ID, THE CODE WILL CONTINOUSLY KEEP REFRESHING ACCESS TOKEN 
# FOR CONTINUED ACCESS



import requests
import asyncio

tenant_id = '#USE YOUR TENANT ID'
client_id = '#USE YOUR CLIENT ID'
client_secret = 'USE YOUR CLIENT SECRET'
scope = 'https://graph.microsoft.com/.default'

access_token = ''
user_id = ''


async def get_token():
    global access_token, expires_in
    url = "https://login.microsoftonline.com/" + tenant_id + "/oauth2/v2.0/token"
    payload = "grant_type=client_credentials&" \
              f"client_id={client_id}&" \
              f"client_secret={client_secret}&" \
              f"scope={scope}"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Host': "login.microsoftonline.com",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }
    while True:
        print("Getting Token")
        try:
            response = requests.request("POST", url, data=payload, headers=headers)  # print(response.text)
            json_obj = response.json()
            access_token = json_obj["access_token"]
            expires_in = json_obj["expires_in"]
            print(f"access_token = {access_token}")
            print(f"expires_in = {expires_in}")
        except requests.exceptions.HTTPError as err:
            print(f"HTTPError : {err}")
        except requests.exceptions.Timeout:
            print("Request TimeOut")
        except requests.exceptions.TooManyRedirects:
            print("Bad URL too many redirects")
        except requests.exceptions.RequestException:
            print("Bad Request")
        await asyncio.sleep((expires_in-5))


async def get_user():
    global user_id
    url = "https://graph.microsoft.com/v1.0/users"
    headers = {
        'Authorization': f"{access_token}",
        'Cache-Control': "no-cache",
        'Host': "graph.microsoft.com",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }
    try:
        response = requests.request("GET", url, headers=headers)
        json_obj = response.json()
        user_id = json_obj["value"][0]["id"]
        print(user_id)
    except requests.exceptions.HTTPError as err:
        print(f"HTTPError : {err}")
    except requests.exceptions.Timeout:
        print("Request TimeOut")
    except requests.exceptions.TooManyRedirects:
        print("Bad URL too many redirects")
    except requests.exceptions.RequestException:
        print("Bad Request")

async def main():
    await asyncio.gather(get_token(), get_user())

if __name__ == '__main__':
    asyncio.run(main())
