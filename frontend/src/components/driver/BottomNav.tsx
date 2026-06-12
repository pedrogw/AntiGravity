'use client';

const tabs = [
  { id: 'entrega', label: 'Entrega', icon: '🚛', active: true },
  { id: 'mapa', label: 'Mapa', icon: '🗺️', active: false },
  { id: 'perfil', label: 'Perfil', icon: '👤', active: false },
]

export function BottomNav() {
  return (
    <nav className="sticky bottom-0 w-full bg-white/80 backdrop-blur-lg border-t border-slate-200 px-6 pb-8 pt-4">
      <div className="flex justify-between items-center max-w-md mx-auto">
        {tabs.map((tab) => (
          <a
            key={tab.id}
            href="#"
            className={`flex flex-col items-center gap-1 group ${
              tab.active ? 'text-[#ec5b13]' : 'text-slate-400'
            }`}
          >
            <div
              className={`flex h-10 w-10 items-center justify-center rounded-2xl transition-all ${
                tab.active ? 'bg-[#ec5b13]/10' : ''
              }`}
            >
              <span className="text-lg">{tab.icon}</span>
            </div>
            <p className="text-[10px] font-bold uppercase tracking-wider">{tab.label}</p>
          </a>
        ))}
      </div>
    </nav>
  )
}
