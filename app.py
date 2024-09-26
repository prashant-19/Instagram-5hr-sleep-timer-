import instaloader
import time
import shutil
import os
from instaloader.exceptions import TooManyRequestsException, ProfileNotExistsException
import socket

def download_profile(loader, username):
    try:
        print(f"Attempting to download profile: {username}")

        
        loader.resume_prefix = username  
        loader.post_metadata_txt_pattern = ""  
        loader.save_metadata = False  

        loader.download_profile(username, profile_pic_only=False, fast_update=True)
        print(f"Successfully downloaded profile: {username}")

        resume_file = f"{username}.json.xz"
        if os.path.exists(resume_file):
            os.remove(resume_file)
            print(f"Removed resume file for {username}")

        return True
    except TooManyRequestsException:
        print("Rate limit reached, sleeping for 5 hours.")
        return False
    except ProfileNotExistsException:
        print(f"Profile {username} does not exist.")
        return True
    except (socket.timeout, TimeoutError):
        print("Timeout occurred, sleeping for 5 hours.")
        return False  
    except Exception as e:
        error_message = str(e)
        if "Please wait a few minutes before you try again" in error_message:
            print("Instagram is asking to wait, sleeping for 5 hours.")
            return False  
        else:
            print(f"Error downloading profile {username}: {error_message}")
            return True 

def zip_profile(username):
    profile_dir = f"./{username}"  
    zip_filename = f"./{username}.zip"  
    
    if os.path.isdir(profile_dir): 
        print(f"Zipping profile: {username}")
        shutil.make_archive(f"./{username}", 'zip', profile_dir)  
        print(f"Profile {username} successfully zipped as {zip_filename}")
    else:
        print(f"Directory {profile_dir} not found, unable to zip profile.")

def download_profiles_with_rate_limiting(usernames):
    loader = instaloader.Instaloader()

    for username in usernames:
        success = False
        while not success:
            success = download_profile(loader, username)
            if not success:
                print(f"Sleeping for 5 hours before retrying profile: {username}")
                for i in range(5 * 60 * 60):
                    print(f"Sleeping... {i+1} seconds", end='\r')  
                    time.sleep(1)  
        
        print(f"Completed downloading profile: {username}")
        zip_profile(username) 

if __name__ == "__main__":
    usernames = ["appliviu"]

    download_profiles_with_rate_limiting(usernames)
