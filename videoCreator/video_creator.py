from moviepy.editor import VideoFileClip,CompositeVideoClip,concatenate_videoclips,ImageClip
import random
from dependency.storage_bucket.index import getS3StorageInstance
import os
import requests
from dependency.database.index import getDatabaseWrapperInstance
from sanitize_filename import sanitize

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

    # watermark=ImageClip(f"{BASE_DIR}/video/title.png").set_start(60).set_duration(video.duration).resize(0.3)
    # watermark=watermark.set_position(("left", "top"))
    home=CompositeVideoClip([clip,overlay])
    # video=CompositeVideoClip([video,watermark])
    result=concatenate_videoclips([home,video])

    result.write_videofile(output_path,preset="veryfast")
    return True

def main(mp4Path,tags,username=""):
    filename=mp4Path.split("/")[-1]
    filename=sanitize(filename)
    result=create_video(mp4Path,f'{BASE_DIR}/video/overlay.mp4',f'{BASE_DIR}/tmp/{filename}')
    if result:
        with open(f"{BASE_DIR}/converted_videos.txt","a") as txt_file:
            txt_file.write(filename+"\n")
        
        storage_bucket=getS3StorageInstance()
        storage_bucket.upload_file(path=f'{BASE_DIR}/tmp/{filename}',bucket_name='onlyfans-data-bucket',upload_location=f'{filename}')
        os.unlink(f"{BASE_DIR}/tmp/{filename}")
        url=f"https://onlyfans-data-bucket.s3.amazonaws.com/{filename.replace(' ','+')}"

        db=getDatabaseWrapperInstance(table_name="created_video")
        
        db.insert(collection="videos",data={
            "url":url,
            "title":filename.split(".")[0],
            "tags":tags,
            "username":username
        })

        # requests.post(url='https://7sve4dxax3.execute-api.us-east-1.amazonaws.com/prod/send',json={
        #     "url":url,
        #     "title":filename.split(".")[0],
        #     "tags":tags,
        #     "username":""
        # })
    
if __name__ == '__main__':
    main()
