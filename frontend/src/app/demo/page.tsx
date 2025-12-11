'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Loader2, FileText } from 'lucide-react'

export default function DemoPage() {
  const router = useRouter()
  const [status, setStatus] = useState('Setting up demo account...')

  useEffect(() => {
    setupDemo()
  }, [])

  const setupDemo = async () => {
    try {
      // Create a demo user session
      const demoUser = {
        id: 'demo-user-' + Date.now(),
        email: 'demo@docvault.ai',
        full_name: 'Demo User',
        role: 'admin'
      }

      // Store demo credentials
      localStorage.setItem('token', 'demo-token-' + Date.now())
      localStorage.setItem('user', JSON.stringify(demoUser))

      setStatus('Loading dashboard...')

      // Short delay for UX
      await new Promise(resolve => setTimeout(resolve, 1000))

      // Redirect to dashboard
      router.push('/dashboard')
    } catch (error) {
      setStatus('Error setting up demo. Redirecting...')
      setTimeout(() => router.push('/register'), 2000)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center">
      <div className="text-center">
        <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-700 rounded-2xl flex items-center justify-center mx-auto mb-6">
          <FileText className="w-8 h-8 text-white" />
        </div>
        <div className="flex items-center justify-center gap-3 mb-4">
          <Loader2 className="w-5 h-5 animate-spin text-blue-600" />
          <span className="text-lg text-slate-700">{status}</span>
        </div>
        <p className="text-slate-500 text-sm">
          You'll be signed in as a demo admin user
        </p>
      </div>
    </div>
  )
}
