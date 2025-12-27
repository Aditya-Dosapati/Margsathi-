import { useState, useRef, useEffect } from 'react'
import {
  Languages,
  Loader2,
  Copy,
  Check,
  Image as ImageIcon,
  Upload,
  ArrowLeftRight,
  Sparkles,
  History,
  X
} from 'lucide-react'
import axios from 'axios'

const Translation = () => {
  // Text translation state
  const [text, setText] = useState('')
  const [targetLang, setTargetLang] = useState('hi')
  const [sourceLang, setSourceLang] = useState('en')
  const [provider, setProvider] = useState('deep')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [copied, setCopied] = useState(false)

  // Image translation state
  const [imageMode, setImageMode] = useState(false)
  const [selectedImage, setSelectedImage] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  const [imageLoading, setImageLoading] = useState(false)
  const [imageResult, setImageResult] = useState(null)
  const fileInputRef = useRef(null)

  // Translation history
  const [history, setHistory] = useState([])
  const [showHistory, setShowHistory] = useState(false)

  // Tesseract OCR availability
  const [tesseractAvailable, setTesseractAvailable] = useState(true)
  const [statusChecked, setStatusChecked] = useState(false)

  const languages = [
    { code: 'en', name: 'English', flag: '🇬🇧' },
    { code: 'hi', name: 'Hindi', flag: '🇮🇳' },
    { code: 'ta', name: 'Tamil', flag: '🇮🇳' },
    { code: 'te', name: 'Telugu', flag: '🇮🇳' },
    { code: 'bn', name: 'Bengali', flag: '🇮🇳' },
    { code: 'mr', name: 'Marathi', flag: '🇮🇳' },
    { code: 'kn', name: 'Kannada', flag: '🇮🇳' },
    { code: 'ml', name: 'Malayalam', flag: '🇮🇳' },
    { code: 'gu', name: 'Gujarati', flag: '🇮🇳' },
  ]

  const exampleTexts = [
    'Parking Available',
    'No Parking',
    'Turn Left',
    'Road Closed',
    'Bus Stop Ahead',
    'One Way Street',
    'Speed Limit 40',
    'Hospital Zone',
  ]

  const providers = [
    { value: 'deep', name: 'Deep Translator', description: 'Free, Fast' },
    { value: 'google', name: 'Google Translate', description: 'High Quality' },
    { value: 'mock', name: 'Demo Mode', description: 'Testing Only' },
  ]

  // Check translation service status on mount
  useEffect(() => {
    const checkStatus = async () => {
      try {
        const response = await axios.get('/api/translation/status')
        setTesseractAvailable(response.data.image_translation.available)
        setStatusChecked(true)
      } catch (err) {
        console.error('Failed to check translation status:', err)
        setStatusChecked(true)
      }
    }
    checkStatus()
  }, [])

  // Text translation
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
        source_lang: sourceLang,
        provider: provider,
      })

      const translationResult = response.data
      setResult(translationResult)

      // Add to history
      const historyItem = {
        id: Date.now(),
        original: text,
        translated: translationResult.translated_text,
        sourceLang: translationResult.source_lang,
        targetLang: translationResult.target_lang,
        provider: translationResult.provider,
        timestamp: new Date().toLocaleString(),
      }
      setHistory(prev => [historyItem, ...prev.slice(0, 9)]) // Keep last 10
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to translate text')
    } finally {
      setLoading(false)
    }
  }

  // Image translation
  const handleImageSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      setSelectedImage(file)
      const reader = new FileReader()
      reader.onloadend = () => {
        setImagePreview(reader.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleImageTranslate = async () => {
    if (!selectedImage) return

    setImageLoading(true)
    setError(null)
    setImageResult(null)

    try {
      const formData = new FormData()
      formData.append('file', selectedImage)
      formData.append('target_lang', targetLang)
      formData.append('source_lang', sourceLang)
      formData.append('provider', provider)

      const response = await axios.post('/api/translation/translate-image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      setImageResult(response.data)

      // Add to history
      const historyItem = {
        id: Date.now(),
        original: response.data.extracted_text,
        translated: response.data.translated_text,
        sourceLang: response.data.source_lang,
        targetLang: response.data.target_lang,
        provider: response.data.provider,
        timestamp: new Date().toLocaleString(),
        isImage: true,
      }
      setHistory(prev => [historyItem, ...prev.slice(0, 9)])
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to translate image')
    } finally {
      setImageLoading(false)
    }
  }

  const handleCopy = (textToCopy) => {
    navigator.clipboard.writeText(textToCopy)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const swapLanguages = () => {
    const temp = sourceLang
    setSourceLang(targetLang)
    setTargetLang(temp)
  }

  const clearImage = () => {
    setSelectedImage(null)
    setImagePreview(null)
    setImageResult(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const loadFromHistory = (item) => {
    setText(item.original)
    setSourceLang(item.sourceLang)
    setTargetLang(item.targetLang)
    setShowHistory(false)
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="flex items-center justify-center gap-3 mb-3">
          <Languages className="w-10 h-10 text-primary-600" />
          <h1 className="text-4xl font-bold text-gray-900">Sign Translation</h1>
          <Sparkles className="w-8 h-8 text-yellow-500" />
        </div>
        <p className="text-gray-600 text-lg">
          Translate traffic signs and directions to your preferred language
        </p>
        <p className="text-sm text-gray-500 mt-2">
          Now with real translation powered by AI • Support for image OCR
        </p>
      </div>

      {/* Mode Toggle */}
      <div className="flex justify-center gap-4 mb-6">
        <button
          onClick={() => setImageMode(false)}
          className={`px-6 py-3 rounded-lg font-medium transition-all ${!imageMode
            ? 'bg-primary-600 text-white shadow-lg'
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
        >
          <Languages className="w-5 h-5 inline mr-2" />
          Text Translation
        </button>
        <button
          onClick={() => setImageMode(true)}
          className={`px-6 py-3 rounded-lg font-medium transition-all ${imageMode
            ? 'bg-primary-600 text-white shadow-lg'
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
        >
          <ImageIcon className="w-5 h-5 inline mr-2" />
          Image Translation
        </button>
        <button
          onClick={() => setShowHistory(!showHistory)}
          className="px-6 py-3 rounded-lg font-medium bg-gray-100 text-gray-700 hover:bg-gray-200 transition-all relative"
        >
          <History className="w-5 h-5 inline mr-2" />
          History
          {history.length > 0 && (
            <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
              {history.length}
            </span>
          )}
        </button>
      </div>

      {/* History Panel */}
      {showHistory && history.length > 0 && (
        <div className="card mb-6 bg-gradient-to-br from-blue-50 to-indigo-50">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Translation History</h3>
            <button
              onClick={() => setShowHistory(false)}
              className="text-gray-500 hover:text-gray-700"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {history.map((item) => (
              <div
                key={item.id}
                onClick={() => loadFromHistory(item)}
                className="p-3 bg-white rounded-lg hover:shadow-md transition-shadow cursor-pointer"
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs text-gray-500">{item.timestamp}</span>
                  <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                    {item.provider}
                  </span>
                </div>
                <div className="text-sm">
                  <span className="text-gray-600">{item.original.substring(0, 50)}...</span>
                  <span className="mx-2">→</span>
                  <span className="text-primary-600 font-medium">
                    {item.translated.substring(0, 50)}...
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Settings Panel */}
        <div className="lg:col-span-1">
          <div className="card sticky top-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Settings</h3>

            {/* Language Selection */}
            <div className="space-y-4">
              <div>
                <label className="label">Source Language</label>
                <select
                  className="input-field"
                  value={sourceLang}
                  onChange={(e) => setSourceLang(e.target.value)}
                >
                  {languages.map((lang) => (
                    <option key={lang.code} value={lang.code}>
                      {lang.flag} {lang.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="flex justify-center">
                <button
                  onClick={swapLanguages}
                  className="p-2 bg-gray-100 hover:bg-gray-200 rounded-full transition-colors"
                  title="Swap languages"
                >
                  <ArrowLeftRight className="w-5 h-5 text-gray-600" />
                </button>
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
                      {lang.flag} {lang.name}
                    </option>
                  ))}
                </select>
              </div>

              {/* Provider Selection */}
              <div>
                <label className="label">Translation Provider</label>
                <div className="space-y-2">
                  {providers.map((p) => (
                    <label
                      key={p.value}
                      className={`flex items-center p-3 border-2 rounded-lg cursor-pointer transition-all ${provider === p.value
                        ? 'border-primary-500 bg-primary-50'
                        : 'border-gray-200 hover:border-gray-300'
                        }`}
                    >
                      <input
                        type="radio"
                        name="provider"
                        value={p.value}
                        checked={provider === p.value}
                        onChange={(e) => setProvider(e.target.value)}
                        className="mr-3"
                      />
                      <div>
                        <div className="font-medium text-gray-900">{p.name}</div>
                        <div className="text-xs text-gray-500">{p.description}</div>
                      </div>
                    </label>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Translation Panel */}
        <div className="lg:col-span-2">
          {!imageMode ? (
            // Text Translation Mode
            <form onSubmit={handleSubmit} className="card">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Text Translation</h3>

              <div className="space-y-4">
                <div>
                  <label className="label">Text to Translate</label>
                  <textarea
                    className="input-field min-h-[150px] resize-none"
                    placeholder="Enter text from a sign or direction..."
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    required
                  />
                  <div className="mt-3">
                    <p className="text-sm text-gray-600 mb-2">Quick examples:</p>
                    <div className="flex flex-wrap gap-2">
                      {exampleTexts.map((example, index) => (
                        <button
                          key={index}
                          type="button"
                          onClick={() => setText(example)}
                          className="px-3 py-1.5 text-sm bg-gradient-to-r from-blue-50 to-indigo-50 hover:from-blue-100 hover:to-indigo-100 border border-blue-200 rounded-lg transition-all"
                        >
                          {example}
                        </button>
                      ))}
                    </div>
                  </div>
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
          ) : (
            // Image Translation Mode
            <div className="card">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Image Translation</h3>

              <div className="space-y-4">
                {!imagePreview ? (
                  <div
                    onClick={() => fileInputRef.current?.click()}
                    className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-primary-500 hover:bg-primary-50 transition-all cursor-pointer"
                  >
                    <Upload className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                    <p className="text-gray-600 mb-2">Click to upload an image</p>
                    <p className="text-sm text-gray-500">PNG, JPG, JPEG up to 10MB</p>
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept="image/*"
                      onChange={handleImageSelect}
                      className="hidden"
                    />
                  </div>
                ) : (
                  <div className="relative">
                    <img
                      src={imagePreview}
                      alt="Preview"
                      className="w-full rounded-lg shadow-md max-h-96 object-contain bg-gray-50"
                    />
                    <button
                      onClick={clearImage}
                      className="absolute top-2 right-2 p-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors"
                    >
                      <X className="w-5 h-5" />
                    </button>
                  </div>
                )}

                {imagePreview && (
                  <button
                    onClick={handleImageTranslate}
                    className="btn-primary w-full flex items-center justify-center space-x-2"
                    disabled={imageLoading}
                  >
                    {imageLoading ? (
                      <>
                        <Loader2 className="w-5 h-5 animate-spin" />
                        <span>Processing Image...</span>
                      </>
                    ) : (
                      <>
                        <ImageIcon className="w-5 h-5" />
                        <span>Extract & Translate</span>
                      </>
                    )}
                  </button>
                )}
              </div>
            </div>
          )}

          {/* Tesseract Warning for Image Mode */}
          {imageMode && !tesseractAvailable && statusChecked && (
            <div className="card mt-6 bg-yellow-50 border-2 border-yellow-300">
              <div className="flex items-start gap-3">
                <div className="text-2xl">⚠️</div>
                <div className="flex-1">
                  <h4 className="font-semibold text-yellow-900 mb-2">
                    Tesseract OCR Not Installed
                  </h4>
                  <p className="text-sm text-yellow-800 mb-3">
                    Image translation requires Tesseract OCR to extract text from images.
                    Please install Tesseract to use this feature.
                  </p>
                  <div className="text-sm text-yellow-900">
                    <p className="font-medium mb-1">Installation:</p>
                    <ul className="list-disc list-inside space-y-1 ml-2">
                      <li>
                        <strong>Windows:</strong>{' '}
                        <a
                          href="https://github.com/UB-Mannheim/tesseract/wiki"
                          target="_blank"
                          rel="noopener noreferrer"
                          className="underline hover:text-yellow-700"
                        >
                          Download installer
                        </a>
                      </li>
                      <li><strong>Linux:</strong> sudo apt-get install tesseract-ocr</li>
                      <li><strong>Mac:</strong> brew install tesseract</li>
                    </ul>
                  </div>
                  <p className="text-xs text-yellow-700 mt-3">
                    After installation, restart the backend server to enable image translation.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Error Display */}
          {error && (
            <div className="card bg-red-50 border-red-200 mt-6">
              <p className="text-red-700">{error}</p>
            </div>
          )}

          {/* Text Translation Result */}
          {result && !imageMode && (
            <div className="card mt-6 bg-gradient-to-br from-green-50 to-emerald-50">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-semibold text-gray-900">Translation Result</h2>
                <div className="flex items-center gap-2">
                  {result.confidence && (
                    <span className="text-sm bg-green-100 text-green-700 px-3 py-1 rounded-full">
                      {Math.round(result.confidence * 100)}% confident
                    </span>
                  )}
                  <button
                    onClick={() => handleCopy(result.translated_text)}
                    className="flex items-center space-x-2 px-4 py-2 bg-white hover:bg-gray-50 rounded-lg transition-colors shadow-sm"
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
              </div>

              <div className="space-y-4">
                <div>
                  <p className="text-sm text-gray-600 mb-2">
                    Original Text ({result.source_lang.toUpperCase()})
                  </p>
                  <div className="bg-white rounded-lg p-4 shadow-sm">
                    <p className="text-gray-900">{result.original_text}</p>
                  </div>
                </div>

                <div>
                  <p className="text-sm text-gray-600 mb-2">
                    Translated Text ({result.target_lang.toUpperCase()})
                  </p>
                  <div className="bg-white rounded-lg p-4 shadow-sm border-2 border-green-200">
                    <p className="text-primary-900 text-xl font-medium">
                      {result.translated_text}
                    </p>
                  </div>
                </div>

                <div className="flex items-center justify-between text-sm text-gray-600 pt-2 border-t">
                  <span>Provider: <strong>{result.provider}</strong></span>
                  {result.is_mock && (
                    <span className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-xs">
                      ⚠️ Demo Mode
                    </span>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Image Translation Result */}
          {imageResult && imageMode && (
            <div className="card mt-6 bg-gradient-to-br from-purple-50 to-pink-50">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-semibold text-gray-900">Image Translation Result</h2>
                <button
                  onClick={() => handleCopy(imageResult.translated_text)}
                  className="flex items-center space-x-2 px-4 py-2 bg-white hover:bg-gray-50 rounded-lg transition-colors shadow-sm"
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
                  <p className="text-sm text-gray-600 mb-2">
                    Extracted Text (OCR)
                    {imageResult.ocr_confidence && (
                      <span className="ml-2 text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                        {Math.round(imageResult.ocr_confidence * 100)}% OCR confidence
                      </span>
                    )}
                  </p>
                  <div className="bg-white rounded-lg p-4 shadow-sm">
                    <p className="text-gray-900 whitespace-pre-wrap">{imageResult.extracted_text}</p>
                  </div>
                </div>

                <div>
                  <p className="text-sm text-gray-600 mb-2">
                    Translated Text ({imageResult.target_lang.toUpperCase()})
                  </p>
                  <div className="bg-white rounded-lg p-4 shadow-sm border-2 border-purple-200">
                    <p className="text-primary-900 text-xl font-medium whitespace-pre-wrap">
                      {imageResult.translated_text}
                    </p>
                  </div>
                </div>

                <div className="flex items-center justify-between text-sm text-gray-600 pt-2 border-t">
                  <span>Provider: <strong>{imageResult.provider}</strong></span>
                  {imageResult.is_mock && (
                    <span className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-xs">
                      ⚠️ Demo Mode
                    </span>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Translation
