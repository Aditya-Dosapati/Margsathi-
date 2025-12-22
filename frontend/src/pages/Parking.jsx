import { useState } from 'react'
import { ParkingCircle, Clock, TrendingUp, Loader2 } from 'lucide-react'
import axios from 'axios'

const Parking = () => {
  const [area, setArea] = useState('MG Road')
  const [areaType, setAreaType] = useState('commercial')
  const [timeOfDay, setTimeOfDay] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const areaTypes = [
    { value: 'commercial', label: 'Commercial' },
    { value: 'residential', label: 'Residential' },
    { value: 'mixed', label: 'Mixed' },
  ]

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const params = {
        area,
        area_type: areaType,
      }
      if (timeOfDay) {
        params.time_of_day = timeOfDay
      }

      const response = await axios.get('/api/parking/predict', { params })
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to get parking prediction')
    } finally {
      setLoading(false)
    }
  }

  const getAvailabilityColor = (availability) => {
    switch (availability) {
      case 'High':
        return 'text-green-600 bg-green-50'
      case 'Medium':
        return 'text-yellow-600 bg-yellow-50'
      case 'Low':
        return 'text-red-600 bg-red-50'
      default:
        return 'text-gray-600 bg-gray-50'
    }
  }

  const getOccupancyPercentage = () => {
    if (!result) return 0
    return result.predicted_occupancy_percent
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Parking Prediction</h1>
        <p className="text-gray-600">Predict parking availability by area and time</p>
      </div>

      <form onSubmit={handleSubmit} className="card mb-6">
        <div className="space-y-4">
          <div>
            <label className="label">
              <ParkingCircle className="w-4 h-4 inline mr-1" />
              Area Name
            </label>
            <input
              type="text"
              className="input-field"
              placeholder="e.g., MG Road, BTM Layout"
              value={area}
              onChange={(e) => setArea(e.target.value)}
              required
            />
          </div>

          <div>
            <label className="label">Area Type</label>
            <select
              className="input-field"
              value={areaType}
              onChange={(e) => setAreaType(e.target.value)}
            >
              {areaTypes.map((type) => (
                <option key={type.value} value={type.value}>
                  {type.label}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="label">
              <Clock className="w-4 h-4 inline mr-1" />
              Time of Day (Optional)
            </label>
            <input
              type="time"
              className="input-field"
              value={timeOfDay}
              onChange={(e) => setTimeOfDay(e.target.value)}
            />
            <p className="text-sm text-gray-500 mt-1">
              Leave empty to use current time
            </p>
          </div>

          <button
            type="submit"
            className="btn-primary w-full flex items-center justify-center space-x-2"
            disabled={loading}
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Predicting...</span>
              </>
            ) : (
              <>
                <TrendingUp className="w-5 h-5" />
                <span>Predict Availability</span>
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
          <h2 className="text-2xl font-semibold text-gray-900 mb-6">Prediction Result</h2>

          <div className="mb-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">Area: {result.area}</span>
              <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getAvailabilityColor(result.availability)}`}>
                {result.availability} Availability
              </span>
            </div>

            {/* Availability Meter */}
            <div className="w-full bg-gray-200 rounded-full h-8 mb-2 overflow-hidden">
              <div
                className={`h-full transition-all duration-500 ${
                  result.availability === 'High'
                    ? 'bg-green-500'
                    : result.availability === 'Medium'
                    ? 'bg-yellow-500'
                    : 'bg-red-500'
                }`}
                style={{ width: `${getOccupancyPercentage()}%` }}
              />
            </div>
            <div className="flex justify-between text-xs text-gray-600">
              <span>0%</span>
              <span className="font-semibold">{getOccupancyPercentage().toFixed(1)}% Occupied</span>
              <span>100%</span>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-4 mb-4">
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-sm text-gray-600 mb-1">Predicted Occupancy</p>
              <p className="text-2xl font-bold text-gray-900">
                {result.predicted_occupancy_percent}%
              </p>
            </div>

            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-sm text-gray-600 mb-1">Confidence</p>
              <p className="text-2xl font-bold text-gray-900">
                {(result.confidence * 100).toFixed(0)}%
              </p>
            </div>

            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-sm text-gray-600 mb-1">Time</p>
              <p className="text-lg font-semibold text-gray-900">{result.time_of_day}</p>
            </div>
          </div>

          <div className="bg-primary-50 rounded-lg p-4">
            <p className="text-sm text-gray-600 mb-1">Reason</p>
            <p className="text-gray-900">{result.reason}</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default Parking

