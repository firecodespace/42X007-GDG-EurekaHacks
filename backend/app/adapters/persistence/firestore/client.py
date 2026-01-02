from google.cloud import firestore


def get_firestore_client() -> firestore.Client:
    return firestore.Client()
