import os
import firebase_admin
from firebase_admin import credentials, firestore_async, storage

from AnnaDoncovaBackend import settings

certificate_name = 'service_account_key_testing.json' if settings.IS_DEV else 'service_account_key_production.json'
storage_name = 'anna-doncova-testing.appspot.com' if settings.IS_DEV else 'anna-doncova-production.appspot.com'

path_to_credentials = os.path.join(settings.BASE_DIR, certificate_name)
cred = credentials.Certificate(path_to_credentials)
default_app = firebase_admin.initialize_app(cred, {
    'storageBucket': storage_name,
})
db = firestore_async.client()
bucket = storage.bucket()
