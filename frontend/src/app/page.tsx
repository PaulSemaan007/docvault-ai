'use client'

import { useState } from 'react'
import {
  FileText,
  Upload,
  Search,
  Settings,
  BarChart3,
  Shield,
  Workflow,
  Brain,
  ArrowRight,
  CheckCircle,
  Users,
  Lock
} from 'lucide-react'
import Link from 'next/link'

export default function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  const features = [
    {
      icon: Brain,
      title: 'AI-Powered Classification',
      description: 'Automatically categorize documents as invoices, contracts, reports, and more using machine learning.'
    },
    {
      icon: Search,
      title: 'Smart Entity Extraction',
      description: 'Extract names, dates, amounts, and other key data from your documents automatically.'
    },
    {
      icon: Workflow,
      title: 'Workflow Automation',
      description: 'Create rules to automatically tag, route, and process documents based on their content.'
    },
    {
      icon: Shield,
      title: 'Enterprise Security',
      description: 'Role-based access control, audit logging, and secure cloud storage protect your data.'
    },
    {
      icon: FileText,
      title: 'Full-Text Search',
      description: 'Search across all your documents instantly with powerful filtering options.'
    },
    {
      icon: BarChart3,
      title: 'Analytics Dashboard',
      description: 'Get insights into your document processing with real-time statistics and reports.'
    }
  ]

  const stats = [
    { label: 'Document Types Supported', value: '10+' },
    { label: 'Entity Types Extracted', value: '15+' },
    { label: 'Classification Accuracy', value: '94%' },
    { label: 'Processing Time', value: '<5s' }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Navigation */}
      <nav className="bg-white/80 backdrop-blur-md border-b border-slate-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-700 rounded-xl flex items-center justify-center">
                <FileText className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
                DocVault AI
              </span>
            </div>
            <div className="flex items-center gap-4">
              <Link
                href="/login"
                className="text-slate-600 hover:text-slate-900 font-medium transition-colors"
              >
                Login
              </Link>
              <Link
                href="/register"
                className="bg-blue-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-blue-100 text-blue-700 px-4 py-2 rounded-full text-sm font-medium mb-8">
            <Brain className="w-4 h-4" />
            Powered by Machine Learning
          </div>
          <h1 className="text-5xl md:text-6xl font-bold text-slate-900 mb-6 leading-tight">
            Intelligent Document
            <br />
            <span className="bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
              Management System
            </span>
          </h1>
          <p className="text-xl text-slate-600 mb-10 max-w-3xl mx-auto">
            Transform how you handle documents with AI-powered classification,
            smart data extraction, and automated workflows. Built for enterprise security.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/register"
              className="inline-flex items-center justify-center gap-2 bg-blue-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-blue-700 transition-all hover:scale-105 shadow-lg shadow-blue-500/25"
            >
              Start Free Trial
              <ArrowRight className="w-5 h-5" />
            </Link>
            <Link
              href="/demo"
              className="inline-flex items-center justify-center gap-2 bg-white text-slate-700 px-8 py-4 rounded-xl font-semibold text-lg hover:bg-slate-50 transition-all border border-slate-200"
            >
              View Demo
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12 bg-white border-y border-slate-200">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-4xl font-bold text-blue-600 mb-2">{stat.value}</div>
                <div className="text-slate-600">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-4">
              Everything you need for document management
            </h2>
            <p className="text-lg text-slate-600 max-w-2xl mx-auto">
              Powerful features designed to streamline your document workflows and enhance productivity.
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="bg-white p-8 rounded-2xl border border-slate-200 hover:border-blue-300 hover:shadow-lg transition-all group"
              >
                <div className="w-14 h-14 bg-blue-100 rounded-xl flex items-center justify-center mb-6 group-hover:bg-blue-600 transition-colors">
                  <feature.icon className="w-7 h-7 text-blue-600 group-hover:text-white transition-colors" />
                </div>
                <h3 className="text-xl font-semibold text-slate-900 mb-3">{feature.title}</h3>
                <p className="text-slate-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 px-4 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-4">
              How DocVault AI Works
            </h2>
            <p className="text-lg text-slate-600">
              Three simple steps to intelligent document management
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                step: '01',
                title: 'Upload Documents',
                description: 'Drop any document - PDFs, images, or scans. Our system handles them all.'
              },
              {
                step: '02',
                title: 'AI Processing',
                description: 'Machine learning classifies your document and extracts key information automatically.'
              },
              {
                step: '03',
                title: 'Automate & Search',
                description: 'Set up workflows, search instantly, and access your data from anywhere.'
              }
            ].map((item, index) => (
              <div key={index} className="relative">
                <div className="text-8xl font-bold text-blue-100 absolute -top-4 -left-2">
                  {item.step}
                </div>
                <div className="relative z-10 pt-12">
                  <h3 className="text-xl font-semibold text-slate-900 mb-3">{item.title}</h3>
                  <p className="text-slate-600">{item.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="bg-gradient-to-br from-blue-600 to-blue-800 rounded-3xl p-12 text-center text-white">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Ready to transform your document workflow?
            </h2>
            <p className="text-blue-100 text-lg mb-8 max-w-2xl mx-auto">
              Join thousands of organizations using DocVault AI to manage documents smarter.
            </p>
            <Link
              href="/register"
              className="inline-flex items-center justify-center gap-2 bg-white text-blue-600 px-8 py-4 rounded-xl font-semibold text-lg hover:bg-blue-50 transition-all"
            >
              Get Started Free
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900 text-slate-400 py-12 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <FileText className="w-5 h-5 text-white" />
              </div>
              <span className="font-semibold text-white">DocVault AI</span>
            </div>
            <div className="text-sm">
              Built for the Laserfiche Software Engineer Internship Application
            </div>
            <div className="flex gap-6 text-sm">
              <Link href="/privacy" className="hover:text-white transition-colors">Privacy</Link>
              <Link href="/terms" className="hover:text-white transition-colors">Terms</Link>
              <Link href="/contact" className="hover:text-white transition-colors">Contact</Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
