from moviepy.editor import VideoFileClip,CompositeVideoClip,concatenate_videoclips,ImageClip
import random
from dependency.storage_bucket.index import getS3StorageInstance
import os
import requests
from moviepy.video.fx.resize import resize
BASE_DIR=os.path.dirname(os.path.realpath(__file__))

def get_random_subclip(total_duration,subclip_duration):
    pos=random.randint(0,int(total_duration)-int(subclip_duration))
    return [pos,pos+int(subclip_duration)]


def get_dimension(width,height):
    [overlay_width,overlay_height]=VideoFileClip(f'{BASE_DIR}/video/overlay.mp4').size
    print(overlay_height,overlay_width)
    print(width)
    return [ 1024,720]
    
    if (width/overlay_width)<=1.0:
        return [int(width),int(height)]
    else:
        return [int(width/4),int(height)]
    

def create_video(video_path,overlay_path,output_path):
    video = VideoFileClip(video_path,target_resolution=(720,1280))
    
    # [width,height]=video.size
    # [width,height]=get_dimension(width,height)

    overlay= VideoFileClip(overlay_path,has_mask=True,target_resolution=(720,int(1280/4)))
    overlay=overlay.set_position(("right", "top"))


    if not video.duration > overlay.duration:
        return False

    [start,end]=(get_random_subclip(video.duration,overlay.duration))

    clip1=video.subclip(start,end)
    clip=clip1.without_audio()

    if video.duration > 60*7:
        video=video.subclip(0,60*7)

    overlay_title = ImageClip(f"{BASE_DIR}/video/title.png",).set_start(0).set_duration(overlay.duration).set_pos((15,"bottom"))
    overlay_title=overlay_title.resize(0.4)
    
    title = ImageClip(f"{BASE_DIR}/video/title.png",).set_start(0).set_duration(video.duration).set_pos((15,"bottom"))
    title=overlay_title.resize(0.4)

    home=CompositeVideoClip([clip,overlay,overlay_title])
    video=CompositeVideoClip([video,title])
    result=concatenate_videoclips([home,video])
    # result.resize(height=480)
    result.write_videofile(output_path,preset="veryfast")
    return True

def main(mp4Path,tags):
    filename=mp4Path.split("/")[-1]
    result=create_video(mp4Path,f'{BASE_DIR}/video/overlay.mp4',f'{BASE_DIR}/tmp/{filename}')
    if result:
        with open(f"{BASE_DIR}/converted_videos.txt","a") as txt_file:
            txt_file.write(filename+"\n")
        
        storage_bucket=getS3StorageInstance()
        storage_bucket.upload_file(path=f'{BASE_DIR}/tmp/{filename}',bucket_name='onlyfans-data-bucket',upload_location=f'{filename}')
        os.unlink(f"{BASE_DIR}/tmp/{filename}")
        url=f"https://onlyfans-data-bucket.s3.amazonaws.com/{filename.replace(' ','+')}"
    
        requests.post(url='https://7sve4dxax3.execute-api.us-east-1.amazonaws.com/prod/send',json={
            "url":url,
            "title":filename.split(".")[0],
            "tags":tags
        })
    
if __name__ == '__main__':
    main()
