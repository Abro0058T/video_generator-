from fastapi import FastAPI

from pymongo import MongoClient
from schemas import VideoResponse,VideoEditInfo
from typing import List
from services.autoVideoGenerator import generate_video_from_prid,generate_video_from_edit
import asyncio
from fastapi.middleware.cors import CORSMiddleware


collection = MongoClient("mongodb://0.tcp.in.ngrok.io:18176")['pixel']['videos']


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You should restrict this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/video/{prid}/create")
async def create_video(prid:int, user_email:str):
    
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
    collection.videos.insert_one({"prid":edit_data.prid,"status":"Generating", "url":""})
    
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
    edited_video_response:VideoResponse = collection.videos.find_one({"prid":prid, "user_email":user_email})
    return edited_video_response

