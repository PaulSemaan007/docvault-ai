"""
Workflow Service.
Manages workflow rules and executes automation actions.
"""

from typing import Optional, List, Any
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

# In-memory workflow store
_workflows = {}


class WorkflowService:
    """
    Service for workflow automation operations.
    """

    async def create(
        self,
        name: str,
        description: Optional[str],
        conditions: List[dict],
        actions: List[dict],
        is_active: bool,
        created_by: str
    ) -> dict:
        """
        Create a new workflow rule.
        """
        workflow_id = str(uuid.uuid4())

        workflow = {
            "id": workflow_id,
            "name": name,
            "description": description,
            "conditions": conditions,
            "actions": actions,
            "is_active": is_active,
            "created_by": created_by,
            "created_at": datetime.utcnow().isoformat(),
            "trigger_count": 0
        }

        _workflows[workflow_id] = workflow
        return workflow

    async def get(self, workflow_id: str) -> Optional[dict]:
        """Get a workflow by ID."""
        return _workflows.get(workflow_id)

    async def list(self, is_active: Optional[bool] = None) -> List[dict]:
        """List all workflows with optional active filter."""
        workflows = list(_workflows.values())

        if is_active is not None:
            workflows = [w for w in workflows if w["is_active"] == is_active]

        workflows.sort(key=lambda x: x["created_at"], reverse=True)
        return workflows

    async def update(
        self,
        workflow_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        conditions: Optional[List[dict]] = None,
        actions: Optional[List[dict]] = None,
        is_active: Optional[bool] = None
    ) -> dict:
        """Update a workflow rule."""
        workflow = _workflows.get(workflow_id)
        if not workflow:
            raise Exception("Workflow not found")

        if name is not None:
            workflow["name"] = name
        if description is not None:
            workflow["description"] = description
        if conditions is not None:
            workflow["conditions"] = conditions
        if actions is not None:
            workflow["actions"] = actions
        if is_active is not None:
            workflow["is_active"] = is_active

        return workflow

    async def delete(self, workflow_id: str) -> bool:
        """Delete a workflow rule."""
        if workflow_id in _workflows:
            del _workflows[workflow_id]
            return True
        return False

    async def evaluate(self, document: dict) -> List[dict]:
        """
        Evaluate all active workflows against a document.
        Returns list of triggered workflows.
        """
        triggered = []

        for workflow in _workflows.values():
            if not workflow["is_active"]:
                continue

            if self._check_conditions(document, workflow["conditions"]):
                logger.info(f"Workflow '{workflow['name']}' triggered for document {document['id']}")

                # Execute actions
                await self._execute_actions(document, workflow["actions"])

                # Increment trigger count
                workflow["trigger_count"] += 1

                triggered.append(workflow)

        return triggered

    def _check_conditions(self, document: dict, conditions: List[dict]) -> bool:
        """
        Check if all conditions are met for a document.
        """
        for condition in conditions:
            field = condition["field"]
            operator = condition["operator"]
            value = condition["value"]

            # Get document field value
            if field == "classification":
                doc_value = document.get("classification")
            elif field == "file_size":
                doc_value = document.get("file_size", 0)
            elif field == "mime_type":
                doc_value = document.get("mime_type")
            elif field.startswith("entity_"):
                # Check entity values
                entity_type = field.replace("entity_", "").upper()
                doc_value = self._get_entity_values(document, entity_type)
            else:
                doc_value = document.get(field)

            # Evaluate condition
            if not self._evaluate_condition(doc_value, operator, value):
                return False

        return True

    def _evaluate_condition(
        self,
        doc_value: Any,
        operator: str,
        condition_value: Any
    ) -> bool:
        """Evaluate a single condition."""
        if doc_value is None:
            return False

        if operator == "equals":
            return doc_value == condition_value
        elif operator == "not_equals":
            return doc_value != condition_value
        elif operator == "contains":
            if isinstance(doc_value, list):
                return condition_value in doc_value
            return condition_value.lower() in str(doc_value).lower()
        elif operator == "greater_than":
            return float(doc_value) > float(condition_value)
        elif operator == "less_than":
            return float(doc_value) < float(condition_value)
        elif operator == "in":
            return doc_value in condition_value

        return False

    def _get_entity_values(self, document: dict, entity_type: str) -> List[str]:
        """Get all values of a specific entity type from document."""
        entities = document.get("entities", [])
        return [e["value"] for e in entities if e["type"] == entity_type]

    async def _execute_actions(self, document: dict, actions: List[dict]):
        """Execute workflow actions on a document."""
        for action in actions:
            action_type = action["type"]
            params = action["params"]

            if action_type == "tag":
                # Add tag to document
                tags = document.get("tags", [])
                if params["tag"] not in tags:
                    tags.append(params["tag"])
                    document["tags"] = tags
                logger.info(f"Added tag '{params['tag']}' to document")

            elif action_type == "notify":
                # Send notification (placeholder)
                logger.info(f"Notification: {params.get('message')} to {params.get('email')}")

            elif action_type == "move":
                # Move to folder (placeholder)
                logger.info(f"Would move document to folder: {params.get('folder')}")

            elif action_type == "approve_request":
                # Create approval request (placeholder)
                logger.info(f"Approval requested from: {params.get('approver')}")
