import { useState } from 'react'
import { Languages, Loader2, Copy, Check } from 'lucide-react'
import axios from 'axios'

const Translation = () => {
  const [text, setText] = useState('')
  const [targetLang, setTargetLang] = useState('hi')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [copied, setCopied] = useState(false)

  const languages = [
    { code: 'hi', name: 'Hindi' },
    { code: 'ta', name: 'Tamil' },
    { code: 'te', name: 'Telugu' },
    { code: 'bn', name: 'Bengali' },
    { code: 'mr', name: 'Marathi' },
    { code: 'kn', name: 'Kannada' },
    { code: 'ml', name: 'Malayalam' },
    { code: 'gu', name: 'Gujarati' },
  ]

  const exampleTexts = [
    'Parking Available',
    'No Parking',
    'Turn Left',
    'Road Closed',
    'Bus Stop Ahead',
  ]

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!text.trim()) return

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await axios.post('/api/translation/simple', {
        text,
        target_lang: targetLang,
      })
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to translate text')
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = () => {
    if (result?.translated_text) {
      navigator.clipboard.writeText(result.translated_text)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Sign Translation</h1>
        <p className="text-gray-600">Translate traffic signs and directions to your preferred language</p>
      </div>

      <form onSubmit={handleSubmit} className="card mb-6">
        <div className="space-y-4">
          <div>
            <label className="label">
              <Languages className="w-4 h-4 inline mr-1" />
              Text to Translate
            </label>
            <textarea
              className="input-field min-h-[120px] resize-none"
              placeholder="Enter text from a sign or direction..."
              value={text}
              onChange={(e) => setText(e.target.value)}
              required
            />
            <div className="mt-2">
              <p className="text-sm text-gray-600 mb-2">Quick examples:</p>
              <div className="flex flex-wrap gap-2">
                {exampleTexts.map((example, index) => (
                  <button
                    key={index}
                    type="button"
                    onClick={() => setText(example)}
                    className="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
                  >
                    {example}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div>
            <label className="label">Target Language</label>
            <select
              className="input-field"
              value={targetLang}
              onChange={(e) => setTargetLang(e.target.value)}
            >
              {languages.map((lang) => (
                <option key={lang.code} value={lang.code}>
                  {lang.name}
                </option>
              ))}
            </select>
          </div>

          <button
            type="submit"
            className="btn-primary w-full flex items-center justify-center space-x-2"
            disabled={loading || !text.trim()}
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Translating...</span>
              </>
            ) : (
              <>
                <Languages className="w-5 h-5" />
                <span>Translate</span>
              </>
            )}
          </button>
        </div>
      </form>

      {error && (
        <div className="card bg-red-50 border-red-200 mb-6">
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {result && (
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-semibold text-gray-900">Translation Result</h2>
            <button
              onClick={handleCopy}
              className="flex items-center space-x-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
            >
              {copied ? (
                <>
                  <Check className="w-4 h-4 text-green-600" />
                  <span className="text-sm text-green-600">Copied!</span>
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4 text-gray-600" />
                  <span className="text-sm text-gray-600">Copy</span>
                </>
              )}
            </button>
          </div>

          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-600 mb-2">Original Text ({result.source_lang.toUpperCase()})</p>
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-gray-900">{result.original_text}</p>
              </div>
            </div>

            <div>
              <p className="text-sm text-gray-600 mb-2">
                Translated Text ({result.target_lang.toUpperCase()})
              </p>
              <div className="bg-primary-50 rounded-lg p-4">
                <p className="text-primary-900 text-lg font-medium">{result.translated_text}</p>
              </div>
            </div>

            {result.is_mock && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                <p className="text-sm text-yellow-800">
                  ⚠️ This is a mock translation for demo purposes. In production, this would use a real translation service.
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default Translation

