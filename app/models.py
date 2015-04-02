import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date , func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Category(Base):
	__tablename__ = 'Category'
	name = Column(String(80), nullable=False)
	description = Column(Text)
	id = Column(Integer, primary_key = True)

class Article(Base):
	__tablename__ = 'Article'
	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key = True)
	text= Column(Text)
	category_id = Column(Integer,ForeignKey('Category.id'))
	Category = relationship(Category)

class Parents(Base):
	__tablename__ = 'Parents'
	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key = True)
	children_id = Column(Integer,ForeignKey('Children.id'))

class Children(Base):
	__tablename__ = "Children"
	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key = True)
	class_id = Column(Integer,ForeignKey('Class.id'))	

class Class(Base):
	__tablename__ = "Class"
	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key = True)

class Subject(Base):
	__tablename__ = "Subject"
	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key = True)

class Marks(Base):
	__tablename__ = "Marks"
	mark = Column(Integer, nullable=False)
	id = Column(Integer, primary_key = True)
	class_id = Column(Integer,ForeignKey('Class.id'))
	children_id = Column(Integer,ForeignKey('Children.id'))
	subject_id = Column(Integer,ForeignKey('Subject.id'))


engine = create_engine('sqlite:///school.db')
Base.metadata.create_all(engine)
