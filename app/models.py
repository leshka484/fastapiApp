from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import date

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    reg_date = Column(Date, default=date.today)
    disabled = Column(Boolean, default=False)
    publications = relationship("Publication", back_populates="owner")

class Publication(Base):
    __tablename__ = "publications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    publication_date = Column(Date)
    owner = relationship("User", back_populates="publications")
    tags = relationship("Tags",secondary="publications_tags", back_populates="publications")


publications_tags = Table('publications_tags', Base.metadata,
    Column("publication_id", ForeignKey("publications.id"), primary_key=True), 
    Column("tag_id", ForeignKey("tags.id"), primary_key=True)
)   

class Tags(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    publications = relationship("Publication",secondary="publications_tags", back_populates="tags")