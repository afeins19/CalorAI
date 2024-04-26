import http.cookiejar as cookiejar
import json
import browsercookie
import wearipedia  
from selenium import webdriver 

# formatting timestamps to work with JSON 

def datacleanup(data):
  res = []
  for d in data:
    if 'date' in d:
      d['date'] = str(d['date'])
    if type(d)==list:
      if 'day' in d[0]:
        d[0]['day'] = str(d[0]['day'])
      if 'date' in d[0]:
        d[0]['date'] = str(d[0]['date'])
    res.append(d)
  return res

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

    def get_webdriver():
        pass

    def download_cookies(self):
        # getting the users cookies 
        try:
            driver = webdriver.Firefox()
            driver.get("https://www.myfitnesspal.com")
            
            cookies = driver.get_cookies()
            cookie_list = []

            # testing cookie retrieval
            print(f"Cookies: {cookies}")

            driver.quite()

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
            if not device:
                print("Device Retrieval Failed - No Device")
                return None
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


# test the module functionality if we run just this module 
if __name__ == '__main__':
    # Create an instance of the MfpClient
    mfp_client = MfpClient()

    # Example parameters for testing - adjust these as necessary
    start_date = "2024-01-01"
    end_date = "2024-01-31"

    try:
        # Test downloading cookies (assuming this should normally be run first)
        mfp_client.download_cookies()
        print("Cookies downloaded successfully.")

        # Set cookies from the downloaded data
        mfp_client.set_cookies()
        print("Cookies are set successfully.")

        # Authenticate device or session based on cookies
        device = mfp_client.make_and_auth_device()
        if device:
            print("Device authenticated successfully.")
        
        # Fetch some data with the MfpClient
        mfp_client.get_data(start_date, end_date)
        print("Data fetched successfully.")
        print("Fetched data:", mfp_client.data)

        # Clean the data
        cleaned_data = mfp_client.clean_data()
        print("Data cleaned successfully.")
        print("Cleaned data:", cleaned_data)

        # Optionally export the data
        mfp_client.export()
        print("Data exported successfully.")

    except Exception as e:
        print("An error occurred:", str(e))
