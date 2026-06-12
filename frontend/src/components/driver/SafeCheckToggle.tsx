'use client';

import { useState } from 'react'

export function SafeCheckToggle() {
  const [checked, setChecked] = useState(true)

  return (
    <div className="bg-white rounded-2xl p-5 flex items-center justify-between border border-slate-100 shadow-sm">
      <div className="flex items-center gap-4">
        <div className="relative">
          <div className={`w-3 h-3 rounded-full ${checked ? 'bg-green-500 pulse-animation' : 'bg-slate-300'}`} />
        </div>
        <div>
          <p className="text-base font-bold">Safe-Check</p>
          <p className="text-sm text-slate-500">
            {checked ? 'Sistema Operacional Online' : 'Safe-Check Desativado'}
          </p>
        </div>
      </div>
      <label className="relative flex h-[31px] w-[51px] cursor-pointer items-center rounded-full bg-slate-200 p-0.5 transition-colors has-[:checked]:bg-green-500">
        <div className={`h-full w-[27px] rounded-full bg-white shadow-md transition-transform ${checked ? 'translate-x-5' : 'translate-x-0'}`} />
        <input
          type="checkbox"
          checked={checked}
          onChange={(e) => setChecked(e.target.checked)}
          className="sr-only"
        />
      </label>
    </div>
  )
}
