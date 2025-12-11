'use client'

import { useState } from 'react'
import {
  Search,
  FileText,
  Filter,
  Calendar,
  Tag,
  ChevronDown,
  X,
  Clock,
  Sparkles
} from 'lucide-react'

interface SearchResult {
  id: string
  filename: string
  classification: string
  snippet: string
  score: number
  created_at: string
  entities: Array<{ type: string; value: string }>
}

export default function SearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<SearchResult[]>([])
  const [loading, setLoading] = useState(false)
  const [searched, setSearched] = useState(false)
  const [filters, setFilters] = useState({
    classification: '',
    dateFrom: '',
    dateTo: '',
    entityType: ''
  })
  const [showFilters, setShowFilters] = useState(false)

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()

    setLoading(true)
    setSearched(true)

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const searchParams = new URLSearchParams({ q: query.trim() })
      const response = await fetch(`${apiUrl}/api/search/demo?${searchParams}`)

      if (response.ok) {
        const data = await response.json()
        // Map API response to frontend format
        let searchResults: SearchResult[] = data.results.map((r: {
          id: string
          filename: string
          classification: string
          snippet: string
          confidence_score: number
          created_at: string
          entities: Array<{ type: string; value: string }>
        }) => ({
          id: r.id,
          filename: r.filename,
          classification: r.classification,
          snippet: r.snippet,
          score: r.confidence_score,
          created_at: r.created_at,
          entities: r.entities || []
        }))

        // Apply client-side filters
        if (filters.classification) {
          searchResults = searchResults.filter(r => r.classification === filters.classification)
        }

        setResults(searchResults)
      } else {
        console.error('Search failed')
        setResults([])
      }
    } catch (error) {
      console.error('Search error:', error)
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  const clearFilters = () => {
    setFilters({
      classification: '',
      dateFrom: '',
      dateTo: '',
      entityType: ''
    })
  }

  const classificationColors: Record<string, string> = {
    invoice: 'bg-blue-100 text-blue-700',
    contract: 'bg-green-100 text-green-700',
    report: 'bg-purple-100 text-purple-700',
    letter: 'bg-yellow-100 text-yellow-700',
    other: 'bg-slate-100 text-slate-700'
  }

  const suggestions = [
    'invoices from last month',
    'contracts with Acme Corp',
    'reports containing revenue',
    'documents over $10,000'
  ]

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Search Documents</h1>
        <p className="text-slate-600">
          Search across all your documents using natural language.
        </p>
      </div>

      {/* Search form */}
      <form onSubmit={handleSearch} className="space-y-4">
        <div className="relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search documents by content, filename, or entities..."
            className="w-full pl-12 pr-4 py-4 text-lg border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
          />
          <button
            type="submit"
            disabled={loading}
            className="absolute right-2 top-1/2 -translate-y-1/2 bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-50"
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>

        {/* Filter toggle */}
        <div className="flex items-center justify-between">
          <button
            type="button"
            onClick={() => setShowFilters(!showFilters)}
            className="flex items-center gap-2 text-slate-600 hover:text-slate-900"
          >
            <Filter className="w-4 h-4" />
            <span className="text-sm font-medium">
              {showFilters ? 'Hide Filters' : 'Show Filters'}
            </span>
            <ChevronDown className={`w-4 h-4 transition-transform ${showFilters ? 'rotate-180' : ''}`} />
          </button>
          {Object.values(filters).some(v => v) && (
            <button
              type="button"
              onClick={clearFilters}
              className="text-sm text-slate-500 hover:text-slate-700 flex items-center gap-1"
            >
              <X className="w-3 h-3" />
              Clear filters
            </button>
          )}
        </div>

        {/* Filters */}
        {showFilters && (
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 p-4 bg-slate-50 rounded-xl">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Document Type
              </label>
              <select
                value={filters.classification}
                onChange={(e) => setFilters({ ...filters, classification: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
              >
                <option value="">All Types</option>
                <option value="invoice">Invoice</option>
                <option value="contract">Contract</option>
                <option value="report">Report</option>
                <option value="letter">Letter</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                From Date
              </label>
              <input
                type="date"
                value={filters.dateFrom}
                onChange={(e) => setFilters({ ...filters, dateFrom: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                To Date
              </label>
              <input
                type="date"
                value={filters.dateTo}
                onChange={(e) => setFilters({ ...filters, dateTo: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Entity Type
              </label>
              <select
                value={filters.entityType}
                onChange={(e) => setFilters({ ...filters, entityType: e.target.value })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
              >
                <option value="">All Entities</option>
                <option value="PERSON">Person</option>
                <option value="ORGANIZATION">Organization</option>
                <option value="MONEY">Money</option>
                <option value="DATE">Date</option>
              </select>
            </div>
          </div>
        )}
      </form>

      {/* Suggestions (when no search) */}
      {!searched && (
        <div className="bg-blue-50 border border-blue-100 rounded-xl p-6">
          <div className="flex items-center gap-2 text-blue-700 mb-3">
            <Sparkles className="w-5 h-5" />
            <span className="font-medium">Try searching for:</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {suggestions.map((suggestion, idx) => (
              <button
                key={idx}
                onClick={() => {
                  setQuery(suggestion)
                }}
                className="bg-white text-blue-700 px-3 py-1.5 rounded-lg text-sm hover:bg-blue-100 transition-colors border border-blue-200"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Results */}
      {searched && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <p className="text-slate-600">
              {loading ? 'Searching...' : `Found ${results.length} results for "${query}"`}
            </p>
          </div>

          {results.length > 0 ? (
            <div className="space-y-4">
              {results.map((result) => (
                <div
                  key={result.id}
                  className="bg-white border border-slate-200 rounded-xl p-5 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                      <FileText className="w-6 h-6 text-blue-600" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="font-semibold text-slate-900 truncate">
                          {result.filename}
                        </h3>
                        <span className={`px-2 py-0.5 rounded-full text-xs font-medium capitalize ${classificationColors[result.classification]}`}>
                          {result.classification}
                        </span>
                      </div>
                      <p
                        className="text-slate-600 text-sm mb-3"
                        dangerouslySetInnerHTML={{ __html: result.snippet }}
                      />
                      <div className="flex items-center gap-4 text-sm text-slate-500">
                        <span className="flex items-center gap-1">
                          <Clock className="w-4 h-4" />
                          {new Date(result.created_at).toLocaleDateString()}
                        </span>
                        <span className="flex items-center gap-1">
                          <Tag className="w-4 h-4" />
                          {result.entities.map(e => e.value).join(', ')}
                        </span>
                        <span className="text-blue-600">
                          {(result.score * 100).toFixed(0)}% match
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : !loading && (
            <div className="text-center py-12 bg-slate-50 rounded-xl">
              <Search className="w-12 h-12 text-slate-300 mx-auto mb-4" />
              <p className="text-slate-600">No documents found matching your search.</p>
              <p className="text-slate-500 text-sm mt-1">Try different keywords or adjust your filters.</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
