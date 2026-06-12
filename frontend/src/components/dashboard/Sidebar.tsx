'use client';

import { useRouter, usePathname } from 'next/navigation'
import Link from 'next/link'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { makeLogoutUseCase } from '@/infrastructure/di/factories'
import { useCallback, useEffect, useState } from 'react'

const navItems = [
  { id: 'dashboard', label: 'Dashboard', icon: '▦', href: '/dashboard' },
  { id: 'torre', label: 'Torre de Controle', icon: '🗼', href: '/control-tower' },
  { id: 'agendamentos', label: 'Agendamentos', icon: '📅', href: '#' },
  { id: 'entregas', label: 'Entregas', icon: '📦', href: '#' },
  { id: 'inventario', label: 'Inventário', icon: '📋', href: '#' },
]

export function Sidebar() {
  const router = useRouter()
  const pathname = usePathname()
  const [email, setEmail] = useState('')

  useEffect(() => {
    setEmail(localStorage.getItem('user_email') || 'Operador Industrial')
  }, [])

  const handleLogout = useCallback(async () => {
    const logout = makeLogoutUseCase()
    await logout.execute()
    router.push('/')
  }, [router])

  return (
    <aside className="w-64 border-r border-slate-200 bg-white flex flex-col h-screen sticky top-0 shrink-0">
      <div className="p-6 flex items-center gap-3">
        <div className="w-10 h-10 bg-[#ec5b13] rounded-lg flex items-center justify-center text-white">
          <span className="text-lg font-bold">A</span>
        </div>
        <div>
          <h1 className="text-lg font-bold leading-tight">AntiGravity</h1>
          <p className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold">Industrial Hub</p>
        </div>
      </div>

      <nav className="flex-1 px-4 space-y-1 mt-4">
        {navItems.map((item) => {
          const isActive = item.href !== '#' && pathname === item.href
          return (
            <Link
              key={item.id}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors ${
                isActive
                  ? 'bg-[#ec5b13]/10 text-[#ec5b13] font-medium'
                  : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              <span className="text-lg">{item.icon}</span>
              <span>{item.label}</span>
            </Link>
          )
        })}
      </nav>

      <div className="p-4 border-t border-slate-200">
        <a
          href="#"
          className="flex items-center gap-3 px-3 py-2 rounded-lg text-slate-600 hover:bg-slate-100 transition-colors text-sm"
          onClick={(e) => { e.preventDefault(); handleLogout() }}
        >
          <span className="text-lg">🚪</span>
          <span>Sair</span>
        </a>
        <div className="mt-4 flex items-center gap-3 px-3 py-2">
          <Avatar className="h-8 w-8">
            <AvatarFallback className="text-xs bg-slate-200 text-slate-700">
              {email.charAt(0).toUpperCase()}
            </AvatarFallback>
          </Avatar>
          <div className="text-xs">
            <p className="font-bold text-slate-800">{email}</p>
            <p className="text-slate-500">Unidade SP-01</p>
          </div>
        </div>
      </div>
    </aside>
  )
}
