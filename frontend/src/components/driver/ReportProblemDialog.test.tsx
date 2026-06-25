import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { ReportProblemDialog } from './ReportProblemDialog';

vi.mock('@/infrastructure/api/api_client', () => ({
  apiClient: {
    post: vi.fn(),
  },
}));

import { apiClient } from '@/infrastructure/api/api_client';

const mockedPost = vi.mocked(apiClient.post);

describe('ReportProblemDialog', () => {
  const deliveryId = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa';

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renderiza título e descrição quando aberto', () => {
    render(
      <ReportProblemDialog
        deliveryId={deliveryId}
        open={true}
        onOpenChange={vi.fn()}
      />,
    );
    expect(screen.getByText('Reportar Problema')).toBeInTheDocument();
    expect(screen.getByText('Selecione o tipo de problema encontrado na entrega.')).toBeInTheDocument();
  });

  it('renderiza 6 opções de problema', () => {
    render(
      <ReportProblemDialog
        deliveryId={deliveryId}
        open={true}
        onOpenChange={vi.fn()}
      />,
    );
    expect(screen.getByText('Trânsito')).toBeInTheDocument();
    expect(screen.getByText('Acidente')).toBeInTheDocument();
    expect(screen.getByText('Mecânico')).toBeInTheDocument();
    expect(screen.getByText('Clima')).toBeInTheDocument();
    expect(screen.getByText('Estrada bloqueada')).toBeInTheDocument();
    expect(screen.getByText('Outro')).toBeInTheDocument();
  });

  it('chama apiClient.post com parâmetros corretos ao clicar em Trânsito', async () => {
    mockedPost.mockResolvedValueOnce({ data: {} });
    const onOpenChange = vi.fn();
    render(
      <ReportProblemDialog
        deliveryId={deliveryId}
        open={true}
        onOpenChange={onOpenChange}
      />,
    );
    fireEvent.click(screen.getByText('Trânsito'));
    await waitFor(() => {
      expect(mockedPost).toHaveBeenCalledWith(`/deliveries/${deliveryId}/chaos`, {
        event_type: 'reporte_transito',
        delay_minutes: 15,
        impact_factor: 1.5,
      });
    });
  });

  it('chama apiClient.post com parâmetros corretos ao clicar em Acidente', async () => {
    mockedPost.mockResolvedValueOnce({ data: {} });
    render(
      <ReportProblemDialog
        deliveryId={deliveryId}
        open={true}
        onOpenChange={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByText('Acidente'));
    await waitFor(() => {
      expect(mockedPost).toHaveBeenCalledWith(`/deliveries/${deliveryId}/chaos`, {
        event_type: 'reporte_acidente',
        delay_minutes: 45,
        impact_factor: 2.5,
      });
    });
  });

  it('mostra mensagem de sucesso após submit', async () => {
    mockedPost.mockResolvedValueOnce({ data: {} });
    render(
      <ReportProblemDialog
        deliveryId={deliveryId}
        open={true}
        onOpenChange={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByText('Trânsito'));
    await waitFor(() => {
      expect(screen.getByText('Problema reportado com sucesso ✓')).toBeInTheDocument();
    });
  });

  it('mostra mensagem de erro quando API falha', async () => {
    mockedPost.mockRejectedValueOnce(new Error('Network error'));
    render(
      <ReportProblemDialog
        deliveryId={deliveryId}
        open={true}
        onOpenChange={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByText('Trânsito'));
    await waitFor(() => {
      expect(screen.getByText('Falha ao reportar problema. Tente novamente.')).toBeInTheDocument();
    });
  });

  it('desabilita botões enquanto carregando', async () => {
    mockedPost.mockResolvedValueOnce({ data: {} });
    render(
      <ReportProblemDialog
        deliveryId={deliveryId}
        open={true}
        onOpenChange={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByText('Outro'));
    expect(screen.getByText('Outro').closest('button')).toBeDisabled();
    await waitFor(() => {
      expect(screen.getByText('Problema reportado com sucesso ✓')).toBeInTheDocument();
    });
  });

  it('não renderiza nada quando fechado', () => {
    const { container } = render(
      <ReportProblemDialog
        deliveryId={deliveryId}
        open={false}
        onOpenChange={vi.fn()}
      />,
    );
    expect(container.textContent).toBe('');
  });
});
