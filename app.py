import instaloader
import time
from instaloader.exceptions import TooManyRequestsException, ProfileNotExistsException
import socket

def download_profile(loader, username):
    try:
        print(f"Attempting to download profile: {username}")
        loader.download_profile(username, profile_pic_only=False)
        print(f"Successfully downloaded profile: {username}")
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

if __name__ == "__main__":

    usernames = ["appliviu"]

    download_profiles_with_rate_limiting(usernames)
