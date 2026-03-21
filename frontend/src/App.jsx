import { useState, useEffect } from 'react'
import { Router, Routes, Route, BrowserRouter } from 'react-router-dom'
import { supabase } from './lib/supabase'

import Auth from './components/Auth'
import Layout from './components/Layout'

// Pages
import HomePage from './components/Home'
import MapPage from './components/Map'
import ChatPage from './components/Chat'

function App() {
  const [session, setSession] = useState(null)
  
  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session)
    })

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session)
    })

    return () => subscription.unsubscribe()
  }, [])

  if (!session) {
    return (
      <div className="app-container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Auth />
      </div>
    )
  }

  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/map" element={<MapPage />} />
          <Route path="/chat" element={<ChatPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}

export default App
