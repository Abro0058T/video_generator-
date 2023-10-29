from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip,ImageClip,AudioFileClip
# Load your video clip
import requests
import base64
from xml.sax.saxutils import escape
# import io
# import tempfile
import cloudinary
import cloudinary.uploader
import cloudinary.api
from services.tempCodeRunnerFile import get_release
# from tempCodeRunnerFile import get_release

from pymongo import MongoClient

collection = MongoClient("mongodb+srv://SIH2023:SIH2023@cluster0.nqzxnng.mongodb.net/")['pixel']['videos']

cloudinary.config(
    cloud_name="dsztz2gsf",
    api_key="661837983169221",
    api_secret="58BTwHOeZPJ8yit4XbTJ9CtYw4w"
)

# Add custom header and ministart 
# 
from pydub import AudioSegment
import zlib

def generate_video_task(images,texts, video_prid,ministry,ReleaseHeading,language="English"):
    print("working1")
    print(language,"language")
    # Audio file 
    audio_text=[]
    final_text=""
    azure_final_text=""
    for text in texts:
        final_text+=text["text"]+"\t"+"\n"
        azure_final_text+=text["azure_text"]
        audio_text.append({"text":text["azure_text"],"voice_gender":"Female","language":language})
    print(audio_text,"audio text")
    # print(audio_text)'
    audio_text.append({"text":azure_final_text,"voice_gender":"Female","language":language})
    # print(final_text)
    print("working2")
    # update video status to 'Analyzing Sound Data'
    # collection.update_one({"prid":video_prid},{"$set":{"status":"Analyzing Sound Data"}})
    print("before audio")
    print("working3")
    url="https://text-to-audio.ashishkingdom.live/text_to_audio"
    print(audio_text)
    data={
      "count": 1,
    #   "texts": [
    #     {
    #       "text": "Hello world abhushke ",
    #       "voice_gender": "Female",
    #     }
    #   ]
      "texts":audio_text
        
    }
    headers={
        'Content-Type': 'application/json',
        'ngrok-skip-browser-warning': 'huehuehue',
    }
    print("working4")
    response=requests.post(url,json=data,headers=headers)
    
    audio_data=collection.update_one({"prid":video_prid},{"$set":{"status":"Audio data generated"}})

    print(response)
    print("working5")
    if response:
        print('hello')
        audio_data = response.json()["audio"][len(audio_text)-1]["data"]
        duration=  response.json()["audio"][len(audio_text)-1]["duration"]

        audio_bytes = base64.b64decode(audio_data)
        decompressed_audio = zlib.decompress(audio_bytes)
        with open("./services/audio.mp3", "wb") as f:
            f.write(decompressed_audio)

    else:
        print("error",response,"THis is t he reeor")
        #exit()
        return None
    print("working6")
    audio_file=collection.update_one({"prid":video_prid},{"$set":{"status":"Audio file generated"}})

    net_time=0
    for audio in response.json()["audio"][:-1]:
        net_time+=audio["duration"]
    video_clip = VideoFileClip("./services/finalBackground.mp4").set_duration(net_time)
    print(net_time,"net_time",duration,"duration")
    print("working7")
    # Image file
    # image=ImageClip("https://upload.wikimedia.org/wikipedia/commons/1/1d/Football_Pallo_valmiina-cropped.jpg")
    if len(images)!=0:
        length_of_image=duration/(len(images))
        image_frames=[]
        url_list=[]
        image_duration=0
        # audio_count_image=0
        for image in images:
            image=ImageClip(image).resize((700,500)).set_position(('right','center')).set_start(image_duration).set_duration(length_of_image)
            image_duration+=length_of_image
            image=image.crossfadein(2)
            image=image.crossfadeout(2)
            # audio_count_image+=1
            image_frames.append(image)
        image_duration=0
        for url in images:
            # print(video_clip.size)
            # print(data)
            url_clip = TextClip("Source of image :-"+url,method="caption",fontsize=25, color='red',size=(1000,600),kerning=2).set_position((500,700))
            # text_clip=fadeout.fadeout(text_clip,1)
            url_clip=url_clip.set_start(image_duration).set_duration(length_of_image)
            # start=start+response.json()["audio"][audio_count]["duration"]
            image_duration+=length_of_image
            url_list.append(url_clip)
    image=ImageClip("./services/75_logo.png")
    # extraImages=ImageClip('PMmodi.png')

    audio=AudioFileClip('./services/audio.mp3').set_duration(duration)
    print(audio,'audio')

    video_clip=video_clip.set_audio(audio)
    video_width, video_height = video_clip.size
    text_width, text_height = image.size
    top_right_x = video_width - text_width
    top_right_y = 0  # Position at the top
    print("working1")
    # extraImages=extraImages.set_position(('right','center')).set_duration(5)
    image=image.set_position((top_right_x,top_right_y)).set_duration(net_time).resize((250,150))
    print("working2")

    # Create an array of text clips

    # heading=TextClip("Heading from the house of Prime minister",fontsize=60,color='red',bg_color='rgb(238, 231, 233)').set_position(('left','top')).set_duration(net_time).margin(left=10,top=10)
    print(ministry)
    heading=TextClip(ministry[0],fontsize=50,color='black',bg_color='rgba(212, 199, 206, 0.37)').set_duration(net_time).margin(left=10,top=10,color=(255,255,255),opacity=0)
    def translate(t):
    # Start and end positions of the text
        start_pos = (1000,0)
        end_pos = (0,0)
        # Calculate x and y positions based on elapsed time and total duration
        # Linear interpolation is used to determine the position of the text at any given time
        x = int(start_pos[0] + t/2 * (end_pos[0] - start_pos[0]))
        y = int(start_pos[1] + t/2 * (end_pos[1] - start_pos[1]))
        if x>0:
            return(x,y)

        return (0,0)
    
# ====================================================================
    heading=heading.set_position(translate)
    heading=heading.crossfadein(4)
# Sub heading animation
    subhead=ReleaseHeading.split(" ")

    sub_heading=TextClip(ReleaseHeading,fontsize=20,color='black',bg_color='rgba(212, 199, 206, 0.37)').set_duration(net_time)
    def sub_translate(t):
    # Start and end positions of the text
        start_pos = (1200,heading.size[1]+10)
        end_pos = (0,heading.size[1]+10)
        # Calculate x and y positions based on elapsed time and total duration
        # Linear interpolation is used to determine the position of the text at any given time
        x = int(start_pos[0] + t/2 * (end_pos[0] - start_pos[0]))
        y = int(start_pos[1] + t/2 * (end_pos[1] - start_pos[1]))
        if x>0:
            return(x,y)

        return (0,heading.size[1]+10)
    sub_heading=sub_heading.set_position(sub_translate)
    sub_heading=sub_heading.crossfadein(4)
# ====================================================================
    heading=heading.set_position(translate)
   

    text_clips = []
    print("working3")
    # Define text content, duration, and position for each text clip
    # text_data = [
    #     {"text": """ 
    #      Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
    #       Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
    #       Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
    #       Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
    #       Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
    #       Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
    #       Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
    #       Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
    #       Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
    #       Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
    #       Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
    #       Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.
    #       Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsam aliquid dolorem blanditiis non ipsum perferendis enim.""", "duration": 5, "position": ("left","center")},
    #     {"text": "Text 2", "duration": 5, "position": (0.5,0.5)},
    #     # Add more text clips as needed
    # ]

    # Create and append TextClip objects to the array
    start=0
    audio_count=0
    print("working4")
    for data in texts:
        print(data)
        text_clip = TextClip(data['text'],method="caption",fontsize=30, color='red',size=(1000,600),kerning=2,font="C:/Users/Abro0058T/AppData/Local/Microsoft/Windows/Fonts/arial-unicode-ms.ttf").margin(left=20,color=(255,255,255),opacity=0)
        text_clip=text_clip.set_start(start,change_end=True)
        start=start+response.json()["audio"][audio_count]["duration"]
        print("working5")
        text_clip = text_clip.set_duration(response.json()["audio"][audio_count]["duration"])
        print("working6")
        audio_count+=1
        text_clip = text_clip.set_position(data["position"])
        text_clip=text_clip.crossfadein(1).crossfadeout(1)
        text_clips.append(text_clip)
    # Composite the text clips onto the video clip

    # update video status to 'Analysing & Generating Video'
    # collection.update_one({"prid":video_prid},{"$set":{"status":"Analysing & Generating Video"}}

    if len(images)!=0:
        video_with_text = CompositeVideoClip([video_clip,image,heading,sub_heading] + text_clips+image_frames+url_list)
    else:
        video_with_text = CompositeVideoClip([video_clip,image,heading,sub_heading] + text_clips+url_list)

    video_data=collection.update_one({"prid":video_prid},{"$set":{"status":"Generating Video"}})
    # update video status to 'Uploading Video'
    # collection.update_one({"prid":video_prid},{"$set":{"status":"Uploading Video"}})

    # Write the final video to a file

    video_with_text.write_videofile("output_video.mp4")
    final_video=collection.update_one({"prid":video_prid},{"$set":{"status":"Video generated"}})

    print("video created")
    upload_result=cloudinary.uploader.upload("output_video.mp4",resource_type="video")
    print("Video uploaded to Cloudinary:", upload_result["secure_url"])

    # update video status to 'Approval Pending'
    # collection.update_one({"prid",video_prid}, {"$set",{"status":"Approval Pending"}})

    return upload_result["secure_url"]
    # print("working5")



image=["https://tse3.mm.bing.net/th?id=OIP.Vt3kGu4X6WQlmH91GpJpzgHaFH&pid=Api&P=0&h=180","https://tse1.mm.bing.net/th?id=OIP.1YM53mG10H_U25iPjop83QHaEo&pid=Api&P=0&h=180"]
text=[
      {"text": "The Vice President, Shri Jagdeep Dhankhar today emphasized the need to promote\nIndia’s glorious cultural heritage of India, spanning over 5000 years. He called upon the  \n media to recognize our cultural heritage and expressed the need to protect, support and \n nurture our artists in a structured manner.","azure_text": "The Vice President, Shri Jagdeep Dhankhar today emphasized the need to promote India’s glorious cultural heritage of India, spanning over 5000 years. He called upon the  media to recognize our cultural heritage and expressed the need to protect, support and  nurture our artists in a structured manner.", "duration": 5, "position": ('left','center')},
      # {"text": """Addressing a gathering after conferring the Sangeet Natak Akademi Amrit Awards\n at Vigyan Bhawan, in New Delhi today, the Vice President expressed his happiness in \n honoring the individuals whose contributions uphold the cultural heritage and pride of\n the nation.""", "duration": 5, "position": ('left','center')},
      {"text":  """Addressing a gathering after conferring the Sangeet Natak Akademi Amrit Awards\nat Vigyan Bhawan, in New Delhi today, the Vice President expressed his happiness in \nhonoring the individuals whose contributions uphold the cultural heritage and pride of\n  the nation.""","azure_text":  """Addressing a gathering after conferring the Sangeet Natak Akademi Amrit Awards at Vigyan Bhawan, in New Delhi today, the Vice President expressed his happiness in honoring the individuals whose contributions uphold the cultural heritage and pride of the nation.""", "duration": 5, "position": (0.5,0.5)},
]

def convertData(id):
    relese_data=get_release(id)# get data
    texts=[]
    print(relese_data["paragraph"])
    def add_newline_every_n_words(text, n):
        # Split the text into words
        words = text.split()

        # Check if there are more than n words
        if len(words) <= n:
            return text

        # Create a list to hold lines of text with n words each
        lines = []
        for i in range(0, len(words), n):
            line = " ".join(words[i:i + n])
            lines.append(line)

        # Join the lines with newline characters
        result = "\n".join(lines)

        return result

    # Example usage:
    for text in relese_data["paragraph"]:
        azure_text=text.replace("\n", "").replace("\r", "")
        output_text = add_newline_every_n_words(text, 210)
        if output_text.count("*") <1:
            # texts.append({'text':escape(output_text),"azure_text":escape(azure_text), "position": ('left','center')})
            texts.append({'text':escape(output_text),"azure_text":escape(output_text), "position": ('left','center')})

        # texts.append({'text':output_text.replace("’","'").replace('“','"').replace('”','"').replace('‘',"'"),"azure_text":azure_text.replace("’","'").replace('“','"').replace('”','"').replace('‘',"'"), "position": ('left','center')})

    images=[]
    print(texts)
    print("texts2")
    print(relese_data["imageList"])
    if (relese_data["imageList"]!=[]):
         for image in relese_data['imageList']:
             images.append(image)
    print("images")
    print(images,texts)
    ministry=relese_data["ministry"],
    releaseHeading=relese_data["releaseHeading"]
    return (images,texts,ministry,releaseHeading)# desired format 

prid=1960334
images,texts,ministry,releaseHeading=convertData(prid)
print(ministry[0])

generate_video_task(images,texts,prid,ministry,releaseHeading)
