'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import {
  FileText,
  Search,
  Filter,
  Download,
  Trash2,
  Eye,
  MoreVertical,
  ChevronDown,
  Calendar,
  Tag,
  Clock,
  CheckCircle
} from 'lucide-react'

interface Document {
  id: string
  filename: string
  classification: string
  confidence_score: number
  file_size: number
  mime_type: string
  status: string
  tags: string[]
  created_at: string
  entities: Array<{ type: string; value: string }>
}

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<Document[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [filterClassification, setFilterClassification] = useState('')
  const [selectedDocument, setSelectedDocument] = useState<Document | null>(null)

  useEffect(() => {
    fetchDocuments()
  }, [])

  const fetchDocuments = async () => {
    // Mock data for demo
    const mockDocuments: Document[] = [
      {
        id: '1',
        filename: 'Q4_Financial_Report_2024.pdf',
        classification: 'report',
        confidence_score: 0.94,
        file_size: 2456789,
        mime_type: 'application/pdf',
        status: 'processed',
        tags: ['quarterly', 'finance'],
        created_at: '2024-01-15T10:30:00Z',
        entities: [
          { type: 'DATE', value: '2024-01-15' },
          { type: 'MONEY', value: '$1,250,000' },
          { type: 'ORGANIZATION', value: 'Acme Corporation' }
        ]
      },
      {
        id: '2',
        filename: 'Invoice_INV-2024-0042.pdf',
        classification: 'invoice',
        confidence_score: 0.97,
        file_size: 156789,
        mime_type: 'application/pdf',
        status: 'processed',
        tags: ['vendor', 'payable'],
        created_at: '2024-01-14T15:20:00Z',
        entities: [
          { type: 'MONEY', value: '$5,250.00' },
          { type: 'DATE', value: '2024-02-15' },
          { type: 'REFERENCE_NUMBER', value: 'INV-2024-0042' }
        ]
      },
      {
        id: '3',
        filename: 'Employment_Agreement_JSmith.docx',
        classification: 'contract',
        confidence_score: 0.91,
        file_size: 89456,
        mime_type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        status: 'processed',
        tags: ['hr', 'legal'],
        created_at: '2024-01-13T09:15:00Z',
        entities: [
          { type: 'PERSON', value: 'John Smith' },
          { type: 'DATE', value: '2024-01-01' },
          { type: 'MONEY', value: '$85,000/year' }
        ]
      },
      {
        id: '4',
        filename: 'Vendor_Service_Agreement.pdf',
        classification: 'contract',
        confidence_score: 0.89,
        file_size: 345678,
        mime_type: 'application/pdf',
        status: 'processed',
        tags: ['vendor', 'services'],
        created_at: '2024-01-12T14:45:00Z',
        entities: [
          { type: 'ORGANIZATION', value: 'TechServices Inc' },
          { type: 'DATE', value: '2024-12-31' },
          { type: 'MONEY', value: '$24,000' }
        ]
      },
      {
        id: '5',
        filename: 'Meeting_Notes_Jan10.txt',
        classification: 'other',
        confidence_score: 0.72,
        file_size: 12345,
        mime_type: 'text/plain',
        status: 'processed',
        tags: ['meeting', 'internal'],
        created_at: '2024-01-10T16:30:00Z',
        entities: [
          { type: 'DATE', value: '2024-01-10' },
          { type: 'PERSON', value: 'Sarah Johnson' }
        ]
      }
    ]

    setDocuments(mockDocuments)
    setLoading(false)
  }

  const filteredDocuments = documents.filter(doc => {
    const matchesSearch = doc.filename.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesFilter = !filterClassification || doc.classification === filterClassification
    return matchesSearch && matchesFilter
  })

  const classifications = [...new Set(documents.map(d => d.classification))]

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / 1024 / 1024).toFixed(1)} MB`
  }

  const classificationColors: Record<string, string> = {
    invoice: 'bg-blue-100 text-blue-700',
    contract: 'bg-green-100 text-green-700',
    report: 'bg-purple-100 text-purple-700',
    letter: 'bg-yellow-100 text-yellow-700',
    other: 'bg-slate-100 text-slate-700'
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Documents</h1>
          <p className="text-slate-600">Manage and view all your uploaded documents.</p>
        </div>
        <Link
          href="/dashboard/upload"
          className="inline-flex items-center justify-center gap-2 bg-blue-600 text-white px-4 py-2.5 rounded-lg font-medium hover:bg-blue-700 transition-colors"
        >
          Upload New
        </Link>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
          <input
            type="text"
            placeholder="Search documents..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
          />
        </div>
        <div className="relative">
          <Filter className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
          <select
            value={filterClassification}
            onChange={(e) => setFilterClassification(e.target.value)}
            className="pl-10 pr-8 py-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none appearance-none bg-white min-w-[160px]"
          >
            <option value="">All Types</option>
            {classifications.map(c => (
              <option key={c} value={c} className="capitalize">{c}</option>
            ))}
          </select>
          <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none" />
        </div>
      </div>

      {/* Documents table */}
      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-slate-50 border-b border-slate-200">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                  Document
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                  Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                  Size
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                  Uploaded
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-slate-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {filteredDocuments.map((doc) => (
                <tr key={doc.id} className="hover:bg-slate-50 transition-colors">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                        <FileText className="w-5 h-5 text-blue-600" />
                      </div>
                      <div className="min-w-0">
                        <p className="font-medium text-slate-900 truncate max-w-xs">{doc.filename}</p>
                        <div className="flex gap-1 mt-1">
                          {doc.tags.slice(0, 2).map(tag => (
                            <span key={tag} className="text-xs bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded">
                              {tag}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium capitalize ${classificationColors[doc.classification] || classificationColors.other}`}>
                      {doc.classification}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-slate-600">
                    {formatFileSize(doc.file_size)}
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-1.5 text-sm text-slate-600">
                      <Clock className="w-4 h-4" />
                      {new Date(doc.created_at).toLocaleDateString()}
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-1.5 text-green-600">
                      <CheckCircle className="w-4 h-4" />
                      <span className="text-sm font-medium">Processed</span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center justify-end gap-2">
                      <button
                        onClick={() => setSelectedDocument(doc)}
                        className="p-2 hover:bg-slate-100 rounded-lg text-slate-600 hover:text-slate-900"
                        title="View details"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                      <button
                        className="p-2 hover:bg-slate-100 rounded-lg text-slate-600 hover:text-slate-900"
                        title="Download"
                      >
                        <Download className="w-4 h-4" />
                      </button>
                      <button
                        className="p-2 hover:bg-red-50 rounded-lg text-slate-600 hover:text-red-600"
                        title="Delete"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {filteredDocuments.length === 0 && (
          <div className="text-center py-12">
            <FileText className="w-12 h-12 text-slate-300 mx-auto mb-4" />
            <p className="text-slate-600">No documents found</p>
          </div>
        )}
      </div>

      {/* Document detail modal */}
      {selectedDocument && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-slate-200 flex items-start justify-between">
              <div>
                <h2 className="text-xl font-bold text-slate-900">{selectedDocument.filename}</h2>
                <p className="text-slate-600 text-sm mt-1">
                  Uploaded {new Date(selectedDocument.created_at).toLocaleString()}
                </p>
              </div>
              <button
                onClick={() => setSelectedDocument(null)}
                className="p-2 hover:bg-slate-100 rounded-lg"
              >
                <span className="sr-only">Close</span>
                ×
              </button>
            </div>
            <div className="p-6 space-y-6">
              {/* Classification */}
              <div>
                <h3 className="text-sm font-medium text-slate-500 mb-2">Classification</h3>
                <div className="flex items-center gap-3">
                  <span className={`inline-flex items-center px-3 py-1.5 rounded-full text-sm font-medium capitalize ${classificationColors[selectedDocument.classification]}`}>
                    {selectedDocument.classification}
                  </span>
                  <span className="text-sm text-slate-600">
                    {(selectedDocument.confidence_score * 100).toFixed(0)}% confidence
                  </span>
                </div>
              </div>

              {/* Entities */}
              <div>
                <h3 className="text-sm font-medium text-slate-500 mb-2">Extracted Entities</h3>
                <div className="flex flex-wrap gap-2">
                  {selectedDocument.entities.map((entity, idx) => (
                    <span
                      key={idx}
                      className="inline-flex items-center gap-2 bg-slate-100 text-slate-700 px-3 py-1.5 rounded-lg text-sm"
                    >
                      <span className="text-xs font-medium text-slate-500">{entity.type}</span>
                      {entity.value}
                    </span>
                  ))}
                </div>
              </div>

              {/* Tags */}
              <div>
                <h3 className="text-sm font-medium text-slate-500 mb-2">Tags</h3>
                <div className="flex flex-wrap gap-2">
                  {selectedDocument.tags.map(tag => (
                    <span key={tag} className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>

              {/* Actions */}
              <div className="flex gap-3 pt-4 border-t border-slate-200">
                <button className="flex-1 bg-blue-600 text-white py-2.5 rounded-lg font-medium hover:bg-blue-700 transition-colors flex items-center justify-center gap-2">
                  <Download className="w-4 h-4" />
                  Download
                </button>
                <button className="px-4 py-2.5 border border-slate-300 rounded-lg font-medium hover:bg-slate-50 transition-colors flex items-center gap-2 text-red-600 border-red-200 hover:bg-red-50">
                  <Trash2 className="w-4 h-4" />
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
