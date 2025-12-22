import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Routing from './pages/Routing'
import Parking from './pages/Parking'
import Translation from './pages/Translation'
import Layout from './components/Layout'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/routing" element={<Routing />} />
          <Route path="/parking" element={<Parking />} />
          <Route path="/translation" element={<Translation />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App

