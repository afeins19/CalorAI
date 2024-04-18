import http.cookiejar as cookiejar
import json
import browsercookie
import wearipedia  # Make sure this module is properly documented as it's not a standard library
from . import clean_data

class MfpClient:
    def __init__(self) -> None:
        # attempting to find the cookies 
        self.jar = cookiejar.CookieJar()
        if not self.download_cookies():
            raise Exception("Failed to download cookies")

        if not self.set_cookies():
            raise Exception("Failed to set cookies")

        self.device = self.make_and_auth_device() # creating a virtual device to interface with mfp 

        if not self.device:
            raise Exception("Failed to authenticate device")
        self.data = None

    def download_cookies(self):
        # getting the users cookies 
        try:
            cookies = browsercookie.load()
            cookie_list = []

            for cookie in cookies:
                cookie_dict = cookie.__dict__
                cookie_dict['rest'] = cookie_dict['_rest']
                del cookie_dict['_rest']
                cookie_list.append(cookie_dict)

            with open('cookies.json', 'w') as f:
                json.dump(cookie_list, f)
            return True
        except Exception as e:
            print(f"Error downloading cookies: {e}")
            return False

    def set_cookies(self):
        try:
            with open('cookies.json', 'r') as f:
                data = json.load(f)

            for cookie in data:
                self.jar.set_cookie(cookiejar.Cookie(**cookie))
            return True
        except Exception as e:
            print(f"Error setting cookies: {e}")
            return False

    def make_and_auth_device(self):
        # use cookies to estabblish connection between virtual device and mfp 
        try:
            device = wearipedia.get_device("myfitnesspal/myfitnesspal")
            device.authenticate({'cookies': self.jar})
            return device
        except Exception as e:
            print(f"Error authenticating device: {e}")
            return None

    def get_data(self, start_date, end_date):
        # pulling data from mfp 
        params = {"start_date": start_date, "end_date": end_date}
        if self.device:
            try:
                user_data = {meal: self.device.get_data(meal, params=params) for meal in ["goals", "lunch", "breakfast", "dinner", "snacks"]}
                self.data = user_data
            except Exception as e:
                print(f"Error retrieving data: {e}")

    def clean_data(self): 
        # formattting data for JSON compatability 
        if self.data:
            return {name: clean_data(vals) for name, vals in self.data.items()}
        return None

    def export(self):
        # saving data locally for later 
        try:
            with open("core/userdata/data.json", "w") as f:
                json.dump(self.data, f)
        except Exception as e:
            print(f"Error exporting data: {e}")
