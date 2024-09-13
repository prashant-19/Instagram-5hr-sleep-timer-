import instaloader
import time
from instaloader.exceptions import TooManyRequestsException, ProfileNotExistsException

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
    
    except Exception as e:
        print(f"Error downloading profile {username}: {str(e)}")
        return True  


def download_profiles_with_rate_limiting(usernames):
    loader = instaloader.Instaloader()
    
    for username in usernames:
        success = False

        while not success:
            success = download_profile(loader, username)
            if not success:
                time.sleep(5 * 60 * 60) 
        
        print(f"Completed downloading profile: {username}")
        

if __name__ == "__main__":

    usernames = ["appliviu" , "rockstargames"]

    download_profiles_with_rate_limiting(usernames)
