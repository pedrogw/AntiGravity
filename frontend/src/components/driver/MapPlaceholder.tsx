'use client';

import { Delivery } from '@/domain/entities/Delivery'

interface Props {
  delivery: Delivery
}

export function MapPlaceholder({ delivery }: Props) {
  const lat = delivery.currentLat?.toFixed(4) || '-23.5505'
  const lng = delivery.currentLng?.toFixed(4) || '-46.6333'

  return (
    <div className="w-full h-48 bg-slate-100 rounded-2xl overflow-hidden relative">
      <div className="absolute inset-0 bg-gradient-to-br from-slate-200 to-slate-300 flex items-center justify-center">
        <div className="text-center text-slate-400">
          <div className="text-3xl mb-1">🗺️</div>
          <div className="text-xs font-mono">{lat}, {lng}</div>
        </div>
      </div>
      <div className="absolute bottom-4 left-4 bg-white/90 px-3 py-1 rounded-full text-xs font-bold shadow-sm">
        BR-116 Km 244
      </div>
    </div>
  )
}
