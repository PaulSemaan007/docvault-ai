'use client'

import { useState } from 'react'
import {
  Workflow,
  Plus,
  Play,
  Pause,
  Trash2,
  Edit,
  ChevronRight,
  Zap,
  Tag,
  Mail,
  FolderOpen,
  CheckCircle,
  AlertCircle
} from 'lucide-react'

interface WorkflowRule {
  id: string
  name: string
  description: string
  conditions: Array<{ field: string; operator: string; value: string }>
  actions: Array<{ type: string; params: Record<string, string> }>
  is_active: boolean
  trigger_count: number
  created_at: string
}

export default function WorkflowsPage() {
  const [workflows, setWorkflows] = useState<WorkflowRule[]>([
    {
      id: '1',
      name: 'High-Value Invoice Alert',
      description: 'Tag and notify finance team for invoices over $10,000',
      conditions: [
        { field: 'classification', operator: 'equals', value: 'invoice' },
        { field: 'entity_money', operator: 'greater_than', value: '10000' }
      ],
      actions: [
        { type: 'tag', params: { tag: 'high-value' } },
        { type: 'notify', params: { email: 'finance@company.com', message: 'High-value invoice received' } }
      ],
      is_active: true,
      trigger_count: 23,
      created_at: '2024-01-10T09:00:00Z'
    },
    {
      id: '2',
      name: 'Contract Review Routing',
      description: 'Send contracts to legal team for review',
      conditions: [
        { field: 'classification', operator: 'equals', value: 'contract' }
      ],
      actions: [
        { type: 'tag', params: { tag: 'needs-review' } },
        { type: 'notify', params: { email: 'legal@company.com', message: 'New contract for review' } }
      ],
      is_active: true,
      trigger_count: 15,
      created_at: '2024-01-08T14:30:00Z'
    },
    {
      id: '3',
      name: 'Archive Old Reports',
      description: 'Auto-tag reports older than 90 days for archival',
      conditions: [
        { field: 'classification', operator: 'equals', value: 'report' },
        { field: 'age_days', operator: 'greater_than', value: '90' }
      ],
      actions: [
        { type: 'tag', params: { tag: 'archive-ready' } }
      ],
      is_active: false,
      trigger_count: 47,
      created_at: '2024-01-05T11:00:00Z'
    }
  ])

  const [showCreateModal, setShowCreateModal] = useState(false)
  const [newWorkflow, setNewWorkflow] = useState({
    name: '',
    description: '',
    conditionField: 'classification',
    conditionOperator: 'equals',
    conditionValue: '',
    actionType: 'tag',
    actionParam: ''
  })

  const toggleWorkflow = (id: string) => {
    setWorkflows(prev => prev.map(w =>
      w.id === id ? { ...w, is_active: !w.is_active } : w
    ))
  }

  const deleteWorkflow = (id: string) => {
    setWorkflows(prev => prev.filter(w => w.id !== id))
  }

  const createWorkflow = () => {
    const workflow: WorkflowRule = {
      id: Math.random().toString(36).substring(7),
      name: newWorkflow.name,
      description: newWorkflow.description,
      conditions: [{
        field: newWorkflow.conditionField,
        operator: newWorkflow.conditionOperator,
        value: newWorkflow.conditionValue
      }],
      actions: [{
        type: newWorkflow.actionType,
        params: newWorkflow.actionType === 'tag'
          ? { tag: newWorkflow.actionParam }
          : { email: newWorkflow.actionParam, message: 'Automated notification' }
      }],
      is_active: true,
      trigger_count: 0,
      created_at: new Date().toISOString()
    }

    setWorkflows(prev => [workflow, ...prev])
    setShowCreateModal(false)
    setNewWorkflow({
      name: '',
      description: '',
      conditionField: 'classification',
      conditionOperator: 'equals',
      conditionValue: '',
      actionType: 'tag',
      actionParam: ''
    })
  }

  const actionIcons: Record<string, any> = {
    tag: Tag,
    notify: Mail,
    move: FolderOpen
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Workflow Automation</h1>
          <p className="text-slate-600">
            Create rules to automatically process documents based on their content.
          </p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="inline-flex items-center justify-center gap-2 bg-blue-600 text-white px-4 py-2.5 rounded-lg font-medium hover:bg-blue-700 transition-colors"
        >
          <Plus className="w-4 h-4" />
          Create Workflow
        </button>
      </div>

      {/* Info banner */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-100 rounded-xl p-6">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center flex-shrink-0">
            <Zap className="w-6 h-6 text-purple-600" />
          </div>
          <div>
            <h3 className="font-semibold text-slate-900 mb-1">Automate Your Document Workflow</h3>
            <p className="text-slate-600 text-sm">
              Create rules that automatically tag, route, and notify based on document classification and extracted entities.
              Workflows are evaluated when documents are uploaded and processed.
            </p>
          </div>
        </div>
      </div>

      {/* Workflows list */}
      <div className="space-y-4">
        {workflows.map((workflow) => (
          <div
            key={workflow.id}
            className={`bg-white border rounded-xl overflow-hidden transition-all ${
              workflow.is_active ? 'border-slate-200' : 'border-slate-200 opacity-60'
            }`}
          >
            <div className="p-5">
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="font-semibold text-slate-900">{workflow.name}</h3>
                    {workflow.is_active ? (
                      <span className="flex items-center gap-1 text-xs font-medium text-green-600 bg-green-50 px-2 py-1 rounded-full">
                        <CheckCircle className="w-3 h-3" />
                        Active
                      </span>
                    ) : (
                      <span className="flex items-center gap-1 text-xs font-medium text-slate-500 bg-slate-100 px-2 py-1 rounded-full">
                        <Pause className="w-3 h-3" />
                        Paused
                      </span>
                    )}
                  </div>
                  <p className="text-slate-600 text-sm mb-4">{workflow.description}</p>

                  {/* Conditions & Actions */}
                  <div className="flex flex-wrap gap-4 text-sm">
                    <div>
                      <span className="text-slate-500 mr-2">When:</span>
                      {workflow.conditions.map((c, idx) => (
                        <span key={idx} className="bg-blue-50 text-blue-700 px-2 py-1 rounded">
                          {c.field} {c.operator} "{c.value}"
                        </span>
                      ))}
                    </div>
                    <div className="flex items-center gap-2">
                      <ChevronRight className="w-4 h-4 text-slate-400" />
                      <span className="text-slate-500">Then:</span>
                      {workflow.actions.map((a, idx) => {
                        const Icon = actionIcons[a.type] || Zap
                        return (
                          <span key={idx} className="flex items-center gap-1 bg-purple-50 text-purple-700 px-2 py-1 rounded">
                            <Icon className="w-3 h-3" />
                            {a.type === 'tag' ? `Tag: ${a.params.tag}` : `Notify: ${a.params.email}`}
                          </span>
                        )
                      })}
                    </div>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => toggleWorkflow(workflow.id)}
                    className={`p-2 rounded-lg transition-colors ${
                      workflow.is_active
                        ? 'hover:bg-yellow-50 text-yellow-600'
                        : 'hover:bg-green-50 text-green-600'
                    }`}
                    title={workflow.is_active ? 'Pause workflow' : 'Activate workflow'}
                  >
                    {workflow.is_active ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                  </button>
                  <button
                    className="p-2 hover:bg-slate-100 rounded-lg text-slate-500"
                    title="Edit workflow"
                  >
                    <Edit className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => deleteWorkflow(workflow.id)}
                    className="p-2 hover:bg-red-50 rounded-lg text-slate-500 hover:text-red-600"
                    title="Delete workflow"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>

            {/* Stats footer */}
            <div className="px-5 py-3 bg-slate-50 border-t border-slate-100 flex items-center justify-between text-sm text-slate-500">
              <span>Created {new Date(workflow.created_at).toLocaleDateString()}</span>
              <span className="font-medium">{workflow.trigger_count} times triggered</span>
            </div>
          </div>
        ))}

        {workflows.length === 0 && (
          <div className="text-center py-12 bg-white rounded-xl border border-slate-200">
            <Workflow className="w-12 h-12 text-slate-300 mx-auto mb-4" />
            <p className="text-slate-600">No workflows created yet</p>
            <p className="text-slate-500 text-sm mt-1">Create your first workflow to automate document processing.</p>
          </div>
        )}
      </div>

      {/* Create Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full">
            <div className="p-6 border-b border-slate-200">
              <h2 className="text-xl font-bold text-slate-900">Create Workflow</h2>
              <p className="text-slate-600 text-sm mt-1">Define conditions and actions for automatic document processing.</p>
            </div>

            <div className="p-6 space-y-5">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Workflow Name</label>
                <input
                  type="text"
                  value={newWorkflow.name}
                  onChange={(e) => setNewWorkflow({ ...newWorkflow, name: e.target.value })}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                  placeholder="e.g., High-Value Invoice Alert"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Description</label>
                <input
                  type="text"
                  value={newWorkflow.description}
                  onChange={(e) => setNewWorkflow({ ...newWorkflow, description: e.target.value })}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                  placeholder="e.g., Notify finance team for invoices over $10k"
                />
              </div>

              <div className="bg-blue-50 p-4 rounded-lg">
                <label className="block text-sm font-medium text-blue-900 mb-3">When document matches:</label>
                <div className="grid grid-cols-3 gap-2">
                  <select
                    value={newWorkflow.conditionField}
                    onChange={(e) => setNewWorkflow({ ...newWorkflow, conditionField: e.target.value })}
                    className="px-3 py-2 border border-blue-200 rounded-lg bg-white"
                  >
                    <option value="classification">Type</option>
                    <option value="entity_money">Amount</option>
                    <option value="entity_org">Organization</option>
                  </select>
                  <select
                    value={newWorkflow.conditionOperator}
                    onChange={(e) => setNewWorkflow({ ...newWorkflow, conditionOperator: e.target.value })}
                    className="px-3 py-2 border border-blue-200 rounded-lg bg-white"
                  >
                    <option value="equals">equals</option>
                    <option value="contains">contains</option>
                    <option value="greater_than">greater than</option>
                  </select>
                  <input
                    type="text"
                    value={newWorkflow.conditionValue}
                    onChange={(e) => setNewWorkflow({ ...newWorkflow, conditionValue: e.target.value })}
                    className="px-3 py-2 border border-blue-200 rounded-lg"
                    placeholder="invoice"
                  />
                </div>
              </div>

              <div className="bg-purple-50 p-4 rounded-lg">
                <label className="block text-sm font-medium text-purple-900 mb-3">Then perform action:</label>
                <div className="grid grid-cols-2 gap-2">
                  <select
                    value={newWorkflow.actionType}
                    onChange={(e) => setNewWorkflow({ ...newWorkflow, actionType: e.target.value })}
                    className="px-3 py-2 border border-purple-200 rounded-lg bg-white"
                  >
                    <option value="tag">Add Tag</option>
                    <option value="notify">Send Notification</option>
                  </select>
                  <input
                    type="text"
                    value={newWorkflow.actionParam}
                    onChange={(e) => setNewWorkflow({ ...newWorkflow, actionParam: e.target.value })}
                    className="px-3 py-2 border border-purple-200 rounded-lg"
                    placeholder={newWorkflow.actionType === 'tag' ? 'tag-name' : 'email@company.com'}
                  />
                </div>
              </div>
            </div>

            <div className="p-6 border-t border-slate-200 flex gap-3">
              <button
                onClick={() => setShowCreateModal(false)}
                className="flex-1 px-4 py-2.5 border border-slate-300 rounded-lg font-medium hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                onClick={createWorkflow}
                disabled={!newWorkflow.name || !newWorkflow.conditionValue || !newWorkflow.actionParam}
                className="flex-1 bg-blue-600 text-white px-4 py-2.5 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Create Workflow
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
