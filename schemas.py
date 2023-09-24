from pydantic import BaseModel
from typing import List,Dict

# class ImageInfo(BaseModel):
#     # id: int
#     image: str
#     # tags: List[str] = None


class VideoEditInfo(BaseModel):
    # datetime: str
    prid:int
    Lang: str
    # voice_gender:str
    Images: List[str]
    # text_list: List[str] = None
class TextInfo(BaseModel):
    text:str
    azure_text:str
    position:List[str]


class VideoResponse(BaseModel):
    prid:int
    status: str
    url: str= ""
    edit_history: List[VideoEditInfo] = []
    user_email: str= ""
    datetime: str= ""
    ministry_name: str= ""
    heading: str= ""
    images: List[str] = []
    text_list: List[TextInfo] = []
    language: str= ""
    release_language:Dict[str,str]={}


class VideoListResponse(BaseModel):
    videos:List[VideoResponse]


class UserVideoStats(BaseModel):
    total_videos: int
    total_accepted: int
    total_rejected: int
    total_pending: int