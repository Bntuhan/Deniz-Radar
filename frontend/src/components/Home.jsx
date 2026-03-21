import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'

export default function Home() {
  const [user, setUser] = useState(null)
  const [ownShip, setOwnShip] = useState(null)
  const [pendingInvites, setPendingInvites] = useState([])
  
  // Form stats
  const [captainName, setCaptainName] = useState('')
  const [lat, setLat] = useState(41.0)
  const [lon, setLon] = useState(29.0)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return
    setUser(user)

    // Load own ship
    const { data: shipsData } = await supabase.from('ships').select('*').eq('user_id', user.id).order('id', { ascending: false }).limit(1)
    if (shipsData && shipsData.length > 0) {
      const shipData = shipsData[0]
      setOwnShip(shipData)
      setCaptainName(shipData.captain || '')
      setLat(shipData.lat || 41.0)
      setLon(shipData.lon || 29.0)
    }

    // Load pending invites
    const { data: invitesData } = await supabase.from('invites').select('*').eq('to_user', user.id).eq('status', 'pending')
    if (invitesData) {
      setPendingInvites(invitesData)
    }
  }

  const handleUpdateLocation = async () => {
    navigator.geolocation.getCurrentPosition((pos) => {
      setLat(pos.coords.latitude)
      setLon(pos.coords.longitude)
    }, (err) => {
      alert("Konum alınamadı: " + err.message)
    }, {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 0
    })
  }

  const handleSaveShip = async () => {
    if (!user) return
    setLoading(true)
    try {
      const strLat = String(lat).replace(',', '.')
      const strLon = String(lon).replace(',', '.')
      const parsedLat = parseFloat(strLat)
      const parsedLon = parseFloat(strLon)
      if (isNaN(parsedLat) || isNaN(parsedLon)) {
        alert("Geçersiz koordinat değeri!")
        setLoading(false)
        return
      }

      if (ownShip) {
        const { error } = await supabase.from('ships').update({ captain: captainName, lat: parsedLat, lon: parsedLon }).eq('id', ownShip.id)
        if (error) throw error
      } else {
        const { error } = await supabase.from('ships').insert({ user_id: user.id, captain: captainName, lat: parsedLat, lon: parsedLon })
        if (error) throw error
      }
      alert('Transponder yayını başarıyla başlatıldı!')
      loadData()
    } catch (e) {
      alert(e.message)
    } finally {
      setLoading(false)
    }
  }

  const handleInvite = async (id, status) => {
    const { error } = await supabase.from('invites').update({ status }).eq('id', id)
    if (error) alert("Hata: " + error.message)
    loadData()
  }

  const handleLogout = async () => {
    await supabase.auth.signOut()
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', marginTop: '16px' }}>
        <div>
          <h1 className="text-gradient" style={{ fontSize: '28px', margin: 0 }}>Gemi Paneli</h1>
          <p style={{ margin: '6px 0 0 0', color: '#94a3b8' }}>Kaptan: <span style={{ color: '#e2e8f0', fontWeight: 600 }}>{ownShip ? ownShip.captain : 'Atanmadı'}</span></p>
        </div>
        <button className="btn-secondary" style={{ width: 'auto', padding: '0.5rem 1rem' }} onClick={handleLogout}>Bağlantıyı Kes</button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '32px' }}>
        <div className="card" style={{ marginBottom: 0, padding: '24px' }}>
          <div style={{ fontSize: '13px', color: '#94a3b8', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Gelen Çağrılar</div>
          <div style={{ fontSize: '32px', fontWeight: 800, color: '#f8fafc', marginTop: '8px' }}>{pendingInvites.length}</div>
        </div>
        <div className="card" style={{ marginBottom: 0, padding: '24px' }}>
          <div style={{ fontSize: '13px', color: '#94a3b8', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Transponder</div>
          <div style={{ fontSize: '32px', fontWeight: 800, color: ownShip ? '#38bdf8' : '#64748b', marginTop: '8px' }}>
            {ownShip ? 'Aktif' : 'Pasif'}
          </div>
        </div>
      </div>

      <div className="section-title">🚢 Konum Yayını</div>
      <div className="card">
        <label style={{ marginBottom: '8px', display: 'block' }}>Gemi veya Kaptan Adı</label>
        <input className="input-field" value={captainName} onChange={e => setCaptainName(e.target.value)} placeholder="Örn: Barbaros" />
        
        <div style={{ display: 'flex', gap: '12px' }}>
          <div style={{ flex: 1 }}>
            <label style={{ marginBottom: '8px', display: 'block' }}>Enlem (Lat)</label>
            <input type="text" className="input-field" value={lat} onChange={e => {
              const v = e.target.value.replace(',', '.')
              setLat(v)
            }} />
          </div>
          <div style={{ flex: 1 }}>
            <label style={{ marginBottom: '8px', display: 'block' }}>Boylam (Lon)</label>
            <input type="text" className="input-field" value={lon} onChange={e => {
              const v = e.target.value.replace(',', '.')
              setLon(v)
            }} />
          </div>
        </div>
        
        <div style={{ display: 'flex', gap: '12px', marginTop: '16px' }}>
          <button className="btn-secondary" onClick={handleUpdateLocation} style={{ flex: 1 }}>📍 GPS Koordinat</button>
          <button className="btn-primary" onClick={handleSaveShip} disabled={loading} style={{ flex: 2 }}>{ownShip ? 'Sinyali Güncelle' : 'Yayına Başla'}</button>
        </div>
      </div>

      <div className="section-title">📥 Gelen Bağlantı Talepleri</div>
      {pendingInvites.length === 0 ? (
        <div style={{ color: '#64748b', fontSize: '14px', fontStyle: 'italic', background: 'rgba(15, 23, 42, 0.4)', padding: '20px', borderRadius: '16px', border: '1px dashed rgba(71, 85, 105, 0.5)', textAlign: 'center' }}>
          Sinyal alanında bekleyen bağlantı talebi yok.
        </div>
      ) : (
        pendingInvites.map(inv => (
          <div key={inv.id} className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px 20px' }}>
            <div>
              <div style={{ color: '#f8fafc', fontWeight: 600 }}>Bilinmeyen Gemi</div>
              <div style={{ color: '#94a3b8', fontSize: '13px' }}>ID: {inv.from_user.substring(0,8)}...</div>
            </div>
            <div style={{ display: 'flex', gap: '8px' }}>
              <button className="btn-secondary" style={{ color: '#f87171', padding: '0.5rem 1rem' }} onClick={() => handleInvite(inv.id, 'rejected')}>Reddet</button>
              <button className="btn-primary" style={{ padding: '0.5rem 1rem' }} onClick={() => handleInvite(inv.id, 'accepted')}>Bağlan</button>
            </div>
          </div>
        ))
      )}
    </div>
  )
}
