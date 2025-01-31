from datetime import datetime
from app.db import Base
from .Vote import Vote
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, select, func
from sqlalchemy.orm import relationship, column_property

class Post(Base):
    __tablename__='posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    post_url = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # dynamic queries for user, comments and votes
    user = relationship('User')
    comments = relationship('Comment', cascade='all,delete')

    # using column property to create a dynamic query that selects and counts all votes by id where the post id matches
    vote_count = column_property(
        select(func.count(Vote.id))  # Remove brackets from `select([])` => 'select()' for SQLAlchemy 2.0
        .where(Vote.post_id == id)
        .scalar_subquery()  # convert it into a valid subquery column
    )
    votes = relationship('Vote', cascade='all,delete')