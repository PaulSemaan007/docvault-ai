"""
Workflow Automation API endpoints.
Create and manage document processing rules.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any

from app.security.jwt import get_current_user, require_role
from app.security.audit import log_action
from app.services.workflow_service import WorkflowService

router = APIRouter()


class WorkflowCondition(BaseModel):
    """A single condition in a workflow rule."""
    field: str  # classification, entity_type, entity_value, file_size, etc.
    operator: str  # equals, contains, greater_than, less_than, in
    value: Any


class WorkflowAction(BaseModel):
    """An action to perform when conditions are met."""
    type: str  # tag, notify, move, approve_request
    params: dict


class CreateWorkflowRequest(BaseModel):
    name: str
    description: Optional[str] = None
    conditions: List[WorkflowCondition]
    actions: List[WorkflowAction]
    is_active: bool = True


class WorkflowResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    conditions: List[dict]
    actions: List[dict]
    is_active: bool
    created_by: str
    created_at: str
    trigger_count: int


class WorkflowListResponse(BaseModel):
    workflows: List[WorkflowResponse]
    total: int


@router.post("", response_model=WorkflowResponse)
async def create_workflow(
    request: CreateWorkflowRequest,
    current_user: dict = Depends(require_role(["admin", "manager"]))
):
    """
    Create a new workflow automation rule.

    Example workflow: "Auto-tag invoices over $10,000 as 'high-value' and notify finance"

    Conditions:
    - classification equals "invoice"
    - entity_type equals "MONEY" AND entity_value greater_than 10000

    Actions:
    - tag: {"tag": "high-value"}
    - notify: {"email": "finance@company.com", "message": "High-value invoice received"}
    """
    workflow_service = WorkflowService()

    workflow = await workflow_service.create(
        name=request.name,
        description=request.description,
        conditions=[c.model_dump() for c in request.conditions],
        actions=[a.model_dump() for a in request.actions],
        is_active=request.is_active,
        created_by=current_user["id"]
    )

    await log_action(
        user_id=current_user["id"],
        action="WORKFLOW_CREATED",
        resource_type="workflow",
        resource_id=workflow["id"],
        details={"name": request.name}
    )

    return WorkflowResponse(**workflow)


@router.get("", response_model=WorkflowListResponse)
async def list_workflows(
    is_active: Optional[bool] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    List all workflow rules.
    """
    workflow_service = WorkflowService()

    workflows = await workflow_service.list(is_active=is_active)

    return WorkflowListResponse(
        workflows=[WorkflowResponse(**w) for w in workflows],
        total=len(workflows)
    )


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(
    workflow_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific workflow by ID.
    """
    workflow_service = WorkflowService()

    workflow = await workflow_service.get(workflow_id)

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return WorkflowResponse(**workflow)


@router.put("/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(
    workflow_id: str,
    request: CreateWorkflowRequest,
    current_user: dict = Depends(require_role(["admin", "manager"]))
):
    """
    Update an existing workflow rule.
    """
    workflow_service = WorkflowService()

    workflow = await workflow_service.get(workflow_id)

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    updated = await workflow_service.update(
        workflow_id=workflow_id,
        name=request.name,
        description=request.description,
        conditions=[c.model_dump() for c in request.conditions],
        actions=[a.model_dump() for a in request.actions],
        is_active=request.is_active
    )

    await log_action(
        user_id=current_user["id"],
        action="WORKFLOW_UPDATED",
        resource_type="workflow",
        resource_id=workflow_id
    )

    return WorkflowResponse(**updated)


@router.delete("/{workflow_id}")
async def delete_workflow(
    workflow_id: str,
    current_user: dict = Depends(require_role(["admin"]))
):
    """
    Delete a workflow rule.
    """
    workflow_service = WorkflowService()

    workflow = await workflow_service.get(workflow_id)

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    await workflow_service.delete(workflow_id)

    await log_action(
        user_id=current_user["id"],
        action="WORKFLOW_DELETED",
        resource_type="workflow",
        resource_id=workflow_id,
        details={"name": workflow["name"]}
    )

    return {"message": "Workflow deleted successfully"}


@router.post("/{workflow_id}/toggle")
async def toggle_workflow(
    workflow_id: str,
    current_user: dict = Depends(require_role(["admin", "manager"]))
):
    """
    Toggle a workflow's active status.
    """
    workflow_service = WorkflowService()

    workflow = await workflow_service.get(workflow_id)

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    updated = await workflow_service.update(
        workflow_id=workflow_id,
        is_active=not workflow["is_active"]
    )

    await log_action(
        user_id=current_user["id"],
        action="WORKFLOW_TOGGLED",
        resource_type="workflow",
        resource_id=workflow_id,
        details={"is_active": updated["is_active"]}
    )

    return {"is_active": updated["is_active"]}
