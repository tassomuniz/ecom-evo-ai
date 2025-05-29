"""
┌──────────────────────────────────────────────────────────────────────────────┐
│ @author: Davidson Gomes                                                      │
│ @file: a2a_enhanced_types.py                                                 │
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

import logging
from typing import Dict, Any, Optional, List
from uuid import uuid4

try:
    from a2a.types import (
        AgentCard as SDKAgentCard,
        AgentCapabilities as SDKAgentCapabilities,
        AgentSkill as SDKAgentSkill,
        AgentProvider as SDKAgentProvider,
        Message as SDKMessage,
        Task as SDKTask,
        TaskStatus as SDKTaskStatus,
        TaskState as SDKTaskState,
        Part as SDKPart,
        TextPart as SDKTextPart,
        FilePart as SDKFilePart,
        Artifact as SDKArtifact,
    )

    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False
    logging.warning("a2a-sdk not available, falling back to custom types")

from src.schemas.a2a_types import (
    Task as CustomTask,
    TaskStatus as CustomTaskStatus,
    TaskState as CustomTaskState,
    Message as CustomMessage,
    AgentCard as CustomAgentCard,
    AgentCapabilities as CustomAgentCapabilities,
    AgentSkill as CustomAgentSkill,
    AgentProvider as CustomAgentProvider,
    Artifact as CustomArtifact,
)

logger = logging.getLogger(__name__)


class A2ATypeValidator:
    """Validate and convert types between custom and official SDK implementations"""

    @staticmethod
    def is_sdk_available() -> bool:
        """Check if SDK is available"""
        return SDK_AVAILABLE

    @staticmethod
    def validate_agent_card(card_data: Dict[str, Any]) -> Optional[Any]:
        """Validate agent card using SDK types if available"""
        if not SDK_AVAILABLE:
            logger.debug("SDK not available, using custom validation")
            return CustomAgentCard(**card_data)

        try:
            return SDKAgentCard(**card_data)
        except Exception as e:
            logger.warning(f"SDK validation failed, falling back to custom: {e}")
            return CustomAgentCard(**card_data)

    @staticmethod
    def validate_message(message_data: Dict[str, Any]) -> Optional[Any]:
        """Validate message using SDK types if available"""
        if not SDK_AVAILABLE:
            return CustomMessage(**message_data)

        try:
            return SDKMessage(**message_data)
        except Exception as e:
            logger.warning(f"SDK message validation failed: {e}")
            return CustomMessage(**message_data)

    @staticmethod
    def validate_task(task_data: Dict[str, Any]) -> Optional[Any]:
        """Validate task using SDK types if available"""
        if not SDK_AVAILABLE:
            return CustomTask(**task_data)

        try:
            return SDKTask(**task_data)
        except Exception as e:
            logger.warning(f"SDK task validation failed: {e}")
            return CustomTask(**task_data)


class A2ATypeConverter:
    """Convert between custom and SDK types"""

    @staticmethod
    def custom_task_to_sdk(custom_task: CustomTask) -> Optional[Any]:
        """Convert CustomTask to SDKTask"""
        if not SDK_AVAILABLE:
            return custom_task

        try:
            # Convert status
            sdk_status = None
            if custom_task.status:
                sdk_status = A2ATypeConverter.custom_task_status_to_sdk(
                    custom_task.status
                )

            # If status is None, create a basic status
            if not sdk_status:
                sdk_status = SDKTaskStatus(
                    state=SDKTaskState.unknown, message=None, timestamp=None
                )

            # Convert artifacts
            sdk_artifacts = []
            if custom_task.artifacts:
                for artifact in custom_task.artifacts:
                    sdk_artifact = A2ATypeConverter.custom_artifact_to_sdk(artifact)
                    if sdk_artifact:
                        sdk_artifacts.append(sdk_artifact)

            # Convert history
            sdk_history = []
            if custom_task.history:
                for message in custom_task.history:
                    sdk_message = A2ATypeConverter.custom_message_to_sdk(message)
                    if sdk_message:
                        sdk_history.append(sdk_message)

            return SDKTask(
                id=custom_task.id,
                contextId=custom_task.sessionId,
                kind="task",  # New field in SDK
                status=sdk_status,
                artifacts=sdk_artifacts if sdk_artifacts else None,
                history=sdk_history if sdk_history else None,
                metadata=custom_task.metadata,
            )
        except Exception as e:
            logger.error(f"Failed to convert custom task to SDK: {e}")
            return None

    @staticmethod
    def sdk_task_to_custom(sdk_task) -> Optional[CustomTask]:
        """Convert SDKTask to CustomTask"""
        if not SDK_AVAILABLE:
            return sdk_task

        try:
            # Convert status
            custom_status = A2ATypeConverter.sdk_task_status_to_custom(sdk_task.status)

            # Convert artifacts
            custom_artifacts = []
            if sdk_task.artifacts:
                for artifact in sdk_task.artifacts:
                    custom_artifact = A2ATypeConverter.sdk_artifact_to_custom(artifact)
                    if custom_artifact:
                        custom_artifacts.append(custom_artifact)

            # Convert history
            custom_history = []
            if sdk_task.history:
                for message in sdk_task.history:
                    custom_message = A2ATypeConverter.sdk_message_to_custom(message)
                    if custom_message:
                        custom_history.append(custom_message)

            return CustomTask(
                id=sdk_task.id,
                sessionId=sdk_task.contextId,
                status=custom_status,
                artifacts=custom_artifacts if custom_artifacts else None,
                history=custom_history if custom_history else None,
                metadata=sdk_task.metadata,
            )
        except Exception as e:
            logger.error(f"Failed to convert SDK task to custom: {e}")
            return None

    @staticmethod
    def custom_task_status_to_sdk(custom_status: CustomTaskStatus) -> Optional[Any]:
        """Convert CustomTaskStatus to SDKTaskStatus"""
        if not SDK_AVAILABLE:
            return custom_status

        try:
            # Map states
            state_mapping = {
                CustomTaskState.SUBMITTED: SDKTaskState.submitted,
                CustomTaskState.WORKING: SDKTaskState.working,
                CustomTaskState.INPUT_REQUIRED: SDKTaskState.input_required,
                CustomTaskState.COMPLETED: SDKTaskState.completed,
                CustomTaskState.CANCELED: SDKTaskState.canceled,
                CustomTaskState.FAILED: SDKTaskState.failed,
                CustomTaskState.UNKNOWN: SDKTaskState.unknown,
            }

            sdk_state = state_mapping.get(custom_status.state, SDKTaskState.unknown)

            # Convert message if exists
            sdk_message = None
            if custom_status.message:
                sdk_message = A2ATypeConverter.custom_message_to_sdk(
                    custom_status.message
                )

            # Convert timestamp to string if it's a datetime
            timestamp_str = custom_status.timestamp
            if hasattr(custom_status.timestamp, "isoformat"):
                timestamp_str = custom_status.timestamp.isoformat()

            return SDKTaskStatus(
                state=sdk_state, message=sdk_message, timestamp=timestamp_str
            )
        except Exception as e:
            logger.error(f"Failed to convert task status: {e}")
            return None

    @staticmethod
    def sdk_task_status_to_custom(sdk_status) -> Optional[CustomTaskStatus]:
        """Convert SDKTaskStatus to CustomTaskStatus"""
        if not SDK_AVAILABLE:
            return sdk_status

        try:
            # Map states back
            state_mapping = {
                SDKTaskState.submitted: CustomTaskState.SUBMITTED,
                SDKTaskState.working: CustomTaskState.WORKING,
                SDKTaskState.input_required: CustomTaskState.INPUT_REQUIRED,
                SDKTaskState.completed: CustomTaskState.COMPLETED,
                SDKTaskState.canceled: CustomTaskState.CANCELED,
                SDKTaskState.failed: CustomTaskState.FAILED,
                SDKTaskState.unknown: CustomTaskState.UNKNOWN,
            }

            custom_state = state_mapping.get(sdk_status.state, CustomTaskState.UNKNOWN)

            # Convert message if exists
            custom_message = None
            if sdk_status.message:
                custom_message = A2ATypeConverter.sdk_message_to_custom(
                    sdk_status.message
                )

            return CustomTaskStatus(
                state=custom_state,
                message=custom_message,
                timestamp=sdk_status.timestamp,
            )
        except Exception as e:
            logger.error(f"Failed to convert SDK task status: {e}")
            return None

    @staticmethod
    def custom_message_to_sdk(custom_message: CustomMessage) -> Optional[Any]:
        """Convert CustomMessage to SDKMessage"""
        if not SDK_AVAILABLE:
            return custom_message

        try:
            # Convert parts
            sdk_parts = []
            for part in custom_message.parts:
                if hasattr(part, "type"):
                    if part.type == "text":
                        sdk_parts.append(
                            SDKTextPart(
                                kind="text",
                                text=part.text,
                                metadata=getattr(part, "metadata", None),
                            )
                        )
                    elif part.type == "file":
                        sdk_parts.append(
                            SDKFilePart(
                                kind="file",
                                file=part.file,
                                metadata=getattr(part, "metadata", None),
                            )
                        )

            return SDKMessage(
                role=custom_message.role,
                parts=sdk_parts,
                messageId=getattr(custom_message, "messageId", str(uuid4())),
                metadata=custom_message.metadata,
            )
        except Exception as e:
            logger.error(f"Failed to convert message: {e}")
            return None

    @staticmethod
    def sdk_message_to_custom(sdk_message) -> Optional[CustomMessage]:
        """Convert SDKMessage to CustomMessage"""
        if not SDK_AVAILABLE:
            logger.info("SDK not available, returning original message")
            return sdk_message

        try:
            logger.info(f"Converting SDK message to custom: {type(sdk_message)}")
            logger.info(f"SDK message role: {getattr(sdk_message, 'role', 'NO_ROLE')}")
            logger.info(
                f"SDK message parts: {getattr(sdk_message, 'parts', 'NO_PARTS')}"
            )
            logger.info(
                f"SDK message parts length: {len(getattr(sdk_message, 'parts', []))}"
            )

            # Convert parts back
            custom_parts = []
            for idx, part in enumerate(sdk_message.parts):
                logger.info(f"Processing part {idx}: {type(part)}")
                logger.info(f"Part repr: {repr(part)}")

                try:
                    # The SDK TextPart does not allow direct access via getattr
                    # We will extract data from the repr string
                    part_repr = repr(part)
                    logger.info(f"Parsing part repr: {part_repr}")

                    # Check if it's a TextPart
                    if "TextPart" in str(type(part)) or "kind='text'" in part_repr:
                        logger.info("Detected TextPart")

                        # Extract text from repr
                        import re

                        text_match = re.search(r"text='([^']*)'", part_repr)
                        text_content = text_match.group(1) if text_match else ""

                        logger.info(f"Extracted text: {text_content}")

                        # Create dictionary instead of SimpleNamespace for Pydantic compatibility
                        text_part = {
                            "type": "text",
                            "text": text_content,
                            "metadata": None,
                        }
                        custom_parts.append(text_part)
                        logger.info(f"Created text part dict: {text_part}")

                    elif "FilePart" in str(type(part)) or "kind='file'" in part_repr:
                        logger.info("Detected FilePart")

                        # For file parts, we would need to extract more data
                        # For now, create a basic structure
                        file_part = {
                            "type": "file",
                            "file": None,  # It would be necessary to extract from SDK
                            "metadata": None,
                        }
                        custom_parts.append(file_part)
                        logger.info(f"Created file part dict: {file_part}")

                    else:
                        logger.warning(f"Unknown part type in repr: {part_repr}")
                        # Fallback: try to extract any available text
                        if "text=" in part_repr:
                            import re

                            text_match = re.search(r"text='([^']*)'", part_repr)
                            if text_match:
                                fallback_text = text_match.group(1)
                                text_part = {
                                    "type": "text",
                                    "text": fallback_text,
                                    "metadata": None,
                                }
                                custom_parts.append(text_part)
                                logger.info(f"Created fallback text part: {text_part}")

                except Exception as part_error:
                    logger.error(f"Error processing part {idx}: {part_error}")
                    import traceback

                    logger.error(f"Part processing traceback: {traceback.format_exc()}")
                    continue

            logger.info(f"Total custom parts created: {len(custom_parts)}")

            # Convert role from enum to string if necessary
            role_str = sdk_message.role
            if hasattr(sdk_message.role, "value"):
                role_str = sdk_message.role.value
                logger.info(f"Converted role from enum: {role_str}")
            elif not isinstance(sdk_message.role, str):
                role_str = str(sdk_message.role)
                logger.info(f"Converted role to string: {role_str}")

            custom_message = CustomMessage(
                role=role_str, parts=custom_parts, metadata=sdk_message.metadata
            )

            logger.info(
                f"Created custom message: role={custom_message.role}, parts_count={len(custom_message.parts)}"
            )
            return custom_message

        except Exception as e:
            logger.error(f"Failed to convert SDK message: {e}")
            import traceback

            logger.error(f"Full traceback: {traceback.format_exc()}")
            return None

    @staticmethod
    def custom_artifact_to_sdk(custom_artifact: CustomArtifact) -> Optional[Any]:
        """Convert CustomArtifact to SDKArtifact"""
        if not SDK_AVAILABLE:
            return custom_artifact

        try:
            # Convert parts to SDK format
            sdk_parts = []
            if custom_artifact.parts:
                for part in custom_artifact.parts:
                    # If part is a dictionary, convert to appropriate SDK object
                    if isinstance(part, dict):
                        if part.get("type") == "text":
                            sdk_parts.append(
                                SDKTextPart(
                                    kind="text",
                                    text=part.get("text", ""),
                                    metadata=part.get("metadata"),
                                )
                            )
                        elif part.get("type") == "file":
                            sdk_parts.append(
                                SDKFilePart(
                                    kind="file",
                                    file=part.get("file"),
                                    metadata=part.get("metadata"),
                                )
                            )
                    # If it's already a SDK object, use it directly
                    elif hasattr(part, "kind"):
                        sdk_parts.append(part)
                    # If it's a custom TextPart, convert it
                    else:
                        # Fallback: assume text part
                        text_content = getattr(part, "text", str(part))
                        sdk_parts.append(
                            SDKTextPart(
                                kind="text",
                                text=text_content,
                                metadata=getattr(part, "metadata", None),
                            )
                        )

            # Generate artifactId if it doesn't exist
            artifact_id = getattr(custom_artifact, "artifactId", None)
            if not artifact_id:
                from uuid import uuid4

                artifact_id = str(uuid4())

            return SDKArtifact(
                artifactId=artifact_id,
                name=custom_artifact.name,
                description=custom_artifact.description,
                parts=sdk_parts,
                metadata=custom_artifact.metadata,
            )
        except Exception as e:
            logger.error(f"Failed to convert artifact: {e}")
            return None

    @staticmethod
    def sdk_artifact_to_custom(sdk_artifact) -> Optional[CustomArtifact]:
        """Convert SDKArtifact to CustomArtifact"""
        if not SDK_AVAILABLE:
            return sdk_artifact

        try:
            return CustomArtifact(
                name=sdk_artifact.name,
                description=sdk_artifact.description,
                parts=sdk_artifact.parts,
                index=getattr(sdk_artifact, "index", 0),
                append=getattr(sdk_artifact, "append", None),
                lastChunk=getattr(sdk_artifact, "lastChunk", None),
                metadata=sdk_artifact.metadata,
            )
        except Exception as e:
            logger.error(f"Failed to convert SDK artifact: {e}")
            return None

    @staticmethod
    def custom_agent_card_to_sdk(custom_card: CustomAgentCard) -> Optional[Any]:
        """Convert CustomAgentCard to SDKAgentCard"""
        if not SDK_AVAILABLE:
            return custom_card

        try:
            # Convert capabilities
            sdk_capabilities = None
            if custom_card.capabilities:
                sdk_capabilities = SDKAgentCapabilities(
                    streaming=custom_card.capabilities.streaming,
                    pushNotifications=custom_card.capabilities.pushNotifications,
                    stateTransitionHistory=custom_card.capabilities.stateTransitionHistory,
                )

            # Convert provider
            sdk_provider = None
            if custom_card.provider:
                sdk_provider = SDKAgentProvider(
                    organization=custom_card.provider.organization,
                    url=custom_card.provider.url,
                )

            # Convert skills
            sdk_skills = []
            if custom_card.skills:
                for skill in custom_card.skills:
                    sdk_skill = SDKAgentSkill(
                        id=skill.id,
                        name=skill.name,
                        description=skill.description,
                        tags=skill.tags,
                        examples=skill.examples,
                        inputModes=skill.inputModes,
                        outputModes=skill.outputModes,
                    )
                    sdk_skills.append(sdk_skill)

            return SDKAgentCard(
                name=custom_card.name,
                description=custom_card.description,
                url=custom_card.url,
                version=custom_card.version,
                documentationUrl=custom_card.documentationUrl,
                provider=sdk_provider,
                capabilities=sdk_capabilities,
                authentication=custom_card.authentication,
                defaultInputModes=custom_card.defaultInputModes,
                defaultOutputModes=custom_card.defaultOutputModes,
                skills=sdk_skills,
            )
        except Exception as e:
            logger.error(f"Failed to convert agent card: {e}")
            return None


# Utility functions to facilitate usage
def validate_with_sdk(data: Dict[str, Any], data_type: str) -> Any:
    """Utility function to validate data with SDK when available"""
    validator = A2ATypeValidator()

    if data_type == "agent_card":
        return validator.validate_agent_card(data)
    elif data_type == "message":
        return validator.validate_message(data)
    elif data_type == "task":
        return validator.validate_task(data)
    else:
        raise ValueError(f"Unsupported data type: {data_type}")


def convert_to_sdk_format(custom_obj: Any) -> Any:
    """Utility function to convert custom object to SDK format"""
    converter = A2ATypeConverter()

    if isinstance(custom_obj, CustomTask):
        return converter.custom_task_to_sdk(custom_obj)
    elif isinstance(custom_obj, CustomMessage):
        return converter.custom_message_to_sdk(custom_obj)
    elif isinstance(custom_obj, CustomAgentCard):
        return converter.custom_agent_card_to_sdk(custom_obj)
    else:
        logger.warning(f"No converter available for type: {type(custom_obj)}")
        return custom_obj


def convert_from_sdk_format(sdk_obj: Any) -> Any:
    """Utility function to convert SDK object to custom format"""
    converter = A2ATypeConverter()

    if SDK_AVAILABLE:
        if isinstance(sdk_obj, SDKTask):
            return converter.sdk_task_to_custom(sdk_obj)
        elif isinstance(sdk_obj, SDKMessage):
            return converter.sdk_message_to_custom(sdk_obj)

    return sdk_obj
