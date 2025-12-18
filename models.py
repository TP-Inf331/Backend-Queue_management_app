from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from base import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(150), nullable=False)
    role = Column(String(50), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    mot_de_passe_hash = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    tickets = relationship("Ticket", back_populates="user")
    notifications = relationship("Notification", back_populates="user")

class Queue(Base):
    __tablename__ = "queues"
    queue_id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(150), nullable=False)
    institution = Column(String(200), nullable=True)
    code_unique = Column(String(100), unique=True, nullable=False, index=True)
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    max_capacity = Column(Integer, nullable=True)
    tickets = relationship("Ticket", back_populates="queue", cascade="all, delete-orphan")

class Ticket(Base):
    __tablename__ = "tickets"
    ticket_id = Column(Integer, primary_key=True, index=True)
    queue_id = Column(Integer, ForeignKey("queues.queue_id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    numero = Column(Integer, nullable=False, index=True)
    statut = Column(String(50), nullable=False, index=True)
    prioritaire = Column(Boolean, default=False)
    heure_arrivee = Column(DateTime(timezone=True), server_default=func.now())
    heure_passage = Column(DateTime(timezone=True), nullable=True)
    cancelled = Column(Boolean, default=False)
    queue = relationship("Queue", back_populates="tickets")
    user = relationship("User", back_populates="tickets")
    __table_args__ = (UniqueConstraint('queue_id', 'numero', name='uq_queue_numero'),)

class Notification(Base):
    __tablename__ = "notifications"
    notification_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    type = Column(String(50))
    message = Column(Text)
    date_envoi = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="notifications")
