'use client';

import { Alert } from '@/domain/entities/Alert';

interface Props {
  alerts: Alert[];
  isLoading: boolean;
  error: string;
  onDismiss?: (alertId: string) => void;
}

export function AlertList({ alerts, isLoading, error, onDismiss }: Props) {
  if (isLoading) {
    return (
      <div className="text-sm text-slate-400 py-4 text-center">
        Carregando alertas...
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-3 text-sm text-red-700 bg-red-100 rounded" role="alert">
        {error}
      </div>
    );
  }

  if (alerts.length === 0) {
    return (
      <div className="text-sm text-slate-400 py-4 text-center">
        Nenhum alerta registrado.
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {alerts.map((alert) => (
        <div
          key={alert.id}
          className={`p-3 rounded text-sm border ${
            alert.isCritical
              ? 'bg-red-50 border-red-200 text-red-800'
              : 'bg-amber-50 border-amber-200 text-amber-800'
          }`}
        >
          <div className="flex items-start gap-2">
            <span className="mt-0.5 shrink-0">{alert.isCritical ? '🔴' : '🟡'}</span>
            <div className="min-w-0 flex-1">
              <p className="font-medium">{alert.message}</p>
              <p className="text-xs opacity-70 mt-1">
                {alert.createdAt.toLocaleString('pt-BR')}
              </p>
            </div>
            {onDismiss && (
              <button
                onClick={() => onDismiss(alert.id)}
                className="shrink-0 text-xs px-2 py-1 rounded bg-white/60 hover:bg-white/90 border border-current opacity-60 hover:opacity-100 transition-opacity"
                aria-label="Dispensar alerta"
              >
                ✕
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
