from fastapi import FastAPI

from pymongo import MongoClient
from schemas import VideoResponse,VideoEditInfo
from typing import List
from services.autoVideoGenerator import generate_video_from_prid,generate_video_from_edit
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail



collection = MongoClient("mongodb+srv://SIH2023:SIH2023@cluster0.nqzxnng.mongodb.net/")['pixel']['videos']


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You should restrict this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/video/{prid}/create")
async def create_video(prid:int):
    
    # make video status again to 'Generating' and url to ""
    # collection.videos.insert_one({"prid":prid, "user_email":user_email,"status":"Generating", "url":""})
    
    # starts a background task to generate video
    # (work in progress)
    print("create_video funciton")
    asyncio.create_task(generate_video_from_prid(prid))
    # converted_data=convertData(prid) #get latest notice data and convert it into required format
    # print(convertData,"converted_Data") 
    # images,texts=converted_data
    # print(images,"image",texts,"text")
    # video_data=generate_video_task(images,texts, latest_release_id) #convert to video and upload to cloudnary returns the url 
    # print(video_data,"videodata")

    # return the updated video response
    # edited_video_response:VideoResponse = collection.videos.find_one({"prid":prid, "user_email":user_email})
    return {"prid":prid}

@app.post("/video/{prid}/edit")
async def edit_video( edit_data:VideoEditInfo)->VideoResponse:
    
    # make video status again to 'Generating' and url to ""
    collection.videos.insert_one({"prid":edit_data.prid,"status":"Generating"})
    
    # starts a background task to generate video
    # (work in progress)
    asyncio.create_task(generate_video_from_edit(edit_data.prid,edit_data.Images,edit_data.Lang))
    # converted_data=convertData(prid) #get latest notice I and convert it into required format
    # print(convertData,"converted_Data") 
    # images,texts=converted_data
    # print(images,"image",texts,"text")
    # video_data=generate_video_task(images,texts, latest_release_id) #convert to video and upload to cloudnary returns the url 
    # print(video_data,"videodata")

    # return the updated video response
    edited_video_response:VideoResponse = collection.videos.find_one({"prid":edit_data.prid})
    return edited_video_response


@app.post("/notification")
async def send_notifications(request: Request):
    data = await request.json()
    response = ''
    message = Mail(
        from_email='irary.sendgrid@inbox.testmail.app',
        to_emails='abhiseknaulae@gmail.com',
        subject='Sending with Twilio SendGrid',
        html_content=f'<div><h1>A new video is generated</h1></div> '
                     f'<div><a href="url">Click here to go to the video</a></div> '
                     f'<div>This video is available in below languages <br> <h3></h3></div>'
    )
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))
    return {'message': 'Request Processed'}
