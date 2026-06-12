'use client';

import { useState } from 'react'

const quickEvents = [
  { icon: '⛈️', title: 'Tempestade Severa', desc: 'Bloqueio imediato de portos' },
  { icon: '🏭', title: 'Parada de Linha', desc: 'Gargalo em Curitiba/PR' },
  { icon: '💰', title: 'Alta Diesel +15%', desc: 'Recalcular margem de lucro' },
] as const

export function SimuladorCaos() {
  const [logs, setLogs] = useState<string[]>([])

  const trigger = (event: string) => {
    setLogs((prev) => [`[Caos] ${event} — ${new Date().toLocaleTimeString('pt-BR')}`, ...prev])
  }

  return (
    <aside className="w-80 bg-slate-50 border-l border-slate-200 flex flex-col h-full shrink-0">
      <div className="p-6 border-b border-slate-200 bg-white">
        <h3 className="text-sm font-bold flex items-center gap-2">
          ⚡ Simulador de Caos
        </h3>
        <p className="text-xs text-slate-500 mt-1 italic">Stress-test operacional em tempo real</p>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        <div>
          <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-3">Eventos Rápidos</h4>
          <div className="grid grid-cols-1 gap-2">
            {quickEvents.map((e) => (
              <button
                key={e.title}
                onClick={() => trigger(e.title)}
                className="flex items-center gap-3 p-3 bg-white rounded-lg border border-slate-200 hover:border-[#ec5b13] transition-all group text-left"
              >
                <span className="text-slate-400 group-hover:text-[#ec5b13]">{e.icon}</span>
                <div>
                  <p className="text-xs font-bold">{e.title}</p>
                  <p className="text-[10px] text-slate-500">{e.desc}</p>
                </div>
              </button>
            ))}
          </div>
        </div>

        <div>
          <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-3">Nível de Contingência</h4>
          <div className="space-y-4">
            <div className="flex justify-between items-center text-xs">
              <span>Nível Atual</span>
              <span className="font-mono text-[#ec5b13] font-bold">CRITICAL_S2</span>
            </div>
            <div className="h-2 bg-slate-200 rounded-full overflow-hidden">
              <div className="h-full bg-gradient-to-r from-green-500 via-amber-500 to-red-500 w-[75%]" />
            </div>
          </div>
        </div>

        <div className="bg-slate-900 text-white p-4 rounded-xl space-y-3">
          <p className="text-[10px] font-mono text-[#ec5b13] flex items-center gap-1">
            🤖 PREVISÃO_IA
          </p>
          <p className="text-xs leading-relaxed">
            Probabilidade de 64% de atraso na malha Sudeste nas próximas 4h devido a condições climáticas.
          </p>
          <button className="w-full py-2 bg-slate-800 text-[10px] font-bold uppercase rounded border border-white/10 hover:bg-slate-700 flex items-center justify-center gap-1">
            🛣️ Ativar Plano B
          </button>
        </div>

        {logs.length > 0 && (
          <div>
            <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-2">Log</h4>
            <div className="space-y-1">
              {logs.map((log, i) => (
                <div key={i} className="text-[10px] font-mono text-red-500">{log}</div>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="p-4 border-t border-slate-200 bg-white">
        <button
          onClick={() => trigger('SIMULAÇÃO_EXECUTADA')}
          className="w-full flex items-center justify-center gap-2 py-3 bg-slate-900 text-white rounded-lg font-bold text-sm hover:bg-black transition-all"
        >
          🚀 EXECUTAR SIMULAÇÃO
        </button>
      </div>
    </aside>
  )
}
