import base64
import json

import firebase_admin
from firebase_admin import credentials

from app.core.config import settings

_firebase_app: firebase_admin.App | None = None


def get_firebase_app() -> firebase_admin.App:
    global _firebase_app
    if _firebase_app is not None:
        return _firebase_app

    if not settings.FIREBASE_CREDENTIALS_BASE64:
        raise RuntimeError(
            "FIREBASE_CREDENTIALS_BASE64 is not set. Generate a service account "
            "key in Firebase Console > Project settings > Service accounts, "
            "base64-encode the downloaded JSON, and set it as this env var."
        )

    # Strip whitespace/newlines that web UI text inputs sometimes introduce
    # when pasting a long single-line value.
    b64 = "".join(settings.FIREBASE_CREDENTIALS_BASE64.split())
    cred_json = base64.b64decode(b64).decode("utf-8")
    cred_dict = json.loads(cred_json)
    _firebase_app = firebase_admin.initialize_app(credentials.Certificate(cred_dict))
    return _firebase_app
