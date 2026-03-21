import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom'
import { Home, Map as MapIcon, MessageCircle } from 'lucide-react'

// Skeletons
import Dashboard from './Home'
import RadarMap from './Map'
import Chat from './Chat'

function BottomNav() {
  const location = useLocation()
  
  return (
    <div className="bottom-nav">
      <Link to="/" className={`nav-item ${location.pathname === '/' ? 'active' : ''}`}>
        <Home size={24} />
        <span>Home</span>
      </Link>
      <Link to="/map" className={`nav-item ${location.pathname === '/map' ? 'active' : ''}`}>
        <MapIcon size={24} />
        <span>Harita</span>
      </Link>
      <Link to="/chat" className={`nav-item ${location.pathname === '/chat' ? 'active' : ''}`}>
        <MessageCircle size={24} />
        <span>Chat</span>
      </Link>
    </div>
  )
}

export default function Layout({ children }) {
  return (
    <div className="app-container">
      {children}
      <BottomNav />
    </div>
  )
}
