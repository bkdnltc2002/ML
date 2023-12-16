from sqlalchemy.orm import Session
from .database import Base, engine, get_db, SessionLocal
from ..models.user_model import User
from ..models.playlist_model import Playlist
from ..utils.hash import hash_password
import uuid
def seed_data():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        #Add default playlist
    #     playlist = (
    #     db.query(Playlist)
    #     .where(Playlist.playlist_name == "default")
    #     .where(Playlist.is_deleted == False)
    #     .first()
    # )
    #     if playlist is None:
    #         default_playlist = Playlist()
    #         default_playlist.playlist_name = "default"
    #         default_playlist.playlist_id = str(uuid.uuid4())
    #         default_playlist.playlist_description = "Default playlist"
    #         default_playlist.created_by = "System"
    #         print(default_playlist)
    #         db.add(default_playlist)
    #         db.commit()
        
        
        # Check if data is already seeded
        # if not db.query(User).count():
        #     # Seed default data here
        #     default_playlist = (
        #         db.query(Playlist)
        #         .where(Playlist.playlist_name == "default")
        #         .where(Playlist.is_deleted == False)
        #         .first()
        #     )
            
            user_data = [
                {
                    "name": "admin",
                    "password": hash_password("123456"),
                    "phone": "01234567890",
                    "role": "admin",
                    # "playlist_id": default_playlist.playlist_id
                },
                {
                    "name": "operator",
                    "password": hash_password("123456"),
                    "phone": "09876543210",
                    "role": "operator",
                    # "playlist_id": default_playlist.playlist_id
                },
                {
                    "name": "viewer",
                    "password": hash_password("123456"),
                    "phone": "08876543210",
                    "role": "viewer",
                    # "playlist_id": default_playlist.playlist_id
                },
            ]
            for data in user_data:
                user = User(**data)
                db.add(user)
            db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
