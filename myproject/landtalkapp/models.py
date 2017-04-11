from __future__ import unicode_literals

import datetime
import os
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.deconstruct import deconstructible

# def path_and_rename(path, name):
#     def wrapper(instance, filename):

#         ext = filename.split('.')[-1]

#         # get filename
#         if instance.pk:
#             filename = '{}.{}.{}'.format(instance.pk, name, instance.location)
#         else:
#             # set filename as random string
#             filename = '{}.{}'.format(uuid4().hex, name)

#         print "filename: ", filename
#         # return the whole path to the file
#         return os.path.join(path, filename)
#     return wrapper

@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

def defaultYear():
    return datetime.datetime.now().year

class Submission(models.Model):
    YEAR_CHOICES = [(r,r) for r in range(1900, datetime.datetime.now().year+1)]

    path_and_rename = PathAndRename("landtalk/")

    pub = models.BooleanField(('Publish'), default=False)
    location = models.CharField(('Name of the location (for example: Chavez Park, Berkeley CA)'),max_length=50) #char field?
    lat = models.FloatField(('Latitude of the location (for exammple: 37.427)'))
    lng = models.FloatField(('Longitude of the location (for example: -122.169)'))
    steward = models.ForeignKey(User)
    interviewer = models.CharField(('Your first and last name'), max_length=50, blank=True) #check this max length
    observer = models.CharField(('Frst and last name of the Observer'), max_length=50, blank=True)
    contact_org = models.URLField(('For public lands, enter the name of the managing organization (for example, State Park System)'), blank=True)
    videourl = models.URLField(('Your complete video URL (for example: https://youtu.be/EcSzOnY7uEY)'), blank=True)

    hist_img = models.ImageField(('Upload a historical image of the location'), upload_to=path_and_rename('hist'),blank=True)
    hist_year = models.IntegerField(('Enter the year the historical image was taken'), choices=YEAR_CHOICES, default=defaultYear(),blank=True)
    hist_caption = models.CharField(('Write a caption for the historical image'), max_length=200, blank=True)
    curr_img = models.ImageField(('Upload a current image of the location'), upload_to=path_and_rename('curr'),blank=True)
    curr_year = models.IntegerField(('Enter the year the current image was taken'), choices=YEAR_CHOICES, default=defaultYear(), blank=True)
    curr_caption = models.CharField(('Write a caption for the current image'), max_length=200, blank=True)

    time_submitted = models.DateTimeField(auto_now_add = True)
    time_posted = models.DateTimeField(null = True)

    summary = models.TextField(('Write a brief summary of the video: Who says what about land and weather (max length 200 characters)'), max_length=200)
    look = models.TextField(('How did your observer describe the way the place used to look? (max length 200 characters)'), max_length=200)
    past_do = models.TextField(('What are some of the things your observer used to do here? (max length 200 characters)'), max_length=200)
    current_do = models.TextField(('What are some of the things your observer does here now? (max length 200 characters)'), max_length=200)
    key_words = models.TextField(('Add key words, separated by a comma (for example: dry creek, flood in spring, frogs)'))

    class Meta:
        # Sort by location (ascending), then by time submitted (descending)
        ordering = ["location", "time_submitted"]

    def save(self, *args, **kwargs):
        if self.pub is True:
            self.time_posted = timezone.now()
        else:
            self.time_posted = None

        # create folder for steward if does not exist
        # stewardPath = 'landtalk/' + str(self.steward)
        # if not os.path.exists(stewardPath):
        #     os.makedirs(str(self.steward))

        super(Submission, self).save(*args, **kwargs)

    def publish(self):
        self.time_posted = timezone.now()
        self.save()

    def __str__(self):
        return '{} submitted by {}'.format(self.location, self.interviewer)
