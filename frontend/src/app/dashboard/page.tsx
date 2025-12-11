'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import {
  FileText,
  Upload,
  Search,
  TrendingUp,
  Clock,
  CheckCircle,
  AlertCircle,
  ArrowUpRight,
  BarChart3,
  PieChart,
  Activity
} from 'lucide-react'

export default function DashboardPage() {
  const [stats, setStats] = useState({
    totalDocuments: 0,
    documentsToday: 0,
    documentsThisWeek: 0,
    storageUsed: 0
  })

  const [recentDocuments, setRecentDocuments] = useState<any[]>([])
  const [classificationBreakdown, setClassificationBreakdown] = useState<Record<string, number>>({})

  useEffect(() => {
    // Fetch dashboard stats
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

      // Fetch stats and documents in parallel
      const [statsRes, docsRes] = await Promise.all([
        fetch(`${apiUrl}/api/documents/demo-stats`),
        fetch(`${apiUrl}/api/documents/demo-list`)
      ])

      if (statsRes.ok) {
        const statsData = await statsRes.json()
        setStats({
          totalDocuments: statsData.total_documents,
          documentsToday: statsData.recent_count,
          documentsThisWeek: statsData.total_documents,
          storageUsed: 0
        })
        setClassificationBreakdown(statsData.classifications || {})
      }

      if (docsRes.ok) {
        const docsData = await docsRes.json()
        // Get the 5 most recent documents
        const recent = docsData.documents.slice(0, 5).map((doc: {
          id: string
          filename: string
          classification: string
          created_at: string
          status: string
        }) => ({
          id: doc.id,
          filename: doc.filename,
          classification: doc.classification,
          created_at: doc.created_at,
          status: doc.status
        }))
        setRecentDocuments(recent)
      }
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
      // Keep defaults on error
    }
  }

  const statCards = [
    {
      title: 'Total Documents',
      value: stats.totalDocuments,
      icon: FileText,
      color: 'blue',
      change: '+12%'
    },
    {
      title: 'Uploaded Today',
      value: stats.documentsToday,
      icon: Upload,
      color: 'green',
      change: '+5'
    },
    {
      title: 'This Week',
      value: stats.documentsThisWeek,
      icon: TrendingUp,
      color: 'purple',
      change: '+23%'
    },
    {
      title: 'Storage Used',
      value: `${stats.storageUsed} MB`,
      icon: BarChart3,
      color: 'orange',
      change: '15.6%'
    }
  ]

  const colorMap: Record<string, string> = {
    blue: 'bg-blue-100 text-blue-600',
    green: 'bg-green-100 text-green-600',
    purple: 'bg-purple-100 text-purple-600',
    orange: 'bg-orange-100 text-orange-600'
  }

  const classificationColors: Record<string, string> = {
    invoice: 'bg-blue-500',
    contract: 'bg-green-500',
    report: 'bg-purple-500',
    letter: 'bg-yellow-500',
    other: 'bg-slate-400'
  }

  const totalDocs = Object.values(classificationBreakdown).reduce((a, b) => a + b, 0)

  return (
    <div className="space-y-8">
      {/* Page header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
          <p className="text-slate-600">Welcome back! Here's your document overview.</p>
        </div>
        <Link
          href="/dashboard/upload"
          className="inline-flex items-center justify-center gap-2 bg-blue-600 text-white px-4 py-2.5 rounded-lg font-medium hover:bg-blue-700 transition-colors"
        >
          <Upload className="w-4 h-4" />
          Upload Document
        </Link>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((stat, index) => (
          <div
            key={index}
            className="bg-white p-6 rounded-xl border border-slate-200 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between">
              <div className={`p-3 rounded-lg ${colorMap[stat.color]}`}>
                <stat.icon className="w-5 h-5" />
              </div>
              <span className="text-sm font-medium text-green-600 bg-green-50 px-2 py-1 rounded">
                {stat.change}
              </span>
            </div>
            <div className="mt-4">
              <p className="text-2xl font-bold text-slate-900">{stat.value}</p>
              <p className="text-sm text-slate-600">{stat.title}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Charts and tables */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Classification breakdown */}
        <div className="bg-white p-6 rounded-xl border border-slate-200">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-slate-900">Document Types</h2>
            <PieChart className="w-5 h-5 text-slate-400" />
          </div>
          <div className="space-y-4">
            {Object.entries(classificationBreakdown).map(([type, count]) => (
              <div key={type}>
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm font-medium text-slate-700 capitalize">{type}</span>
                  <span className="text-sm text-slate-500">{count} ({Math.round(count / totalDocs * 100)}%)</span>
                </div>
                <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                  <div
                    className={`h-full ${classificationColors[type] || 'bg-slate-400'} rounded-full transition-all`}
                    style={{ width: `${(count / totalDocs) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent documents */}
        <div className="lg:col-span-2 bg-white rounded-xl border border-slate-200">
          <div className="p-6 border-b border-slate-200 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-slate-900">Recent Documents</h2>
            <Link
              href="/dashboard/documents"
              className="text-sm text-blue-600 hover:text-blue-700 font-medium flex items-center gap-1"
            >
              View all
              <ArrowUpRight className="w-4 h-4" />
            </Link>
          </div>
          <div className="divide-y divide-slate-100">
            {recentDocuments.map((doc) => (
              <div key={doc.id} className="p-4 hover:bg-slate-50 transition-colors">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <FileText className="w-5 h-5 text-blue-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-slate-900 truncate">{doc.filename}</p>
                    <div className="flex items-center gap-3 mt-1">
                      <span className={`text-xs px-2 py-0.5 rounded-full capitalize ${
                        classificationColors[doc.classification]?.replace('bg-', 'bg-opacity-20 text-').replace('500', '700') || 'bg-slate-100 text-slate-600'
                      }`}>
                        {doc.classification}
                      </span>
                      <span className="text-xs text-slate-500 flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {new Date(doc.created_at).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                  <div className="flex items-center gap-1 text-green-600">
                    <CheckCircle className="w-4 h-4" />
                    <span className="text-xs font-medium">Processed</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Quick actions */}
      <div className="bg-gradient-to-br from-blue-500 to-blue-700 rounded-xl p-6 text-white">
        <h2 className="text-lg font-semibold mb-2">Quick Actions</h2>
        <p className="text-blue-100 mb-4">Get started with common tasks</p>
        <div className="flex flex-wrap gap-3">
          <Link
            href="/dashboard/upload"
            className="inline-flex items-center gap-2 bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg font-medium transition-colors"
          >
            <Upload className="w-4 h-4" />
            Upload Document
          </Link>
          <Link
            href="/dashboard/search"
            className="inline-flex items-center gap-2 bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg font-medium transition-colors"
          >
            <Search className="w-4 h-4" />
            Search Documents
          </Link>
          <Link
            href="/dashboard/workflows"
            className="inline-flex items-center gap-2 bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg font-medium transition-colors"
          >
            <Activity className="w-4 h-4" />
            Create Workflow
          </Link>
        </div>
      </div>
    </div>
  )
}
