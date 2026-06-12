'use client';

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'

export function JanelaRecebimento() {
  const [startTime, setStartTime] = useState('08:00')
  const [endTime, setEndTime] = useState('18:00')
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    const savedStart = localStorage.getItem('janela_inicio')
    const savedEnd = localStorage.getItem('janela_termino')
    if (savedStart) setStartTime(savedStart)
    if (savedEnd) setEndTime(savedEnd)
  }, [])

  const handleUpdate = () => {
    localStorage.setItem('janela_inicio', startTime)
    localStorage.setItem('janela_termino', endTime)
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
  }

  return (
    <header className="bg-white border-b border-slate-200 p-6">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Configurar Janela de Recebimento</h2>
          <p className="text-sm text-slate-500">Defina o período operacional para o fluxo de cargas de hoje.</p>
        </div>
        <div className="flex items-center gap-4 bg-slate-50 p-2 rounded-xl border border-slate-100">
          <div className="flex flex-col px-3">
            <span className="text-[10px] uppercase font-bold text-slate-400">Início</span>
            <input
              type="time"
              value={startTime}
              onChange={(e) => setStartTime(e.target.value)}
              className="bg-transparent border-none p-0 text-sm font-semibold focus:outline-none text-slate-700"
            />
          </div>
          <div className="h-8 w-px bg-slate-200" />
          <div className="flex flex-col px-3">
            <span className="text-[10px] uppercase font-bold text-slate-400">Término</span>
            <input
              type="time"
              value={endTime}
              onChange={(e) => setEndTime(e.target.value)}
              className="bg-transparent border-none p-0 text-sm font-semibold focus:outline-none text-slate-700"
            />
          </div>
          <Button
            className="bg-[#ec5b13] hover:bg-[#ec5b13]/90 text-white shadow-sm shadow-[#ec5b13]/20"
            size="sm"
            onClick={handleUpdate}
          >
            {saved ? 'Atualizado ✓' : 'Atualizar Janela'}
          </Button>
        </div>
      </div>
    </header>
  )
}
