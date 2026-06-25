import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { AlertList } from './AlertList';
import { Alert } from '@/domain/entities/Alert';

describe('AlertList', () => {
  const criticalAlert = new Alert(
    { deliveryId: 'del1', message: 'Atraso crítico', isCritical: true, createdAt: new Date() },
    'alert1',
  );

  const infoAlert = new Alert(
    { deliveryId: 'del2', message: 'Alerta informativo', isCritical: false, createdAt: new Date() },
    'alert2',
  );

  it('deve mostrar loading quando isLoading é true', () => {
    render(<AlertList alerts={[]} isLoading={true} error="" />);
    expect(screen.getByText('Carregando alertas...')).toBeTruthy();
  });

  it('deve mostrar erro quando error não é vazio', () => {
    render(<AlertList alerts={[]} isLoading={false} error="Erro de rede" />);
    expect(screen.getByText('Erro de rede')).toBeTruthy();
  });

  it('deve mostrar mensagem quando não há alertas', () => {
    render(<AlertList alerts={[]} isLoading={false} error="" />);
    expect(screen.getByText('Nenhum alerta registrado.')).toBeTruthy();
  });

  it('deve renderizar alertas críticos e normais', () => {
    render(<AlertList alerts={[criticalAlert, infoAlert]} isLoading={false} error="" />);

    expect(screen.getByText('Atraso crítico')).toBeTruthy();
    expect(screen.getByText('Alerta informativo')).toBeTruthy();
  });

  it('deve aplicar classe visual diferente para alertas críticos', () => {
    render(<AlertList alerts={[criticalAlert]} isLoading={false} error="" />);

    const container = screen.getByText('Atraso crítico').closest('.bg-red-50');
    expect(container).toBeTruthy();
  });

  it('deve aplicar classe visual diferente para alertas normais', () => {
    render(<AlertList alerts={[infoAlert]} isLoading={false} error="" />);

    const container = screen.getByText('Alerta informativo').closest('.bg-amber-50');
    expect(container).toBeTruthy();
  });

  it('deve exibir a data de criação formatada', () => {
    const fixedDate = new Date('2026-06-25T10:00:00Z');
    const alert = new Alert(
      { deliveryId: 'del1', message: 'Teste', isCritical: false, createdAt: fixedDate },
      'alert1',
    );

    render(<AlertList alerts={[alert]} isLoading={false} error="" />);

    expect(screen.getByText(fixedDate.toLocaleString('pt-BR'))).toBeTruthy();
  });
});
