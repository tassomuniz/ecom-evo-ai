"""
┌──────────────────────────────────────────────────────────────────────────────┐
│ @author: Davidson Gomes                                                      │
│ @file: service_providers.py                                                  │
│ Developed by: Davidson Gomes                                                 │
│ Creation date: May 13, 2025                                                  │
│ Contact: contato@evolution-api.com                                           │
├──────────────────────────────────────────────────────────────────────────────┤
│ @copyright © Evolution API 2025. All rights reserved.                        │
│ Licensed under the Apache License, Version 2.0                               │
│                                                                              │
│ You may not use this file except in compliance with the License.             │
│ You may obtain a copy of the License at                                      │
│                                                                              │
│    http://www.apache.org/licenses/LICENSE-2.0                                │
│                                                                              │
│ Unless required by applicable law or agreed to in writing, software          │
│ distributed under the License is distributed on an "AS IS" BASIS,            │
│ WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.     │
│ See the License for the specific language governing permissions and          │
│ limitations under the License.                                               │
├──────────────────────────────────────────────────────────────────────────────┤
│ @important                                                                   │
│ For any future changes to the code in this file, it is recommended to        │
│ include, together with the modification, the information of the developer    │
│ who changed it and the date of modification.                                 │
└──────────────────────────────────────────────────────────────────────────────┘
"""

import os
import logging
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.sessions import DatabaseSessionService
from google.adk.memory import InMemoryMemoryService
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Import settings after loading .env
from src.config.settings import settings
from src.services.crewai.session_service import CrewSessionService

# Configure logger
logger = logging.getLogger(__name__)

# Debug logging to understand what's happening
logger.info(f"AI_ENGINE from settings: {settings.AI_ENGINE}")
logger.info(f"POSTGRES_CONNECTION_STRING from settings: {settings.POSTGRES_CONNECTION_STRING}")

# Verify that the database URL is not None
if not settings.POSTGRES_CONNECTION_STRING:
    raise ValueError("POSTGRES_CONNECTION_STRING is None or empty. Please check your .env configuration.")

try:
    if settings.AI_ENGINE == "crewai":
        logger.info("Using CrewAI session service")
        session_service = CrewSessionService(db_url=settings.POSTGRES_CONNECTION_STRING)
    else:
        logger.info("Using ADK DatabaseSessionService")
        session_service = DatabaseSessionService(
            db_url=settings.POSTGRES_CONNECTION_STRING
        )
    logger.info("Session service initialized successfully")
except Exception as e:
    logger.error(f"Error initializing session service: {str(e)}")
    logger.info("Falling back to CrewAI session service with SQLite")
    # Fallback to CrewAI with SQLite for development
    session_service = CrewSessionService(db_url="sqlite:///./evo_ai_fallback.db")

artifacts_service = InMemoryArtifactService()
memory_service = InMemoryMemoryService()
