import { FormEvent, useEffect, useState } from 'react';
import { Activity, ArrowLeft, ArrowRight, Eye, EyeOff, ShieldCheck } from 'lucide-react';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';
type Props = { onLogin: (token: string) => void };
export default function Auth({ onLogin }: Props) {
  const [mode,setMode]=useState<'login'|'register'|'forgot'|'reset'>('login');
  const [name,setName]=useState(''); const [email,setEmail]=useState(''); const [password,setPassword]=useState('');
  const [confirm,setConfirm]=useState(''); const [show,setShow]=useState(false);
  const [message,setMessage]=useState(''); const [error,setError]=useState(''); const [busy,setBusy]=useState(false);
  const [resetToken,setResetToken]=useState('');
  useEffect(()=>{const params=new URLSearchParams(window.location.search);const verify=params.get('verify');const reset=params.get('reset');
    if(verify){setBusy(true);fetch(API+'/api/auth/verify-email',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({token:verify})}).then(async r=>{const d=await r.json();if(!r.ok)throw Error(d.detail||'Verification failed');setMessage(d.message);}).catch(e=>setError(e.message)).finally(()=>{setBusy(false);window.history.replaceState({},'',window.location.pathname);});}
    if(reset){setResetToken(reset);setMode('reset');window.history.replaceState({},'',window.location.pathname);}
  },[]);
  async function submit(e:FormEvent){e.preventDefault();setError('');setMessage('');
    if(mode==='register'&&password.length<10){setError('Use at least 10 characters for your password.');return;}
    if(mode==='reset'&&password!==confirm){setError('Your passwords do not match.');return;}
    setBusy(true);
    try{
      let endpoint='',body:any={};
      if(mode==='register'){endpoint='/api/auth/register';body={full_name:name,email,password};}
      if(mode==='login'){endpoint='/api/auth/login';body={email,password};}
      if(mode==='forgot'){endpoint='/api/auth/password-reset/request';body={email};}
      if(mode==='reset'){endpoint='/api/auth/password-reset/confirm';body={token:resetToken,new_password:password};}
      const response=await fetch(API+endpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
      const data=await response.json();if(!response.ok)throw Error(data.detail||'Something went wrong. Please try again.');
      if(mode==='login'){onLogin(data.access_token);return;}
      setMessage(data.message);if(mode==='register'||mode==='reset'){setMode('login');setPassword('');setConfirm('');}
    }catch(e){setError(e instanceof Error?e.message:'Unable to connect to the academy.');}finally{setBusy(false);}
  }
  const title=mode==='register'?'Create your student account':mode==='forgot'?'Reset your password':mode==='reset'?'Choose a new password':'Welcome back';
  const subtitle=mode==='register'?'Start building your forex knowledge, one lesson at a time.':mode==='forgot'?'Enter your account email and we will send reset instructions.':mode==='reset'?'Choose a strong password you have not used before.':'Sign in to continue your learning journey.';
  return <div className="auth-page"><div className="auth-brand"><div className="auth-mark"><Activity/></div><div><b>LEARNING FOREX</b><small>ACADEMY</small></div></div><div className="auth-layout"><div className="auth-story"><span className="auth-kicker">LEARN WITH PURPOSE</span><h1>Build knowledge.<br/><em>Trade with awareness.</em></h1><p>A structured learning space for understanding the forex market, developing chart-reading skills and tracking your progress.</p><div className="auth-points"><span><ShieldCheck/> Learn at your own pace</span><span><ShieldCheck/> Secure student account</span><span><ShieldCheck/> Education before execution</span></div><small className="auth-disclaimer">Forex trading involves substantial risk. Education does not guarantee trading profits.</small></div><div className="auth-card"><div className="auth-card-top"><span>STUDENT PORTAL</span><span className="secure-pill"><ShieldCheck size={14}/> SECURE ACCESS</span></div><h2>{title}</h2><p className="auth-subtitle">{subtitle}</p>{message&&<div className="notice success">{message}</div>}{error&&<div className="notice error">{error}</div>}{busy&&<div className="notice">Please wait…</div>}<form onSubmit={submit}>{mode==='register'&&<label>Full name<input value={name} onChange={e=>setName(e.target.value)} placeholder="Your full name" autoComplete="name" required minLength={2}/></label>}{mode!=='reset'&&<label>Email address<input type="email" value={email} onChange={e=>setEmail(e.target.value)} placeholder="you@example.com" autoComplete="email" required/></label>}{mode!=='forgot'&&<label>{mode==='reset'?'New password':'Password'}<div className="password-field"><input type={show?'text':'password'} value={password} onChange={e=>setPassword(e.target.value)} placeholder={mode==='login'?'Enter your password':'At least 10 characters'} autoComplete={mode==='login'?'current-password':'new-password'} required minLength={mode==='login'?1:10}/><button type="button" onClick={()=>setShow(!show)} aria-label="Toggle password visibility">{show?<EyeOff/>:<Eye/>}</button></div></label>}{mode==='reset'&&<label>Confirm new password<input type="password" value={confirm} onChange={e=>setConfirm(e.target.value)} placeholder="Re-enter new password" required minLength={10}/></label>}{mode==='login'&&<div className="form-options"><span>Use your verified email to sign in</span><button type="button" onClick={()=>{setMode('forgot');setError('');setMessage('');}}>Forgot password?</button></div>}<button className="auth-submit" disabled={busy}>{busy?'Please wait…':mode==='register'?'Create account':mode==='forgot'?'Send reset instructions':mode==='reset'?'Update password':'Sign in'} <ArrowRight size={16}/></button></form><div className="auth-switch">{mode==='login'?<>New to the academy? <button onClick={()=>{setMode('register');setError('');setMessage('');}}>Create an account</button></>:mode==='register'?<>Already registered? <button onClick={()=>setMode('login')}>Sign in</button></>:<button onClick={()=>{setMode('login');setError('');setMessage('');}}><ArrowLeft size={14}/> Back to sign in</button>}</div>{mode==='register'&&<small className="password-hint">Passwords must contain at least 10 characters.</small>}</div></div><footer className="auth-footer">© 2026 Learning Forex Academy <span>Privacy · Terms · Support</span></footer></div>;
}
