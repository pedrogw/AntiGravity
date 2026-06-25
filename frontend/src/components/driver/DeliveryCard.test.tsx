import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { DeliveryCard } from './DeliveryCard';
import { DeliveryStatus } from '@/domain/DeliveryStatus';
import { Delivery } from '@/domain/entities/Delivery';

function makeDelivery(overrides: Partial<{ status: DeliveryStatus; id: string }> = {}): Delivery {
  return new Delivery(
    {
      factoryId: '00000000-0000-0000-0000-000000000001',
      storeId: '00000000-0000-0000-0000-000000000002',
      driverId: '00000000-0000-0000-0000-000000000003',
      status: overrides.status || 'pendente',
    },
    overrides.id || 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
  );
}

describe('DeliveryCard', () => {
  it('mostra "Aceitar Oferta" quando status é pendente', () => {
    render(
      <DeliveryCard
        delivery={makeDelivery({ status: 'pendente' })}
        onAccept={vi.fn()}
        onStartRoute={vi.fn()}
        onComplete={vi.fn()}
        onReportProblem={vi.fn()}
      />,
    );
    expect(screen.getByText('Aceitar Oferta')).toBeInTheDocument();
  });

  it('mostra "Iniciar Rota" quando status é aceita', () => {
    render(
      <DeliveryCard
        delivery={makeDelivery({ status: 'aceita' })}
        onAccept={vi.fn()}
        onStartRoute={vi.fn()}
        onComplete={vi.fn()}
        onReportProblem={vi.fn()}
      />,
    );
    expect(screen.getByText('Iniciar Rota')).toBeInTheDocument();
  });

  it('mostra "Concluir Entrega" quando status é em_transito e onComplete existe', () => {
    render(
      <DeliveryCard
        delivery={makeDelivery({ status: 'em_transito' })}
        onAccept={vi.fn()}
        onStartRoute={vi.fn()}
        onComplete={vi.fn()}
        onReportProblem={vi.fn()}
      />,
    );
    expect(screen.getByText('Concluir Entrega')).toBeInTheDocument();
  });

  it('chama onAccept ao clicar em "Aceitar Oferta"', () => {
    const onAccept = vi.fn();
    const delivery = makeDelivery({ status: 'pendente' });
    render(
      <DeliveryCard
        delivery={delivery}
        onAccept={onAccept}
        onStartRoute={vi.fn()}
        onComplete={vi.fn()}
        onReportProblem={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByText('Aceitar Oferta'));
    expect(onAccept).toHaveBeenCalledTimes(1);
    expect(onAccept).toHaveBeenCalledWith(delivery.id);
  });

  it('chama onComplete ao clicar em "Concluir Entrega"', () => {
    const onComplete = vi.fn();
    const delivery = makeDelivery({ status: 'em_transito' });
    render(
      <DeliveryCard
        delivery={delivery}
        onAccept={vi.fn()}
        onStartRoute={vi.fn()}
        onComplete={onComplete}
        onReportProblem={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByText('Concluir Entrega'));
    expect(onComplete).toHaveBeenCalledTimes(1);
    expect(onComplete).toHaveBeenCalledWith(delivery.id);
  });
});
