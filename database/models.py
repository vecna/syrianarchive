from django.db import models
from django.contrib.auth.models import User
from django.contrib.admin import widgets
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
import time
import django_filters


class InternationalInstrument(models.Model):
	name = models.CharField(max_length=250)
	number = models.CharField(max_length=250)

	def __unicode__(self):
		return self.name

class MediaContentType(models.Model):
	name = models.CharField(max_length=250)

	def __unicode__(self):
		return self.name

class SourceConnection(models.Model):
	name = models.CharField(max_length=250)

	def __unicode__(self):
		return self.name

class LocationPlace(models.Model):
	name = models.CharField(max_length=250)
	def __unicode__(self):
		return self.name

class Device(models.Model):
	name = models.CharField(max_length=250)

	def __unicode__(self):
		return self.name

class ViolationType(models.Model):
	name = models.CharField(max_length=250)

	def __unicode__(self):
		return self.name

class DatabaseEntry(models.Model):

	#public
	name = models.CharField(max_length=250)
	reference_code = models.CharField(max_length=250, null=True, blank=True)
	cloths_and_uniforms = models.CharField(max_length=250, null=True, blank=True)
	description = models.TextField(max_length=5000, null=True, blank=True)
	recording_date = models.DateTimeField(default=datetime.now, null=True, blank=True)
	type_of_violation = models.ManyToManyField(ViolationType, blank=True)
	location = models.ManyToManyField(LocationPlace, blank=True)
	location_latitude = models.CharField(max_length=250, null=True, blank=True)
	location_longitude = models.CharField(max_length=250, null=True, blank=True)
	edited = models.NullBooleanField(null=True, blank=True)
	file_size = models.CharField(max_length=250, null=True, blank=True)
	duration = models.CharField(max_length=250, null=True, blank=True)
	device_used = models.ManyToManyField(Device, blank=True)
	chain_of_custody_notes_public = models.TextField(max_length=5000, null=True, blank=True)
	LANGS=(
		('AR','Arabic'),
		('EN','English'),
		('FR','French'),
		('RU','Russian'),
		('FA','Persian'),
	)
	languages = models.CharField(max_length=250, null=True, blank=True, choices=LANGS)
	finding_aids = models.CharField(max_length=250, null=True, blank=True)
	graphic_content = models.NullBooleanField(null=True, blank=True)
	gender_or_sex = models.NullBooleanField(null=True, blank=True)
	keywords = models.CharField(max_length=250, null=True, blank=True)
	international_instrument = models.ManyToManyField(InternationalInstrument, blank=True)
	international_instrument_notes = models.TextField(max_length=5000, null=True, blank=True)
	media_content_type = models.ManyToManyField(MediaContentType,  blank=True)
	landmarks = models.TextField(max_length=5000, null=True, blank=True)
	weather_in_media = models.TextField(max_length=5000, null=True, blank=True)
	weapons_used = models.TextField(max_length=5000, null=True, blank=True)
	urls_and_news = models.TextField(max_length=5000, null=True, blank=True)
	reliability_score = models.IntegerField(
        			default=1,
        			validators=[
            			MaxValueValidator(100),
            			MinValueValidator(1)
        			]
     			)
	related_incidents = models.ManyToManyField("DatabaseEntry", blank=True)


	

	#private
	staff_id = models.CharField(max_length=250, null=True, blank=True)
	file_name = models.CharField(max_length=250, null=True, blank=True)
	recording_creator = models.CharField(max_length=250, null=True, blank=True)
	generation = models.CharField(max_length=250, null=True, blank=True)
	location_of_original = models.CharField(max_length=250, null=True, blank=True)
	online = models.NullBooleanField(null=True, blank=True)
	online_link = models.CharField(max_length=250, null=True, blank=True)
	online_link_mediadrop = models.CharField(max_length=250, null=True, blank=True)
	online_title = models.CharField(max_length=250, null=True, blank=True)
	date_of_acquisition = models.DateField(default=datetime.now)
	acquired_from = models.CharField(max_length=250, null=True, blank=True)
	chain_of_custody_notes = models.TextField(max_length=5000, null=True, blank=True)
	STATUS = (
		('R', 'Restricted'),
		('U', 'Unrestricted'),
	)
	security_restriction_status = models.CharField(max_length=250, null=True, blank=True, choices=STATUS)
	security_restriction_notes = models.TextField(max_length=5000, null=True, blank=True)
	date_of_fixity_check = models.DateTimeField(default=datetime.now, null=True, blank=True)
	md5_hash = models.CharField(max_length=25000, null=True, blank=True)
	rights_owner = models.CharField(max_length=250, null=True, blank=True)
	rights_declaration = models.CharField(max_length=250, null=True, blank=True)
	creator_willing_witness = models.NullBooleanField(null=True, blank=True)
	PRIORITY_LIST = (
        ('UR', 'Urgent'),
        ('HP', 'High priority'),
        ('P', 'Priority'),
        ('LP', 'Low Priority'),
        ('CR', 'Case Rejected'),
    )
	priority = models.CharField(max_length=250, null=True, blank=True, choices=PRIORITY_LIST)
	notes = models.TextField(max_length=5000, null=True, blank=True)
	added_date = models.DateField(default=datetime.now)
	source_connection = models.ManyToManyField(SourceConnection, blank=True)
	creator = models.ForeignKey(User, null=True, blank=True)

	def __unicode__(self):
		return self.name
	def getCreatorID(self):
		if self.creator:
			return self.creator.username
		else:
			return 'ghost user'

	def to_json_dict(self):
		data = {
		'id' : self.id,
		'title': self.name,
		}
		return data

	def save(self, *args, **kwargs):
		super(DatabaseEntry, self).save(*args, **kwargs)


class DatabaseFilter(django_filters.FilterSet):
	class Meta:
		model = DatabaseEntry
		fields = ['type_of_violation','location',]
	'''
	def __init__(self, *args, **kwargs):
		super(DatabaseFilter, self).__init__(*args, **kwargs)
		self.filters['type_of_violation'].extra.update({'empty_label': 'All Violation Types'})
		#self.filters['location'].extra.update({'empty_label':'All Locations'})
	'''