from moviepy.editor import VideoFileClip,CompositeVideoClip,concatenate_videoclips
import random
from dependency.storage_bucket.index import getS3StorageInstance
import sys
from videoUploader.sign_up_upload import sign_up
import os

def get_random_subclip(total_duration,subclip_duration):
    pos=random.randint(0,int(total_duration)-int(subclip_duration))
    return [pos,pos+int(subclip_duration)]


def get_dimension(width,height):
    [overlay_width,overlay_height]=VideoFileClip('./video/overlay.mp4').size
    print(overlay_height,overlay_width)
    print(width)
    
    if (width/overlay_width)<=1.0:
        return [int(width),int(height)]
    else:
        return [int(width/4),int(height)]

def create_video(video_path,overlay_path,output_path):
    video = VideoFileClip(video_path)
    
    [width,height]=video.size
    [width,height]=get_dimension(width,height)

    overlay= VideoFileClip(overlay_path,target_resolution=(height,width))

    if not video.duration > overlay.duration:
        return False

    [start,end]=(get_random_subclip(video.duration,overlay.duration))

    clip1=video.subclip(start,end)
    clip=clip1.without_audio()

    if video.duration > 60*6:
        video=video.subclip(0,60*6)
    home=CompositeVideoClip([clip,overlay])

    result=concatenate_videoclips([home,video])
    # result.resize(height=480)
    result.write_videofile(output_path,fps=24,preset="ultrafast")
    return True

def main(mp4Path):
    filename=mp4Path.split("/")[-1]
    result=create_video(mp4Path,'./video/overlay.mp4',f'./tmp/{filename}')
    if result:
        with open("./converted_videos.txt","a") as txt_file:
            txt_file.write(filename+"\n")
        
        storage_bucket=getS3StorageInstance()
        storage_bucket.upload_file(path=f'./tmp/{filename}',bucket_name='onlyfans-data-bucket',upload_location=f'{filename}')
        os.unlink(f"./tmp/{filename}")
        url=f"https://onlyfans-data-bucket.s3.amazonaws.com/{filename.replace(' ','+')}"
        sign_up(url,filename.split(".")[0])
    
    
if __name__ == '__main__':
    main()
