import os
import dropbox
import requests
import configparser

class DropboxUploader:
    def __init__(self):
        self.credentials_directory = "credentials.ini"
        self.dropbox_directory = "/archives"

        self.access_token = self.read_credentials_value("Authentication", "access_token")
        self.dbx = dropbox.Dropbox(self.access_token)

    def read_credentials_value(self, section, key):
        config = configparser.ConfigParser()
        config.read(self.credentials_directory)

        try:
            return config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            print(f"read_credentials_value function: Error reading config value: {e}")
            return None

    def update_credentials_key_value(self, section, key, value):
        config = configparser.ConfigParser()
        config.read(self.credentials_directory)
        config.set(section, key, value)

        with open(self.credentials_directory, 'w') as config_file:
            config.write(config_file)
            print(f"Key '{key}' value updated successfully in section '{section}'")

    def generate_new_access_token(self, app_key, app_secret, refresh_token):
        url = "https://api.dropbox.com/oauth2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": app_key,
            "client_secret": app_secret,
        }

        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            print("generate_new_access_token function: Failed to get a new access token.")
            print(f"generate_new_access_token function: Status code: {response.status_code}")
            print(f"generate_new_access_token function: Response: {response.text}")
            return None

    def check_token_validity(self):
        try:
            self.dbx.files_list_folder('')
            print("Token is valid")
        except dropbox.exceptions.AuthError:
            print("Token is expired, generating new access token ...")
            app_key = self.read_credentials_value("Authentication", "app_key")
            app_secret = self.read_credentials_value("Authentication", "app_secret")
            refresh_token = self.read_credentials_value("Authentication", "refresh_token")
            new_token = self.generate_new_access_token(app_key, app_secret, refresh_token)

            if new_token:
                self.update_credentials_key_value("Authentication", "access_token", new_token)
                self.access_token = new_token
                self.dbx = dropbox.Dropbox(self.access_token)
        except dropbox.exceptions.DropboxException as e:
            print("check_token_validity function: An error occurred while checking the token:", e)

    def upload_files(self, local_file_path):
        try:
            self.check_token_validity()
            file_name = os.path.basename(local_file_path)
            dropbox_path = f"{self.dropbox_directory}/{file_name}"

            with open(local_file_path, "rb") as file:
                self.dbx.files_upload(file.read(), dropbox_path, mode=dropbox.files.WriteMode("overwrite"))
                print(f"File '{file_name}' uploaded successfully to Dropbox.")
                
                try:
                    shared_link_metadata = self.dbx.sharing_create_shared_link_with_settings(dropbox_path)
                except dropbox.exceptions.ApiError as e:
                    if isinstance(e.error, dropbox.sharing.CreateSharedLinkWithSettingsError) and e.error.is_shared_link_already_exists():
                        shared_link_metadata = self.dbx.sharing_list_shared_links(path=dropbox_path).links[0]
                    else:
                        raise

                shared_link_url = shared_link_metadata.url
                download_link = shared_link_url[:-1] + '1'
                print(f"Download link: {download_link}")
                return download_link

        except Exception as e:
            print("upload_files function: An error occurred:", e)
            return None

def update_short_link(api_token, alias, new_url):
    url = f"https://goo.su/api/links/edit/{alias}"
    headers = {
        "Content-Type": "application/json",
        "x-goo-api-token": api_token
    }
    
    payload = {
        "url": new_url
    }
    
    payload = {k: v for k, v in payload.items() if v is not None}

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def upload_and_update_link(file_path, alias):
    dropbox_uploader = DropboxUploader()
    download_link = dropbox_uploader.upload_files(file_path)

    if download_link:
        api_token = "3crKqpO2BG4AKGzQOMQ4WaWiq9i0hj0tsB9mrEihprYporen4IC9kJp7BHs3"
        response = update_short_link(api_token, alias, download_link)
        
        if response and response.get("successful"):
            print("Short link successfully updated")
            print("Updated link details:", response["link"])
            return response["link"]
        else:
            print("Failed to update the short link")
            return None
    else:
        print("Failed to upload the file to Dropbox")
        return None
