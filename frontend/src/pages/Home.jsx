import { Link } from 'react-router-dom'
import { MapPin, ArrowRight, Sparkles } from 'lucide-react'

const Home = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Hero Section */}
      <div className="text-center py-20">
        <div className="inline-flex items-center justify-center w-20 h-20 bg-primary-100 rounded-2xl mb-6">
          <MapPin className="w-10 h-10 text-primary-600" />
        </div>
        
        <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-4">
          MARGSATHI
        </h1>
        
        <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Intelligent Mobility Platform
          <br />
          <span className="text-primary-600 font-semibold">
            Navigate smarter, park easier, understand better
          </span>
        </p>
        
        <Link to="/routing" className="btn-primary inline-flex items-center space-x-2">
          <span>Try Demo</span>
          <ArrowRight className="w-5 h-5" />
        </Link>
      </div>

      {/* Features Grid */}
      <div className="grid md:grid-cols-3 gap-8 mt-20">
        <div className="card text-center hover:shadow-lg transition-shadow">
          <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <MapPin className="w-6 h-6 text-primary-600" />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">Smart Routing</h3>
          <p className="text-gray-600">
            Get intelligent route suggestions based on real-time events and traffic conditions.
          </p>
          <Link
            to="/routing"
            className="text-primary-600 hover:text-primary-700 font-medium mt-4 inline-block"
          >
            Try Routing →
          </Link>
        </div>

        <div className="card text-center hover:shadow-lg transition-shadow">
          <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <Sparkles className="w-6 h-6 text-primary-600" />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">Parking Prediction</h3>
          <p className="text-gray-600">
            Predict parking availability by area, time, and historical patterns.
          </p>
          <Link
            to="/parking"
            className="text-primary-600 hover:text-primary-700 font-medium mt-4 inline-block"
          >
            Check Parking →
          </Link>
        </div>

        <div className="card text-center hover:shadow-lg transition-shadow">
          <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <Sparkles className="w-6 h-6 text-primary-600" />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">Sign Translation</h3>
          <p className="text-gray-600">
            Translate traffic signs and directions to your preferred language instantly.
          </p>
          <Link
            to="/translation"
            className="text-primary-600 hover:text-primary-700 font-medium mt-4 inline-block"
          >
            Translate Signs →
          </Link>
        </div>
      </div>

      {/* Stats Section */}
      <div className="mt-20 grid md:grid-cols-3 gap-6">
        <div className="text-center">
          <div className="text-3xl font-bold text-primary-600 mb-2">3+</div>
          <div className="text-gray-600">Core Features</div>
        </div>
        <div className="text-center">
          <div className="text-3xl font-bold text-primary-600 mb-2">9+</div>
          <div className="text-gray-600">Languages Supported</div>
        </div>
        <div className="text-center">
          <div className="text-3xl font-bold text-primary-600 mb-2">24/7</div>
          <div className="text-gray-600">Real-time Updates</div>
        </div>
      </div>
    </div>
  )
}

export default Home

