import { useState, useEffect, useRef } from 'react'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import { supabase } from '../lib/supabase'

import L from 'leaflet'
const createCustomIcon = (isMe) => L.divIcon({
  className: 'custom-radar-icon',
  html: `<div style="background-color: ${isMe ? '#38bdf8' : '#cbd5e1'}; width: 14px; height: 14px; border-radius: 50%; box-shadow: 0 0 15px ${isMe ? '#38bdf8' : '#cbd5e1'}; border: 2px solid rgba(255,255,255,0.8);"></div>`,
  iconSize: [20, 20],
  iconAnchor: [10, 10]
})

function calcDistance(lat1, lon1, lat2, lon2) {
  const R = 6371
  const dLat = (lat2 - lat1) * Math.PI / 180
  const dLon = (lon2 - lon1) * Math.PI / 180
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLon/2) * Math.sin(dLon/2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))
  return R * c
}

export default function Map() {
  const [ships, setShips] = useState([])
  const [ownShip, setOwnShip] = useState(null)
  const [user, setUser] = useState(null)
  const [range, setRange] = useState(25)
  const mapRef = useRef(null)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return
    setUser(user)

    const { data } = await supabase.from('ships').select('*')
    if (data) {
      // Keep only newest ship per user
      const latestShips = {}
      for (const s of data) {
        if (!latestShips[s.user_id] || s.id > latestShips[s.user_id].id) {
          latestShips[s.user_id] = s
        }
      }
      const finalShips = Object.values(latestShips)
      
      setShips(finalShips)
      const mine = latestShips[user.id]
      if (mine) setOwnShip(mine)
    }
  }

  const sendInvite = async (targetUserId) => {
    try {
      if (!user) return
      const { error } = await supabase.from('invites').insert({
        from_user: user.id,
        to_user: targetUserId,
        room_id: crypto.randomUUID(),
        status: 'pending'
      })
      if (error) throw error
      alert('Sinyal gönderildi!')
    } catch (e) {
      alert('Hata: ' + e.message)
    }
  }

  const centerLat = ownShip && !isNaN(ownShip.lat) ? ownShip.lat : 41.0
  const centerLon = ownShip && !isNaN(ownShip.lon) ? ownShip.lon : 29.0

  const validShips = ships.filter(s => s.lat != null && s.lon != null && !isNaN(parseFloat(s.lat)) && !isNaN(parseFloat(s.lon)))

  const nearbyShips = validShips.filter(s => {
    if (s.id === ownShip?.id) return false
    const d = calcDistance(centerLat, centerLon, parseFloat(s.lat), parseFloat(s.lon))
    return d <= range
  })

  return (
    <div>
      <div className="section-title" style={{ marginTop: '16px' }}>🗺️ Taktik Radar</div>
      
      <div className="card" style={{ padding: '20px', marginBottom: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '12px', alignItems: 'center' }}>
          <label style={{ margin: 0 }}>Tarama Menzili</label>
          <div style={{ background: 'rgba(56, 189, 248, 0.1)', border: '1px solid rgba(56, 189, 248, 0.3)', padding: '4px 10px', borderRadius: '8px', color: '#38bdf8', fontWeight: 700, fontSize: '14px' }}>
            {range} km
          </div>
        </div>
        <input 
          type="range" 
          min="1" max="100" 
          value={range} 
          onChange={(e) => setRange(parseInt(e.target.value))} 
          style={{ width: '100%', accentColor: '#38bdf8', marginTop: '4px' }}
        />
      </div>

      <div style={{ borderRadius: '24px', overflow: 'hidden', border: '1px solid rgba(56, 189, 248, 0.3)', boxShadow: '0 10px 30px rgba(0,0,0,0.5)', marginBottom: '32px', position: 'relative' }}>
        
        <button 
          onClick={() => {
            if (mapRef.current) {
              mapRef.current.flyTo([centerLat, centerLon], 13, { duration: 1.5 })
            }
          }}
          style={{ position: 'absolute', bottom: '20px', left: '20px', zIndex: 1000, padding: '8px 16px', borderRadius: '20px', background: 'rgba(15, 23, 42, 0.8)', border: '1px solid rgba(56, 189, 248, 0.5)', color: '#38bdf8', fontWeight: 600, cursor: 'pointer', backdropFilter: 'blur(10px)', boxShadow: '0 4px 12px rgba(0,0,0,0.5)' }}
        >
          🧭 Gemim
        </button>

        <MapContainer ref={mapRef} center={[centerLat, centerLon]} zoom={8} scrollWheelZoom={true} style={{ height: '420px', width: '100%' }}>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {validShips.map(s => {
            const isMe = s.id === ownShip?.id
            const plat = parseFloat(s.lat)
            const plon = parseFloat(s.lon)
            const d = calcDistance(centerLat, centerLon, plat, plon)
            if (!isMe && d > range) return null

            return (
              <Marker key={s.id} position={[plat, plon]} icon={createCustomIcon(isMe)}>
                <Popup>
                  <div style={{ background: '#0f172a', padding: '4px', borderRadius: '4px' }}>
                    <strong style={{ color: '#38bdf8', fontSize: '14px' }}>{s.captain}</strong><br/>
                    <span style={{ color: '#94a3b8' }}>{isMe ? 'Transponder: Sizin Geminiz' : `Mesafe: ${d.toFixed(1)} km`}</span><br/>
                    {!isMe && (
                      <button style={{ marginTop: '10px', width: '100%', cursor: 'pointer', padding: '6px 10px', borderRadius: '8px', background: 'linear-gradient(135deg, #0284c7, #3b82f6)', color: 'white', border: 'none', fontWeight: 600 }} onClick={() => sendInvite(s.user_id)}>
                        Bağlantı Kur
                      </button>
                    )}
                  </div>
                </Popup>
              </Marker>
            )
          })}
        </MapContainer>
      </div>

      <div className="section-title">🚢 Tespit Edilen Gemiler</div>
      {nearbyShips.length === 0 ? (
        <div style={{ color: '#64748b', fontSize: '14px', fontStyle: 'italic', background: 'rgba(15, 23, 42, 0.4)', padding: '20px', borderRadius: '16px', border: '1px dashed rgba(71, 85, 105, 0.5)', textAlign: 'center' }}>
          Tarama menzilinde herhangi bir gemi tespit edilemedi.
        </div>
      ) : (
        nearbyShips.map(s => {
          const d = calcDistance(centerLat, centerLon, s.lat, s.lon)
          return (
            <div key={s.id} className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px 20px' }}>
              <div>
                <div style={{ fontWeight: 700, color: '#f8fafc', fontSize: '16px' }}>{s.captain}</div>
                <div style={{ fontSize: '13px', color: '#38bdf8', display: 'flex', alignItems: 'center', gap: '6px', marginTop: '4px' }}>
                  <span className="pulsing-dot" style={{ width: '6px', height: '6px' }}></span>
                  {d.toFixed(1)} km uzaklıkta
                </div>
              </div>
              <button className="btn-secondary" style={{ width: 'auto', padding: '0.6rem 1.2rem' }} onClick={() => sendInvite(s.user_id)}>Sinyal Gönder</button>
            </div>
          )
        })
      )}
    </div>
  )
}
