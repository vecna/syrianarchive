# coding: utf-8
from django.core.management.base import BaseCommand, CommandError
from database.models import LocationPlace, DatabaseEntry, ViolationType
from syrianarchive.site_settings import BASE_PATH
import json
import csv
from django.shortcuts import get_object_or_404, render
from djgeojson.fields import PointField, PolygonField
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Point, LineString, MultiLineString
from datetime import datetime
from dateutil.parser import parse

class Command(BaseCommand):
  def handle(self, *args, **options):
    for row in LocationPlace.objects.all()[::-1]:
        if LocationPlace.objects.filter(name_ar=row.name_ar).count() > 1:
            row.delete()
        if LocationPlace.objects.filter(name_en=row.name_en).count() > 1:
            row.delete()