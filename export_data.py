import os
import django
import json
from io import StringIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homeserve.settings')
django.setup()

from django.core.management import call_command

# Export to string buffer
out = StringIO()
call_command('dumpdata', 
             '--natural-foreign', 
             '--natural-primary',
             '-e', 'contenttypes',
             '-e', 'auth.Permission',
             '--indent', '2',
             stdout=out)

# Write to file with UTF-8 encoding
with open('datadump.json', 'w', encoding='utf-8') as f:
    f.write(out.getvalue())

print("✅ Data exported successfully to datadump.json")
print(f"File size: {os.path.getsize('datadump.json')} bytes")
