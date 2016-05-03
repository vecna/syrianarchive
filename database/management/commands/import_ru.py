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
    help = "Imports locations from json file - Forein keys wont work any more -- deletes old.  for site deploy"
    def add_arguments(self, parser):
        pass
    def handle(self, *args, **options):
        print "Imports the testing spreadsheet of russian attacks"
        var = raw_input("warning: this will remove all data from the Incidents database, resetting them to their original state.  are you sure? (yes): ")
        print "you entered", var
        if var != "yes":
            return
        notfound = []

        def find_location(location_string):
          locations = LocationPlace.objects.filter(name_en__icontains=location_string.strip())
          location = None
          if locations:
            location = locations[0]
            print "found! %s", location
          else:
            print location_string, "not found"
            notfound.append(location_string)
          return location

        def latlon_conversion(old):
          direction = {'N':-1, 'S':1, 'E': -1, 'W':1}
          new = old.replace(u'°',' ').replace('\'',' ').replace('"',' ')
          new = new.split()
          new_dir = new.pop()
          new.extend([0,0,0])
          if "." in str(new_dir):
              return old
          else:
              return (int(new[0])+int(new[1])/60.0+int(new[2])/3600.0) * direction[new_dir]

        dates_not_parsed = []
        def parse_date(date=None):
          if date:
            #spreadsheet date format: 08/21/13 12:00 AM
            try:
              print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
              newdate = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.000Z')
            except:
              print "parse no woek!! eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
              dates_not_parsed.append(date)
              return datetime.now()
            #newdate = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
            return newdate
          print "nodate oooooooooooooooooooooooooooooooooooooooooooo"
          dates_not_parsed.append(date)
          return datetime.now

        def find_violationtype(violation_string):
          violations = ViolationType.objects.filter(name_en__icontains=violation_string)
          violation = None
          if violations:
            violation = violations[0]
            print "found %s" % violation
          else:
            pass
          return violation

        import requests
        from bs4 import BeautifulSoup
        media_url = 'http://media.syrianarchive.org/files/russian_attacks/'
        soup = BeautifulSoup(requests.get(media_url).text)
        links = []
        for a in soup.find_all('a'):
          links.append(a['href'])
        def find_video_name(video_string):
          print(video_string)
          print [s for s in links if video_string in s]
          try:
            return [s for s in links if video_string in s][0]
          except:
            return ""


        print BASE_PATH
        with open( BASE_PATH + '/database/data/ru_at.csv', 'r') as f:
          reader = csv.DictReader(f, (
                "reference_code",
                "youtube_id",
                "youtube_url",
                "description_ar",
                "date",
                "source",
                "location_en",
                "location_ar",
                "lat",
                "lon",
                "description_en",
                "violationtype",
                ))
          print reader
          #print [ row["id"] for row in reader ]
          print reader
          next(reader)
          for row in reader:
            print "hi"
            entry, created = DatabaseEntry.objects.get_or_create(
              name = row["reference_code"].decode('utf8', 'ignore'),
              reference_code = row["reference_code"].decode('utf8', 'ignore'),
              staff_id = "import script",
              location = find_location(row["location_en"]),
              location_latitude = row["lat"].decode('utf8', 'ignore'),
              location_longitude = row ["lon"].decode('utf8', 'ignore'),
              #time = parse_date(row["time"]),
              description_en = row["description_en"].decode('utf8', 'ignore'),
              description_ar = row["description_ar"].decode('utf8', 'ignore'),
              type_of_violation = find_violationtype(row["violationtype"].decode('utf8', 'ignore')),
              #weapons_used = row["weapons"],
              acquired_from_en = row["source"].decode('utf8', 'ignore'),
              acquired_from_ar = row["source"].decode('utf8', 'ignore'),
              #source_connection = row["sources"],
              recording_date = parse_date(row["date"].decode('utf8', 'ignore')),
              video_url = "/files/russian_attacks/" + find_video_name(row["youtube_id"].decode('utf8', 'ignore')),
              online_link = row["youtube_url"].decode('utf8', 'ignore'),
              youtube_id = row["youtube_id"].decode('utf8', 'ignore'),
              online_title = "",
              graphic_content = True
              )

            print(entry)

            try:
              if entry.location_longitude and entry.location_latitude:
                print "adding geom"
                geofield = {'type': 'Point', 'coordinates': [float(latlon_conversion(entry.location_longitude)), float(latlon_conversion(entry.location_latitude))]}
                entry.geom = geofield
                entry.save()
                print entry.geom
            except:
              print("failed geom!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

            print entry.name
          print [ loc for loc in notfound]
          print "bad date pase ", len(dates_not_parsed)
          print [ date for date in dates_not_parsed ]

