from django.contrib import admin
from database.models import *
from django.forms import CheckboxSelectMultiple
from modeltranslation.admin import TranslationAdmin
from leaflet.admin import LeafletGeoAdmin

@admin.register(Collection)
class CollectionAdmin(TranslationAdmin):
    pass

# @admin.register(InternationalInstrument)
# class InternationalInstrumentEntryAdmin(TranslationAdmin):
#   pass

# @admin.register(MediaContentType)
# class MediaContentTypeAdmin(TranslationAdmin):
#   pass

# @admin.register(SourceConnection)
# class SourceConnectionAdmin(TranslationAdmin):
#   pass

@admin.register(LocationPlace)
class LocationPlaceAdmin(TranslationAdmin, LeafletGeoAdmin):
  list_filter = ['name', 'region',]
  search_fields = ['name']

# @admin.register(Device)
# class DeviceAdmin(TranslationAdmin):
#   pass

@admin.register(ViolationType)
class ViolationTypeAdmin(TranslationAdmin):
  pass

@admin.register(DatabaseEntry)
class DatabaseEntryAdmin(TranslationAdmin, LeafletGeoAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    list_filter = ['staff_id', 'type_of_violation', 'location', 'media_content_type','priority','creator','added_date']
    list_display = (
    'reference_code',
    'validated',
    'location',
    'youtube_id',
    'video_source',
    'staff_id',
    'recording_date',
    'online',
    'priority',
    )
    readonly_fields=('initial_data_hash',)
    fieldsets = (
        ('UUID', {
            'fields': ('reference_code',
                       'validated',
                       'initial_data_hash',
                )
        }),
        ('Meta Fields', {
            'fields': (
                'description',
                )
        }),
        ('Video Fields', {
            'fields': (
                'video_url',
                'thumbnail',
                'collections'
            )
        }),
        ('Location Fields', {
            'fields': (
                'geom',
                'location',
                'location_latitude',
                'location_longitude',
            )
        }),
        ('Public Fields', {
            'fields': (
              'recording_date',
                'edited',
                'youtube_id',
              ('file_size','duration',),
              'reliability_score',
              'chain_of_custody_notes_public',
              'media_content_type',
              'device_used',
              'languages',
              'finding_aids',
              'cloths_and_uniforms',
              'type_of_violation',
              'graphic_content',
              'keywords',
              # 'international_instrument',
              # 'international_instrument_notes',
              'landmarks',
              'weather_in_media',
              'weapons_used',
              'urls_and_news',
            )
        }),
        ('Private Fields', {
            'fields': (
              'staff_id',
              'file_name',
              'recording_creator',
              'generation',
              'location_of_original',
              'online',
              'online_link',
              'online_link_mediadrop',
              'online_title',
              'date_of_acquisition',
              'acquired_from',
              'chain_of_custody_notes',
              'security_restriction_status',
              'security_restriction_notes',
              'date_of_fixity_check',
              'md5_hash',
              'rights_owner',
              'rights_declaration',
              'creator_willing_witness',
              'priority',
              'notes',
              'source_connection',
              'added_date',
              'creator',
              )
        }),

    )
    class Media:
            js = (
                '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
                '//ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
                'modeltranslation/js/tabbed_translation_fields.js',
            )
            css = {
                'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
            }


    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator = request.user
        obj.save()

