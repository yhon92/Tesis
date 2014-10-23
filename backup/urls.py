from django.conf.urls import patterns, include, url
from backup.views import *

# users need to be logged in
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('backup.views',
  url(r'^$', login_required(backup_index), name="index_backup"),
  url(r'^export/', login_required(export_database), name="export_database"),
  url(r'^import/', login_required(import_database), name="import_database"),
  url(r'^media/export/', login_required(export_media), name="export_mediaroot"),
)

# from django.conf.urls.defaults import *