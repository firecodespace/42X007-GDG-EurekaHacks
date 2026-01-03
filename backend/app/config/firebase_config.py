import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import Client
from app.config.settings import settings
from app.shared.logger import logger


_firestore_client: Client | None = None


def initialize_firebase() -> None:
    """Initialize Firebase Admin SDK"""
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(settings.firebase_credentials_full_path)
            firebase_admin.initialize_app(cred, {
                'projectId': settings.firebase_project_id,
            })
            logger.info("Firebase initialized successfully")
        else:
            logger.info("Firebase already initialized")
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {e}")
        raise


def get_firestore_client() -> Client:
    """Get Firestore client instance"""
    global _firestore_client
    
    if _firestore_client is None:
        try:
            _firestore_client = firestore.client()
            logger.info("Firestore client created successfully")
        except Exception as e:
            logger.error(f"Failed to create Firestore client: {e}")
            raise
    
    return _firestore_client


def close_firebase() -> None:
    """Close Firebase connection"""
    global _firestore_client
    
    if _firestore_client is not None:
        _firestore_client = None
        logger.info("Firestore client closed")
