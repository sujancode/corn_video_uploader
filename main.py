import os
from videoDownloader.functions import dl_start,add_check,check_for_database

def main():
    check_for_database()

    url="https://www.pornhub.com/pornstar/rae-lil-black/videos"
    add_check(url)
    dl_start()
main()