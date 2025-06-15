'use client'

import { useState } from 'react'
import axios from 'axios'

export default function Home() {
  const [file, setFile] = useState<File | null>(null)
  const [atsScore, setAtsScore] = useState<number | null>(null)
  const [suggestions, setSuggestions] = useState<string[]>([])
  const [loading, setLoading] = useState(false)

  const handleUpload = async () => {
    if (!file) return
    setLoading(true)
    setSuggestions([])
    setAtsScore(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post('http://localhost:8000/analyze_resume/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      const scoreRaw = response.data.ats_score
      const normalizedScore = Math.round(scoreRaw * 100)

      setAtsScore(normalizedScore)
      setSuggestions(response.data.suggestions)
    } catch (error) {
      console.error('Error:', error)
      alert('Something went wrong. Please check the backend.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gray-100">
      <div className="bg-white p-6 rounded-xl shadow-md w-full max-w-2xl">
        <h1 className="text-3xl font-bold mb-6 text-center">ScannMyCV - Resume Analyzer</h1>

        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="mb-4 w-full"
        />

        <button
          onClick={handleUpload}
          disabled={loading || !file}
          className="bg-blue-600 text-white font-semibold py-2 px-4 rounded hover:bg-blue-700 disabled:bg-blue-300 w-full"
        >
          {loading ? 'Analyzing...' : 'Analyze Resume'}
        </button>

        {atsScore !== null && (
          <div className="mt-6">
            <h2 className="text-xl font-bold mb-2">ATS Score</h2>
            <div className="relative pt-1">
              <div className="flex mb-2 items-center justify-between">
                <span className="text-sm font-semibold inline-block text-red-600">
                  {atsScore}%
                </span>
              </div>
              <div className="overflow-hidden h-4 mb-4 text-xs flex rounded bg-red-200">
                <div
                  style={{ width: `${atsScore}%` }}
                  className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-red-600"
                ></div>
              </div>
            </div>
          </div>
        )}

        {suggestions.length > 0 && (
          <div className="mt-6">
            <h2 className="text-xl font-bold mb-2">Summary</h2>
            <h3 className="text-lg font-semibold mb-1">Suggestions</h3>
            <ul className="list-disc pl-5 space-y-1">
              {suggestions.map((s, idx) => (
                <li key={idx}>{s}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </main>
  )
}
