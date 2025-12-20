from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    nom: str
    email: EmailStr
    phone: Optional[str] = None

class UserCreate(UserBase):
    mot_de_passe: str
    role: Optional[str] = "client"

class UserOut(UserBase):
    user_id: int
    role: str
    date_creation: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class QueueCreate(BaseModel):
    nom: str
    institution: Optional[str] = None
    max_capacity: Optional[int] = None

class QueueOut(BaseModel):
    queue_id: int
    nom: str
    institution: Optional[str]
    code_unique: str
    date_creation: datetime
    max_capacity: Optional[int]
    class Config:
        from_attributes = True

class TicketCreate(BaseModel):
    queue_id: int
    user_id: Optional[int] = None
    prioritaire: Optional[bool] = False

class TicketOut(BaseModel):
    ticket_id: int
    queue_id: int
    user_id: Optional[int]
    numero: int
    statut: str
    prioritaire: bool
    heure_arrivee: datetime
    heure_passage: Optional[datetime]
    cancelled: bool
    class Config:
        from_attributes = True

class NotificationCreate(BaseModel):
    user_id: int
    type: str
    message: str

class NotificationOut(BaseModel):
    notification_id: int
    user_id: int
    type: str
    message: str
    date_envoi: datetime
    class Config:
        from_attributes = True
