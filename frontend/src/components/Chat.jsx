import { useState, useEffect, useRef } from 'react'
import { supabase } from '../lib/supabase'

export default function Chat() {
  const [user, setUser] = useState(null)
  const [conversations, setConversations] = useState([])
  const [activeRoom, setActiveRoom] = useState(null)
  const [activePartner, setActivePartner] = useState('')
  
  const [messages, setMessages] = useState([])
  const [newMessage, setNewMessage] = useState('')
  const messagesEndRef = useRef(null)

  useEffect(() => {
    const loadConversations = async () => {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) return
      setUser(user)

      // Accepted invites
      const { data: invites } = await supabase.from('invites').select('*').eq('status', 'accepted').or(`from_user.eq.${user.id},to_user.eq.${user.id}`)
      
      if (invites && invites.length > 0) {
        const { data: ships } = await supabase.from('ships').select('user_id, captain')
        const captainMap = {}
        if (ships) {
          ships.forEach(s => captainMap[s.user_id] = s.captain)
        }

        const convns = []
        const seenRooms = new Set()
        
        invites.forEach(inv => {
          if (!inv.room_id || seenRooms.has(inv.room_id)) return
          seenRooms.add(inv.room_id)
          
          const partnerId = inv.from_user === user.id ? inv.to_user : inv.from_user
          const partnerName = captainMap[partnerId] || 'Bilinmeyen Kaptan'
          
          convns.push({
            room_id: inv.room_id,
            partnerId,
            partnerName
          })
        })
        
        setConversations(convns)
      }
    }

    loadConversations()
  }, [])

  useEffect(() => {
    if (activeRoom) {
      const loadMessages = async (room_id) => {
        const { data } = await supabase.from('messages').select('*').eq('room_id', room_id).order('created_at', { ascending: true })
        if (data) setMessages(data)
      }

      loadMessages(activeRoom)
      
      // Realtime subscription
      const channel = supabase
        .channel(`room_${activeRoom}`)
        .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'messages', filter: `room_id=eq.${activeRoom}` }, payload => {
          setMessages(prev => [...prev, payload.new])
        })
        .subscribe()

      return () => {
        supabase.removeChannel(channel)
      }
    }
  }, [activeRoom])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async (e) => {
    e.preventDefault()
    if (!newMessage.trim() || !user || !activeRoom) return
    
    const msg = newMessage.trim()
    setNewMessage('')
    
    const { error } = await supabase.from('messages').insert({
      room_id: activeRoom,
      sender: user.id,
      message: msg
    })
    if (error) alert("Mesaj iletilemedi: " + error.message)
  }

  const formatTime = (ts) => {
    return new Date(ts).toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })
  }

  if (activeRoom) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 100px)' }}>
        <div style={{ marginBottom: '16px', marginTop: '8px' }}>
          <button className="btn-secondary" style={{ width: 'auto', padding: '8px 16px', fontSize: '13px', borderRadius: '12px' }} onClick={() => setActiveRoom(null)}>
            ← Frekanstan Çık
          </button>
        </div>
        
        <div className="chat-container" style={{ flex: 1 }}>
          <div className="chat-header">
            <span style={{ fontWeight: 700, fontSize: '18px', color: '#f8fafc', display: 'flex', alignItems: 'center', gap: '8px' }}>
              🛳️ {activePartner}
            </span>
            <span style={{ fontSize: '12px', color: '#38bdf8', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span className="pulsing-dot" style={{width:'8px', height:'8px'}}></span>
              Şifreli Hat Aktif
            </span>
          </div>
          
          <div className="chat-messages" style={{ flex: 1 }}>
            {messages.length === 0 ? (
              <div style={{ textAlign: 'center', color: '#64748b', marginTop: 'auto', marginBottom: 'auto', fontStyle: 'italic' }}>
                Bağlantı sağlandı. İletişime geçebilirsiniz.
              </div>
            ) : (
              messages.map(m => {
                const isMe = m.sender === user?.id
                return (
                  <div key={m.id} className={`chat-bubble ${isMe ? 'me' : 'other'}`}>
                    <div>{m.message}</div>
                    <div style={{ fontSize: '10px', opacity: 0.6, textAlign: 'right', marginTop: '6px', fontWeight: 500 }}>{formatTime(m.created_at)}</div>
                  </div>
                )
              })
            )}
            <div ref={messagesEndRef} />
          </div>
          
          <form className="chat-input-wrap" onSubmit={sendMessage}>
            <input 
              className="input-field" 
              style={{ margin: 0, background: 'rgba(30, 41, 59, 0.8)' }} 
              placeholder="Mesaj gönder..." 
              value={newMessage}
              onChange={e => setNewMessage(e.target.value)}
            />
            <button className="btn-primary" type="submit" style={{ width: 'auto', borderRadius: '14px', padding: '0 20px' }}>Gönder</button>
          </form>
        </div>
      </div>
    )
  }

  return (
    <div>
      <div className="section-title" style={{ marginTop: '16px' }}>💬 Aktif Frekanslar</div>
      {conversations.length === 0 ? (
        <div style={{ color: '#64748b', fontSize: '14px', fontStyle: 'italic', background: 'rgba(15, 23, 42, 0.4)', padding: '20px', borderRadius: '16px', border: '1px dashed rgba(71, 85, 105, 0.5)', textAlign: 'center' }}>
          Sinyal alanında aktif güvenli frekans yok.<br/>Harita üzerinden radarınızdaki gemilere koordinat daveti gönderin.
        </div>
      ) : (
        conversations.map(c => (
           <div key={c.room_id} className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px 20px' }}>
             <div>
               <div style={{ fontWeight: 700, fontSize: '16px', color: '#f8fafc' }}>🛳️ {c.partnerName}</div>
               <div style={{ fontSize: '12px', color: '#38bdf8', marginTop: '4px', letterSpacing: '0.05em' }}>FREKANS: {c.room_id.split('-')[0].toUpperCase()}</div>
             </div>
             <button className="btn-primary" style={{ width: 'auto', padding: '0.6rem 1.4rem' }} onClick={() => { setActiveRoom(c.room_id); setActivePartner(c.partnerName); }}>Hatta Gir</button>
           </div>
        ))
      )}
    </div>
  )
}
