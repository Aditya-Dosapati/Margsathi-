import { useState } from 'react'
import { MapPin, Navigation, Clock, Leaf, Loader2 } from 'lucide-react'
import axios from 'axios'

const Routing = () => {
  const [source, setSource] = useState('')
  const [destination, setDestination] = useState('')
  const [event, setEvent] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const eventTypes = [
    { value: '', label: 'No Event' },
    { value: 'Road Closure', label: 'Road Closure' },
    { value: 'Political Rally', label: 'Political Rally' },
    { value: 'Protest', label: 'Protest' },
    { value: 'Concert', label: 'Concert' },
    { value: 'Accident', label: 'Accident' },
    { value: 'Construction', label: 'Construction' },
  ]

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await axios.post('/api/routing/suggest', {
        source,
        destination,
        event,
        mode: 'car',
      })

      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to get route suggestion')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Smart Routing</h1>
        <p className="text-gray-600">Get intelligent route suggestions based on real-time events</p>
      </div>

      <form onSubmit={handleSubmit} className="card mb-6">
        <div className="space-y-4">
          <div>
            <label className="label">
              <MapPin className="w-4 h-4 inline mr-1" />
              Source Location
            </label>
            <input
              type="text"
              className="input-field"
              placeholder="e.g., BTM Layout"
              value={source}
              onChange={(e) => setSource(e.target.value)}
              required
            />
          </div>

          <div>
            <label className="label">
              <Navigation className="w-4 h-4 inline mr-1" />
              Destination Location
            </label>
            <input
              type="text"
              className="input-field"
              placeholder="e.g., MG Road"
              value={destination}
              onChange={(e) => setDestination(e.target.value)}
              required
            />
          </div>

          <div>
            <label className="label">Event Type (Optional)</label>
            <select
              className="input-field"
              value={event}
              onChange={(e) => setEvent(e.target.value)}
            >
              {eventTypes.map((type) => (
                <option key={type.value} value={type.value}>
                  {type.label}
                </option>
              ))}
            </select>
          </div>

          <button
            type="submit"
            className="btn-primary w-full flex items-center justify-center space-x-2"
            disabled={loading}
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Finding Route...</span>
              </>
            ) : (
              <>
                <Navigation className="w-5 h-5" />
                <span>Get Route</span>
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
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">Route Result</h2>
          
          <div className="bg-primary-50 rounded-lg p-4 mb-4">
            <div className="flex items-start space-x-2">
              <Navigation className="w-5 h-5 text-primary-600 mt-1" />
              <div className="flex-1">
                <p className="font-semibold text-gray-900 mb-1">Recommended Route</p>
                <p className="text-primary-700 text-lg">{result.recommended_route}</p>
              </div>
            </div>
          </div>

          <div className="bg-gray-50 rounded-lg p-4 mb-4">
            <p className="text-sm text-gray-600 mb-1">Reason</p>
            <p className="text-gray-900">{result.reason}</p>
          </div>

          <div className="grid md:grid-cols-3 gap-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                <Navigation className="w-5 h-5 text-primary-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">Distance</p>
                <p className="font-semibold text-gray-900">{result.distance_km} km</p>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                <Clock className="w-5 h-5 text-primary-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">Duration</p>
                <p className="font-semibold text-gray-900">{result.duration_minutes} min</p>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                <Leaf className="w-5 h-5 text-primary-600" />
              </div>
              <div>
                <p className="text-sm text-gray-600">CO₂ Emissions</p>
                <p className="font-semibold text-gray-900">{result.estimated_co2_kg} kg</p>
              </div>
            </div>
          </div>

          {result.waypoints && result.waypoints.length > 0 && (
            <div className="mt-4 pt-4 border-t border-gray-200">
              <p className="text-sm text-gray-600 mb-2">Waypoints:</p>
              <div className="flex flex-wrap gap-2">
                {result.waypoints.map((waypoint, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-gray-100 rounded-full text-sm text-gray-700"
                  >
                    {waypoint}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default Routing

