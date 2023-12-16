import os
import uuid
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
from io import BytesIO
from typing import List

from fastapi import APIRouter, Depends, File, UploadFile, status, Form
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from ..crud.audio_crud import (
    all_audios,
    create_audio,
    read_audio,
    soft_delete,
    update_audio,
    search_audios_by_name,
)
from ..db.database import get_db
from ..models.audio_model import Audio
from ..schemas.playlist_audio_schema import (
    AudioBaseSchema,
    AudioSchema,
    AudioUpdate,
    AudioResponseSchema,
    CreateAudioSchema,
)
from ..utils.exception import InvalidFileType, NotFoundException
from ..utils.handle_file import save_to_FS, validate_file_type, get_audio_file_extension
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()
# Serve static files
# router.mount(
#     "/static",
#     StaticFiles(
#         directory=os.path.abspath(
#             os.path.join(os.path.dirname(__file__), "..", "..")
#         )
#         + "/static",
#         html=False,
#     ),
#     name="static",
# )


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=AudioResponseSchema,
)
async def add_audio(
    audio_data: CreateAudioSchema = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Create an audio"""
    is_audio = validate_file_type(file, "audio")
    
    # # Check if not an audio
    if is_audio is False:
        raise InvalidFileType(detail="Your upload file must be a audio")

    extension = get_audio_file_extension(file)
    file_content = await file.read()
    audio = AudioSegment.from_file(BytesIO(file_content))
    desired_sample_rate = 44100  # Example: 44.1 kHz
    audio = audio.set_frame_rate(desired_sample_rate)
    audio = audio.set_channels(1)
    samples = np.array(audio.get_array_of_samples())
    sample_rate = audio.frame_rate
    duration_seconds = len(samples) / sample_rate  # Duration based on the length of input audio
     # Generate the high-pitched sound as a Sine wave
    frequency=19000
    high_pitch_duration = 3  # seconds
    high_pitch_sound = Sine(frequency).to_audio_segment(duration=high_pitch_duration * 1000, volume=-5)  # Convert to milliseconds

    # Define the time range for high-pitch effect (first 3 seconds and last 3 seconds)
    start_time = 0
    end_time = duration_seconds - high_pitch_duration

    # Add high pitch in the first 3 seconds
    output_audio = audio.overlay(high_pitch_sound, position=start_time)

    # Add high pitch in the last 3 seconds
    output_audio = output_audio.overlay(high_pitch_sound, position=end_time * 1000)
    
    
    data = audio_data.dict()
    data["durations"] = duration_seconds
    print("duration: ", duration_seconds)
    audio: Audio = Audio(**data)
    new_audio = create_audio(audio, db)
    
    output_file = f"./static/audio/{audio_data.audio_name}.wav"
    output_audio.export(output_file, format="wav")
    

    # Add metada
    logger.info(
        f"Created audio name {new_audio.audio_name} with ID {new_audio.audio_id}"
    )

    return new_audio.__dict__


@router.post("/soft-delete/{audio_id}", response_model=AudioSchema)
async def soft_delete_by_id(audio_id: str, db: Session = Depends(get_db)):
    """Get the audio by its id"""
    audio = soft_delete(audio_id, db)

    if audio is None:
        logger.info(f"Invalid audio with ID: {audio_id}")
        raise NotFoundException(detail=f"Invalid audio with ID: {audio_id}")
    logger.info(f"Soft delete audio with ID: {audio_id}")
    return audio.__dict__


@router.get("/get/{audio_id}", response_model=AudioSchema)
async def get_audio_by_id(audio_id: str, db: Session = Depends(get_db)):
    """Get the audio by its id"""
    audio = read_audio(audio_id, db)
    if audio is None:
        logger.info(f"Invalid audio with ID: {audio_id}")
        raise NotFoundException(detail=f"Invalid audio with ID: {audio_id}")

    logger.info(f"Get audio with ID: {audio.audio_id}")
    return audio.__dict__


@router.put("/update/{id}", response_model=AudioBaseSchema)
async def update_audio_by_id(
    id: str, audio: AudioUpdate, db: Session = Depends(get_db)
):
    """Update the video following its id"""
    updated_audio = update_audio(id, audio, db)
    if updated_audio is None:
        logger.info(f"Invalid audio with ID: {id}")
        raise NotFoundException(detail=f"Invalid audio with ID: {id}")

    logger.info(f"Updated audio with ID: {id}")
    return updated_audio.__dict__


@router.get("/search/", response_model=List[AudioResponseSchema])
async def get_audios(db: Session = Depends(get_db)):
    audios = await all_audios(db)
    audios_dict_list = [i.__dict__ for i in audios]
    logger.info(f"Number of audios: {len(audios)}")
    return audios_dict_list


@router.get("/search/{name}", response_model=List[AudioResponseSchema])
async def search_audios(name: str, db: Session = Depends(get_db)):
    audios = await search_audios_by_name(name, db)
    audios_dict_list = [i.__dict__ for i in audios]
    logger.info(f"Number of audios: {len(audios)}")
    return audios_dict_list
