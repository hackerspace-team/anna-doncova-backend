import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore_async

from AnnaDoncovaBackend import settings

cred = credentials.Certificate(os.path.join(settings.BASE_DIR, 'service_account_key_testing.json'))
default_app = firebase_admin.initialize_app(cred)
db = firestore_async.client()
