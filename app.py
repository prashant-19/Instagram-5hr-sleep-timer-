import instaloader
from datetime import datetime
import time
import shutil
import os
from instaloader.exceptions import TooManyRequestsException, ProfileNotExistsException
import socket

START_DATE = datetime(2024,11,7)  # Example: datetime(2023, 1, 1) or None
END_DATE = None    # Example: datetime(2024, 1, 1) or None

def download_profile(loader, username):
    try:
        print(f"Attempting to download profile: {username}")
        
        loader.resume_prefix = username  
        loader.post_metadata_txt_pattern = "" 
        loader.save_metadata = False  
        
        profile = instaloader.Profile.from_username(loader.context, username)
        
        for post in profile.get_posts():
            post_date = post.date

            if START_DATE and END_DATE:
                if START_DATE <= post_date <= END_DATE:
                    print(f"Downloading post from {post_date}: {post.url}")
                    loader.download_post(post, target=username)
                else:
                    print(f"Skipping post from {post_date}, outside of date range.")
            elif START_DATE:
                if post_date >= START_DATE:
                    print(f"Downloading post from {post_date}: {post.url}")
                    loader.download_post(post, target=username)
                else:
                    print(f"Skipping post from {post_date}, before START_DATE.")
            elif END_DATE:
                if post_date <= END_DATE:
                    print(f"Downloading post from {post_date}: {post.url}")
                    loader.download_post(post, target=username)
                else:
                    print(f"Skipping post from {post_date}, after END_DATE.")
            else:
                print(f"Downloading post from {post_date}: {post.url}")
                loader.download_post(post, target=username)
                
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
                time.sleep(5 * 60 * 60)  # Sleep for 5 hours
        
        print(f"Completed downloading profile: {username}")
        zip_profile(username) 

if __name__ == "__main__":
    usernames = ["anshikax"]

    download_profiles_with_rate_limiting(usernames)
