import os
from videoDownloader.functions import dl_start,add_check,check_for_database
import sys
def main():
    check_for_database()
    if len(sys.argv)>=1:
        url=sys.argv[1]
        print(url)
        add_check(url)
    dl_start()
main()