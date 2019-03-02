import datetime
from peewee import *

DATABASE=SqliteDatabase('courses.sqlite')

class Review2(Model):
    string1=CharField()
    string2= CharField()
    created_at=DateTimeField(default=datetime.datetime.now)

    class Meta:
        database=DATABASE

class Course(Model):
    title=CharField()
    url= CharField(unique=True)
    created_at=DateTimeField(default=datetime.datetime.now)

    class Meta:
        database=DATABASE

class Review(Model):
    course=ForeignKeyField(Course, related_name='review_set')
    rating=IntegerField()
    comment=TextField()
    created_at=DateTimeField(default=datetime.datetime.now)

    class Meta:
        database=DATABASE

def Initialize():
    DATABASE.connect()
    DATABASE.create_tables([Course,Review,Review2],safe=True)
    DATABASE.close()