'use client'

import { useState, useCallback } from 'react'
import {
  Upload,
  FileText,
  X,
  CheckCircle,
  AlertCircle,
  Loader2,
  Brain,
  Tag,
  User,
  Calendar,
  DollarSign
} from 'lucide-react'

interface UploadedFile {
  file: File
  id: string
  status: 'pending' | 'uploading' | 'processing' | 'complete' | 'error'
  progress: number
  result?: {
    classification: string
    confidence: number
    entities: Array<{ type: string; value: string }>
  }
  error?: string
}

export default function UploadPage() {
  const [files, setFiles] = useState<UploadedFile[]>([])
  const [dragActive, setDragActive] = useState(false)

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFiles(Array.from(e.dataTransfer.files))
    }
  }, [])

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFiles(Array.from(e.target.files))
    }
  }

  const handleFiles = async (newFiles: File[]) => {
    // Filter valid files
    const validExtensions = ['.pdf', '.png', '.jpg', '.jpeg', '.doc', '.docx', '.txt']
    const validFiles = newFiles.filter(file => {
      const ext = '.' + file.name.split('.').pop()?.toLowerCase()
      return validExtensions.includes(ext)
    })

    // Add files to state
    const uploadedFiles: UploadedFile[] = validFiles.map(file => ({
      file,
      id: Math.random().toString(36).substring(7),
      status: 'pending',
      progress: 0
    }))

    setFiles(prev => [...prev, ...uploadedFiles])

    // Process each file
    for (const uploadedFile of uploadedFiles) {
      await processFile(uploadedFile)
    }
  }

  const processFile = async (uploadedFile: UploadedFile) => {
    // Update status to uploading
    setFiles(prev => prev.map(f =>
      f.id === uploadedFile.id ? { ...f, status: 'uploading', progress: 30 } : f
    ))

    try {
      // Create FormData for multipart upload
      const formData = new FormData()
      formData.append('file', uploadedFile.file)

      // Call real backend API for AI processing
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/api/documents/demo-upload`, {
        method: 'POST',
        body: formData,
        // Don't set Content-Type header - browser sets it with boundary for FormData
      })

      // Update to processing state
      setFiles(prev => prev.map(f =>
        f.id === uploadedFile.id ? { ...f, status: 'processing', progress: 60 } : f
      ))

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Upload failed' }))
        throw new Error(errorData.detail || 'Upload failed')
      }

      // Parse the AI processing results
      const data = await response.json()

      // Map API response to UI format
      const result = {
        classification: data.classification,
        confidence: data.confidence_score,
        entities: data.entities.map((e: { type: string; value: string }) => ({
          type: e.type,
          value: e.value
        }))
      }

      setFiles(prev => prev.map(f =>
        f.id === uploadedFile.id ? {
          ...f,
          status: 'complete',
          progress: 100,
          result
        } : f
      ))

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to process document'
      setFiles(prev => prev.map(f =>
        f.id === uploadedFile.id ? {
          ...f,
          status: 'error',
          error: errorMessage
        } : f
      ))
    }
  }

  const removeFile = (id: string) => {
    setFiles(prev => prev.filter(f => f.id !== id))
  }

  const entityIcons: Record<string, any> = {
    DATE: Calendar,
    MONEY: DollarSign,
    PERSON: User,
    ORGANIZATION: Tag
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Page header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Upload Documents</h1>
        <p className="text-slate-600">
          Upload documents for AI-powered classification and entity extraction.
        </p>
      </div>

      {/* Upload area */}
      <div
        className={`relative border-2 border-dashed rounded-xl p-12 text-center transition-colors ${
          dragActive
            ? 'border-blue-500 bg-blue-50'
            : 'border-slate-300 hover:border-slate-400'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          type="file"
          multiple
          accept=".pdf,.png,.jpg,.jpeg,.doc,.docx,.txt"
          onChange={handleFileInput}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        />
        <div className="flex flex-col items-center">
          <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
            <Upload className="w-8 h-8 text-blue-600" />
          </div>
          <h3 className="text-lg font-semibold text-slate-900 mb-2">
            Drop files here or click to upload
          </h3>
          <p className="text-slate-500 mb-4">
            Supports PDF, PNG, JPG, DOC, DOCX, TXT (max 10MB)
          </p>
          <button className="bg-blue-600 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-blue-700 transition-colors">
            Select Files
          </button>
        </div>
      </div>

      {/* File list */}
      {files.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-slate-900">Uploaded Files</h2>
          <div className="space-y-3">
            {files.map((file) => (
              <div
                key={file.id}
                className="bg-white border border-slate-200 rounded-xl p-4 transition-all"
              >
                <div className="flex items-start gap-4">
                  {/* File icon */}
                  <div className="w-12 h-12 bg-slate-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <FileText className="w-6 h-6 text-slate-500" />
                  </div>

                  {/* File info */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-1">
                      <p className="font-medium text-slate-900 truncate">{file.file.name}</p>
                      <button
                        onClick={() => removeFile(file.id)}
                        className="p-1 hover:bg-slate-100 rounded"
                      >
                        <X className="w-4 h-4 text-slate-400" />
                      </button>
                    </div>
                    <p className="text-sm text-slate-500 mb-2">
                      {(file.file.size / 1024 / 1024).toFixed(2)} MB
                    </p>

                    {/* Progress bar */}
                    {(file.status === 'uploading' || file.status === 'processing') && (
                      <div className="space-y-2">
                        <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-blue-500 rounded-full transition-all"
                            style={{ width: `${file.progress}%` }}
                          />
                        </div>
                        <div className="flex items-center gap-2 text-sm text-blue-600">
                          <Loader2 className="w-4 h-4 animate-spin" />
                          {file.status === 'uploading' ? 'Uploading...' : 'Processing with AI...'}
                        </div>
                      </div>
                    )}

                    {/* Success result */}
                    {file.status === 'complete' && file.result && (
                      <div className="space-y-3 mt-3 pt-3 border-t border-slate-100">
                        {/* Classification */}
                        <div className="flex items-center gap-3">
                          <div className="flex items-center gap-2 text-green-600">
                            <CheckCircle className="w-4 h-4" />
                            <span className="text-sm font-medium">Processed</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <Brain className="w-4 h-4 text-purple-500" />
                            <span className="text-sm text-slate-600">
                              Classified as{' '}
                              <span className="font-medium text-slate-900 capitalize">
                                {file.result.classification}
                              </span>
                              {' '}({(file.result.confidence * 100).toFixed(0)}% confidence)
                            </span>
                          </div>
                        </div>

                        {/* Entities */}
                        {file.result.entities.length > 0 && (
                          <div className="flex flex-wrap gap-2">
                            {file.result.entities.map((entity, idx) => {
                              const Icon = entityIcons[entity.type] || Tag
                              return (
                                <span
                                  key={idx}
                                  className="inline-flex items-center gap-1.5 bg-slate-100 text-slate-700 px-3 py-1.5 rounded-lg text-sm"
                                >
                                  <Icon className="w-3.5 h-3.5 text-slate-500" />
                                  {entity.value}
                                </span>
                              )
                            })}
                          </div>
                        )}
                      </div>
                    )}

                    {/* Error state */}
                    {file.status === 'error' && (
                      <div className="flex items-center gap-2 text-red-600 mt-2">
                        <AlertCircle className="w-4 h-4" />
                        <span className="text-sm">{file.error}</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Info cards */}
      <div className="grid md:grid-cols-3 gap-4">
        <div className="bg-blue-50 border border-blue-100 rounded-xl p-4">
          <Brain className="w-8 h-8 text-blue-600 mb-2" />
          <h3 className="font-semibold text-slate-900 mb-1">AI Classification</h3>
          <p className="text-sm text-slate-600">
            Documents are automatically categorized using machine learning.
          </p>
        </div>
        <div className="bg-purple-50 border border-purple-100 rounded-xl p-4">
          <Tag className="w-8 h-8 text-purple-600 mb-2" />
          <h3 className="font-semibold text-slate-900 mb-1">Entity Extraction</h3>
          <p className="text-sm text-slate-600">
            Key data like names, dates, and amounts are extracted automatically.
          </p>
        </div>
        <div className="bg-green-50 border border-green-100 rounded-xl p-4">
          <CheckCircle className="w-8 h-8 text-green-600 mb-2" />
          <h3 className="font-semibold text-slate-900 mb-1">Workflow Triggers</h3>
          <p className="text-sm text-slate-600">
            Uploaded documents can trigger automated workflows.
          </p>
        </div>
      </div>
    </div>
  )
}
