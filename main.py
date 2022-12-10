import sys
import requests
from bs4 import BeautifulSoup
from videoDownloader import youtube_dl

def create_video():
    print("================Vidoe Downloaded================")
    try:
        import os
        import subprocess
        import glob
        folder_name=""
        for folder in os.walk("./data/"):
            print(folder)
            folder_name=folder[1][0]
            break
        folders=os.walk(f'./data/{folder_name}/')
        profile_user=""
        for dir in folders:
            profile_user=dir[1]
            break
        mp4=glob.glob(f'./data/{folder_name}/{profile_user[0]}/*.mp4')
        print(mp4)
        if(len(mp4)>0):
            from videoCreator.video_creator import main                
            main(mp4[0])
        for m in mp4:
            os.unlink(m)
    except Exception as e:
        print(e)
        pass
    print("================Upload To S3====================")
def main():
    url=sys.argv[1]
    print(url)
    res=requests.get(url=url)
    html=str(res.text)
    soup=BeautifulSoup(html,'html.parser')
    for item in soup.find_all("a",attrs={"class":"n"},href=True):
        url=f"https://spankbang.com{item['href']}"
        title=item.text

        ydl_opts = {
            'format': 'best',
            'outtmpl': f'./data/spankbang/{title}.mp4',
            'nooverwrites': True,
            'no_warnings': False,
            'ignoreerrors': True,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        create_video()
        
main()