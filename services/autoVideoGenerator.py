
# Importing libraries
import time
import hashlib
from urllib.request import urlopen, Request
from services.tempCodeRunnerFile import get_latest_release_id,get_release
from services.mainVideo2 import generate_video_task,convertData
# from tempCodeRunnerFile import get_latest_release_id,get_release
# from mainVideo2 import generate_video_task,convertData
import pymongo
from schemas import VideoResponse
from datetime import datetime

client = pymongo.MongoClient("mongodb+srv://SIH2023:SIH2023@cluster0.nqzxnng.mongodb.net/")

db=client['pixel']

collection=db['videos']
# setting the URL you want to monitor


def detect():
	url = Request('https://pib.gov.in/allRel.aspx',
				headers={'User-Agent': 'Mozilla/5.0'})
	# to perform a GET request and load the
	# content of the website and store it in a var
	response = urlopen(url).read()
	# to create the initial hash
	currentHash = hashlib.sha224(response).hexdigest()
	print("running")
	time.sleep(10)
	while True:
		try:
			# perform the get request and store it in a var
			response = urlopen(url).read()
			# create a hash
			currentHash = hashlib.sha224(response).hexdigest()
			# wait for 30 seconds
			time.sleep(30)
			# perform the get request
			response = urlopen(url).read()
			# create a new hash
			newHash = hashlib.sha224(response).hexdigest()
			# check if new hash is same as the previous hash
			if newHash == currentHash:
				continue
			
			# if something changed in the hashes
			else:
				# notify
				print("something changed")
				latest_release_id=get_latest_release_id() # get latest notice prid
				# addData(latest_release_id)
				converted_data=convertData(latest_release_id) #get latest notice data and convert it into required format 
				images,texts=converted_data
				print("converted_data recived")
				video_data=generate_video_task(images,texts, latest_release_id,"English")
				print("video_data_recived") #convert to video and upload to cloudnary returns the url 
				addVideo(video_data,converted_data,latest_release_id)  # add video to mongodb data base
				# again read the website
				response = urlopen(url).read()
				# create a hash
				currentHash = hashlib.sha224(response).hexdigest()
				# wait for 600 seconds
				time.sleep(120)
				continue
			
		# To handle exceptions
		except Exception as e:
			print("error",e)

# detect()
def addVideo(video_data,converted_data,latest_release_id):# runs only  when new notice is uploaded
	notice_data=get_release(latest_release_id)
	print("notice_data",notice_data)
	data={
		'prid':latest_release_id,
		'status':'generated',
		'url':video_data,#cloudnaty url
		"user_email":"generated",
		"datetime":datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
		"ministry_name":notice_data["ministry"],
		"heading":notice_data["releaseHeading"],
		"images":converted_data[0],
		"text_list":converted_data[1],#[{'test':"","azure_text":""}]
		"language":"English",#["name":'link'] change link to prid 
		"release_language":notice_data["releaseLanguages"]
	}
	print("dTA",data)
	# finally update the video data with the given prid
	# result=collection.insert_one({"prid":latest_release_id},{"$set":data})
	data = VideoResponse(**data)
	# insert video data so that it status can be changed during video generation
	result=collection.insert_one(data.model_dump())
	print("result",result)

def addData(latest_release_id):
	# data={
	# 	"prid":latest_release_id,
	# 	"status":"generating",
	# }
	data = VideoResponse(prid=latest_release_id, status="generating")
	# insert video data so that it status can be changed during video generation
	result=collection.insert_one(data.model_dump())

def generate_video_from_prid(id):
	# addData(latest_release_id)
	converted_data=convertData(id) 
	print("converted data")#get latest notice data and convert it into required format 
	images,texts=converted_data
	video_data=generate_video_task(images,texts, id) #convert to video and upload to cloudnary returns the url 
	# addVideo(video_data,converted_data,id)  # add video to mongodb data base

	return video_data # url of video 
				
def generate_video_from_edit(id,imageLists,language):
	converted_data=convertData(id)
	images,texts=converted_data
	video_Data=generate_video_task(imageLists,texts,id,language)
	addVideo(video_Data,converted_data,id)# add video to mongo db database
# print("hello")
# latest_release_id=get_latest_release_id() # get latest notice prid
# print(latest_release_id,"latest-release _id")


latest_release_id=1958613
# addData(latest_release_id)
# print("add data")
# converted_data=convertData(1958613) #get latest notice data and convert it into required format
# print(convertData,"converted_Data") 
# images,texts=converted_data
# print("=================================================================")
# print(images,"image",texts,"text")
# language="marathi"
# video_data=generate_video_task(images,texts, latest_release_id,language) #convert to video and upload to cloudnary returns the url 
# print(video_data,"videodata")
# addVideo(video_data,converted_data,latest_release_id)
# detect()