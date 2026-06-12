'use client';

import { useRouter } from 'next/navigation'
import { useCallback } from 'react'
import { makeLogoutUseCase } from '@/infrastructure/di/factories'

export function ControlTowerHeader() {
  const router = useRouter()

  const handleLogout = useCallback(async () => {
    const logout = makeLogoutUseCase()
    await logout.execute()
    router.push('/')
  }, [router])

  return (
    <header className="sticky top-0 z-10 flex items-center justify-between border-b border-slate-200 bg-white/80 backdrop-blur-md px-6 py-3">
      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2 text-[#ec5b13]">
          <h2 className="text-xl font-bold tracking-tight text-slate-900 uppercase italic">
            Torre de Controle
          </h2>
        </div>
        <div className="hidden md:flex items-center gap-4 bg-slate-100 px-3 py-1.5 rounded-lg border border-slate-200">
          <span className="text-slate-400 text-sm">🔍</span>
          <input
            className="bg-transparent border-none focus:outline-none text-sm w-64 placeholder-slate-400"
            placeholder="Buscar veículo ou planta..."
            type="text"
          />
        </div>
      </div>
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 text-xs font-mono px-3 py-1 bg-slate-100 rounded border border-slate-200">
          <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
          SISTEMA OPERACIONAL
        </div>
        <button className="p-2 hover:bg-slate-100 rounded-lg transition-colors text-slate-600">
          🔔
        </button>
        <button
          onClick={handleLogout}
          className="text-xs text-slate-400 hover:text-slate-600 transition-colors"
        >
          Sair
        </button>
      </div>
    </header>
  )
}
