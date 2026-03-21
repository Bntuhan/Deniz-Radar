import { useState } from 'react'
import { supabase } from '../lib/supabase'

export default function Auth() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLogin, setIsLogin] = useState(true)
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  const handleAuth = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')
    
    try {
      if (isLogin) {
        const { error } = await supabase.auth.signInWithPassword({ email, password })
        if (error) throw error
      } else {
        const { error } = await supabase.auth.signUp({ email, password })
        if (error) throw error
        setMessage('Kayıt başarılı! Lütfen e-postanızı kontrol edin.')
      }
    } catch (error) {
      setMessage(error.message || 'Bir hata oluştu')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card" style={{ marginTop: '2rem', width: '100%', maxWidth: '400px' }}>
      <div style={{ textAlign: 'center', marginBottom: '28px' }}>
        <h1 className="text-gradient" style={{ fontSize: '2.8rem', marginBottom: '8px' }}>Deniz Radar</h1>
        <p style={{ margin: 0, fontSize: '15px' }}>Kaptanların güvenli iletişim ağı.</p>
      </div>
      
      <div style={{ display: 'flex', gap: '8px', marginBottom: '24px' }}>
        <button className={isLogin ? 'btn-primary' : 'btn-secondary'} onClick={() => setIsLogin(true)}>Giriş Yap</button>
        <button className={!isLogin ? 'btn-primary' : 'btn-secondary'} onClick={() => setIsLogin(false)}>Kayıt Ol</button>
      </div>

      <form onSubmit={handleAuth}>
        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', marginBottom: '8px' }}>Email Adresi</label>
          <input 
            type="email" 
            className="input-field" 
            placeholder="kaptan@ornek.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required 
          />
        </div>
        <div style={{ marginBottom: '24px' }}>
          <label style={{ display: 'block', marginBottom: '8px' }}>Şifre</label>
          <input 
            type="password" 
            className="input-field" 
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required 
          />
        </div>
        
        {message && (
          <div style={{ padding: '14px', borderRadius: '14px', background: 'rgba(239, 68, 68, 0.1)', color: '#f87171', marginBottom: '20px', fontSize: '14px', border: '1px solid rgba(239, 68, 68, 0.3)' }}>
            {message}
          </div>
        )}
        
        <button type="submit" className="btn-primary" disabled={loading} style={{ padding: '1rem', fontSize: '16px' }}>
          {loading ? 'Sinyal Gönderiliyor...' : (isLogin ? 'Sisteme Bağlan' : 'Radara Katıl')}
        </button>
      </form>
    </div>
  )
}
