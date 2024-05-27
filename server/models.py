from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("name", "phone_number")
    def validate_author(self, key, value):
        if key == "name":
            if not value:
                raise ValueError ("The Author's name must not be blank.")
            elif db.session.query(Author).filter_by(name=value).first():
                 raise ValueError ("The Author must have a unique name!")
            else:
                return value
        elif key == "phone_number":
            if not value:
                raise ValueError ("Phone number cannot be blank")
            elif len(str(value)) != 10:
                raise ValueError ("Phone number must be only 10 numbers")
            elif not value.isdigit():
                raise ValueError ("Phone number must only be numbers")
            else:
                return value
            
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("title", "content", "category", "summary")
    def validate_post(self, key, value):
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        # breakpoint()
        if key == "title":
            if not value:
                raise ValueError ("The title's name must not be blank.")
            elif [word for word in clickbait if (word in value)]:
                raise ValueError (f'Title must contain {", ".join(clickbait)}')
            else:
                return value
            
        elif key == "content":
            if len(value) < 250:
                raise ValueError ("The content must be 250 characters or longer.")
            else:
                return value
            
        elif key == "category":
            if value != "Fiction" or value != "Non-Fiction":
                raise ValueError ("The category must be \'Fiction\' or \'Non-Fiction\'")
            else:
                return value
            
        elif key == "summary":
            if value > 250:
                raise ValueError ("The summary must be a maximum of 250 characters.")
            else:
                return value


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
