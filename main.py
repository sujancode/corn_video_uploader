import sys
import requests
from bs4 import BeautifulSoup
from videoDownloader import youtube_dl
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
        
main()