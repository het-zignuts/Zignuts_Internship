import os
import requests

# bored_activity_resp=requests.get("https://bored-api.appbrewery.com/random")

# print("Response status code: ", bored_activity_resp.status_code)
# if bored_activity_resp.status_code == 200:
#     act_data = bored_activity_resp.json()
#     print(act_data)
# else:
#     print("Request failed:", bored_activity_resp.status_code)
#     print("Response text:", bored_activity_resp.text)


def api_call_wrapper(retries=3):
    try:
        for retries in range(retries):
            response=requests.get("https://bored-api.appbrewery.com/random")
            if response.status_code==200:
                return response.json()
            print("Reattempting...")
    except Exception as e:
        print("All connection attempts failed...\n", e)

data=api_call_wrapper(3)

print(data)