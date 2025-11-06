import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moviesstore.settings')
import django
django.setup()
from django.contrib import admin
print('site_header=', repr(admin.site.site_header))
print('site_title=', repr(admin.site.site_title))
print('index_title=', repr(admin.site.index_title))
