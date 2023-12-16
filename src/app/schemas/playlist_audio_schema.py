from typing import List, Optional
from pydantic import UUID4, BaseModel
from datetime import datetime
import json


class AudioBaseSchema(BaseModel):
    audio_name: str
    durations: int
    price: Optional[float]
    created_by: str
    audio_id: UUID4

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class CreateAudioSchema(BaseModel):
    audio_name: str
    price: Optional[float]
    created_by: str

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class AudioResponseSchema(AudioBaseSchema):
    audio_id: UUID4
    updated_at: datetime

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class AudioUpdate(BaseModel):
    audio_name: Optional[str]
    price: Optional[float]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class CreatePlaylistSchema(BaseModel):
    playlist_name: str
    playlist_description: Optional[str]
    audio_ids: Optional[List[UUID4]]
    price: Optional[float]
    created_by: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class PlaylistBaseSchema(BaseModel):
    playlist_name: str
    playlist_description: Optional[str]
    price: Optional[float]
    created_by: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class PlaylistResponseSchema(PlaylistBaseSchema):
    playlist_id: UUID4
    updated_at: datetime
    total_time: int
    number_of_songs: int
    audios: Optional[List[AudioBaseSchema]]
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class PlaylistWithAssignedResponseSchema(PlaylistBaseSchema):
    playlist_id: UUID4
    updated_at: datetime
    total_time: int
    number_of_songs: int
    audios: List[AudioBaseSchema]
    is_assigned: bool = False
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class PlaylistUpdate(BaseModel):
    playlist_name: Optional[str]
    playlist_description: Optional[str]
    audio_ids: Optional[List[UUID4]]
    price: Optional[float]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class AudioSchema(AudioBaseSchema):
    playlists: List[PlaylistBaseSchema]
    updated_at: datetime


class PlaylistSchema(PlaylistBaseSchema):
    audios: List[AudioBaseSchema]
    updated_at: datetime


class PlaylistAudioBaseSchema(BaseModel):
    audio_id: UUID4
    playlist_id: UUID4
    order: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class PlaylistAudioBatchDeleteSchema(BaseModel):
    audio_ids: List[str]
    playlist_ids: List[str]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
