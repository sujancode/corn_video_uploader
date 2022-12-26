import sys
import requests
from bs4 import BeautifulSoup
from videoDownloader import youtube_dl
import os
BASE_DIR=os.path.dirname(os.path.realpath(__file__))
print(BASE_DIR)
def create_video(tags,username=""):
    print("================Vidoe Downloaded================")
    try:
        import os
        import subprocess
        import glob
        folder_name=""
        for folder in os.walk(f"{BASE_DIR}/data/"):
            print(folder)
            folder_name=folder[1][0]
            break
        mp4=glob.glob(f'{BASE_DIR}/data/{folder_name}/*.mp4')
        print(mp4)
        if(len(mp4)>0):
            from videoCreator.video_creator import main                
            main(mp4[0],tags,username)
        for m in mp4:
            os.unlink(m)
    except Exception as e:
        print(e)
        pass
    print("================Upload To S3====================")

def scrape_spangbang(html):
    soup=BeautifulSoup(html,'html.parser')
    for item in soup.find_all("a",attrs={"class":"n"},href=True):
            url=f"https://spankbang.com{item['href']}"
            title=item.text

            ydl_opts = {
                'format': 'best',
                'outtmpl': f'{BASE_DIR}/data/spankbang/{title}.mp4',
                'nooverwrites': True,
                'no_warnings': False,
                'ignoreerrors': True,
            }
            print(url)

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])        
            res=requests.get(url)
            tag_soup=BeautifulSoup(res.text,"html.parser")
            tag_div=tag_soup.find("div",attrs={"class":"searches"})
            tags=[]
            try:
                for a in tag_div.find_all("a"):
                    tags.append(a.text)
                tags=list(set(tag_div.text.splitlines()))
                if '' in tags:
                    tags.remove('')
                if '...' in tags:
                    tags.remove('...')
            except Exception as e:
                print(f"Error with url {e}")
            print(tags)
            create_video(tags)    
   
def pornhub_scrapper(html):
    soup=BeautifulSoup(html,'html.parser')
    for item in soup.find_all("div",attrs={"class":"thumbnail-info-wrapper"}):
            try:
                title=item.span.a["title"]
                url=item.span.a["href"]

                url=f"https://pornhub.com{url}"
                ydl_opts = {
                    'format': 'best',
                    'outtmpl': f'{BASE_DIR}/data/pornhub/{title}.mp4',
                    'nooverwrites': True,
                    'no_warnings': False,
                    'ignoreerrors': True,
                }
                print(url)
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])        
                res=requests.get(url)
                username_soup=BeautifulSoup(res.text,"html.parser")
                username=username_soup.select_one(".usernameBadgesWrapper a").text
                tag_soup=BeautifulSoup(res.text,"html.parser")
                tag_div=tag_soup.find_all("a",attrs={"class":"item"})
                tags=[]
                try:
                    for tag in tag_div:
                        tags.append(tag.text)
                except Exception as e:
                    print(f"Error with url {e}")
                print(tags)
                create_video(tags,username)
            except Exception as e:
                print(e)    

def scrape_xvideos():
    
    url=f"https://www.xvideos.com/video23840010/grade_a_ass_with_dani_daniels"
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{BASE_DIR}/data/pornhub/temp.mp4',
        'nooverwrites': True,
        'no_warnings': False,
        'ignoreerrors': True,
    }
    print(url)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])  

def main():
    url=sys.argv[1]
    for index in range(1,1000):
        url+=f"{index}/?o=all"
        print(url)
        res=requests.get(url=url)
        html=str(res.text)
        scrape_spangbang(html)
    
scrape_xvideos()