import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { CriarEntregaDialog } from './CriarEntregaDialog';
import { usePlaces } from '@/hooks/usePlaces';
import { useUsers } from '@/hooks/useUsers';
import { useDeliveries } from '@/hooks/useDeliveries';
import { Factory, Store } from '@/domain/entities/Place';
import { Coordinates } from '@/domain/value_objects/Coordinates';
import { User } from '@/domain/entities/User';
import { AppError } from '@/domain/errors/AppError';

vi.mock('@/hooks/usePlaces');
vi.mock('@/hooks/useUsers');
vi.mock('@/hooks/useDeliveries');

describe('CriarEntregaDialog', () => {
  let mockListFactories: ReturnType<typeof vi.fn>;
  let mockListStores: ReturnType<typeof vi.fn>;
  let mockFetchDrivers: ReturnType<typeof vi.fn>;
  let mockCreateDelivery: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    vi.clearAllMocks();
    mockListFactories = vi.fn();
    mockListStores = vi.fn();
    mockFetchDrivers = vi.fn();
    mockCreateDelivery = vi.fn();

    vi.mocked(usePlaces).mockReturnValue({
      factories: [],
      stores: [],
      listFactories: mockListFactories,
      listStores: mockListStores,
      isLoading: false,
      error: '',
      createFactory: vi.fn(),
      createStore: vi.fn(),
    });

    vi.mocked(useUsers).mockReturnValue({
      drivers: [],
      fetchDrivers: mockFetchDrivers,
      isLoading: false,
      error: '',
    });

    vi.mocked(useDeliveries).mockReturnValue({
      createDelivery: mockCreateDelivery,
      isLoading: false,
      error: '',
      deliveries: [],
      fetchDeliveries: vi.fn(),
      updateDeliveryStatus: vi.fn(),
    });
  });

  it('deve renderizar o dialogo quando open=true', () => {
    render(<CriarEntregaDialog open={true} onOpenChange={vi.fn()} />);
    expect(screen.getByText('Nova Entrega')).toBeInTheDocument();
    expect(screen.getByText(/Preencha os campos/)).toBeInTheDocument();
  });

  it('deve chamar listFactories, listStores e fetchDrivers ao abrir', () => {
    render(<CriarEntregaDialog open={true} onOpenChange={vi.fn()} />);
    expect(mockListFactories).toHaveBeenCalledOnce();
    expect(mockListStores).toHaveBeenCalledOnce();
    expect(mockFetchDrivers).toHaveBeenCalledOnce();
  });

  it('nao deve renderizar conteudo quando open=false', () => {
    render(<CriarEntregaDialog open={false} onOpenChange={vi.fn()} />);
    expect(screen.queryByText('Nova Entrega')).not.toBeInTheDocument();
  });

  it('deve desativar botao criar quando nenhum campo selecionado', () => {
    render(<CriarEntregaDialog open={true} onOpenChange={vi.fn()} />);
    const criarButton = screen.getByRole('button', { name: /criar/i });
    expect(criarButton).toBeDisabled();
  });

  it('deve criar entrega com sucesso', async () => {
    const fakeFactory = new Factory(
      { name: 'Fabrica 1', location: new Coordinates({ lat: -23, lng: -46 }) },
      'fac1',
    );
    const fakeStore = new Store(
      { name: 'Loja 1', location: new Coordinates({ lat: -23, lng: -46 }), ownerId: 'own1' },
      'sto1',
    );
    const fakeDriver = new User({ email: 'driver@test.com', role: 'motorista' }, 'drv1');

    vi.mocked(usePlaces).mockReturnValue({
      factories: [fakeFactory],
      stores: [fakeStore],
      listFactories: mockListFactories,
      listStores: mockListStores,
      isLoading: false,
      error: '',
      createFactory: vi.fn(),
      createStore: vi.fn(),
    });

    vi.mocked(useUsers).mockReturnValue({
      drivers: [fakeDriver],
      fetchDrivers: mockFetchDrivers,
      isLoading: false,
      error: '',
    });

    mockCreateDelivery.mockResolvedValue({ id: 'del1' });

    const onOpenChange = vi.fn();
    render(<CriarEntregaDialog open={true} onOpenChange={onOpenChange} />);

    fireEvent.click(screen.getByRole('button', { name: /selecione uma fábrica/i }));
    fireEvent.click(screen.getByText('Fabrica 1'));

    fireEvent.click(screen.getByRole('button', { name: /selecione uma loja/i }));
    fireEvent.click(screen.getByText('Loja 1'));

    fireEvent.click(screen.getByRole('button', { name: /selecione um motorista/i }));
    fireEvent.click(screen.getByText('driver@test.com'));

    fireEvent.click(screen.getByRole('button', { name: /criar/i }));

    await waitFor(() => {
      expect(mockCreateDelivery).toHaveBeenCalledWith('fac1', 'sto1', 'drv1');
    });

    await waitFor(() => {
      expect(onOpenChange).toHaveBeenCalledWith(false);
    });
  });

  it('deve exibir erro quando createDelivery falha', async () => {
    const fakeFactory = new Factory(
      { name: 'Fabrica 1', location: new Coordinates({ lat: -23, lng: -46 }) },
      'fac1',
    );
    const fakeStore = new Store(
      { name: 'Loja 1', location: new Coordinates({ lat: -23, lng: -46 }), ownerId: 'own1' },
      'sto1',
    );
    const fakeDriver = new User({ email: 'driver@test.com', role: 'motorista' }, 'drv1');

    vi.mocked(usePlaces).mockReturnValue({
      factories: [fakeFactory],
      stores: [fakeStore],
      listFactories: mockListFactories,
      listStores: mockListStores,
      isLoading: false,
      error: '',
      createFactory: vi.fn(),
      createStore: vi.fn(),
    });

    vi.mocked(useUsers).mockReturnValue({
      drivers: [fakeDriver],
      fetchDrivers: mockFetchDrivers,
      isLoading: false,
      error: '',
    });

    mockCreateDelivery.mockRejectedValue(new AppError('Erro ao criar entrega.'));

    render(<CriarEntregaDialog open={true} onOpenChange={vi.fn()} />);

    fireEvent.click(screen.getByRole('button', { name: /selecione uma fábrica/i }));
    fireEvent.click(screen.getByText('Fabrica 1'));

    fireEvent.click(screen.getByRole('button', { name: /selecione uma loja/i }));
    fireEvent.click(screen.getByText('Loja 1'));

    fireEvent.click(screen.getByRole('button', { name: /selecione um motorista/i }));
    fireEvent.click(screen.getByText('driver@test.com'));

    fireEvent.click(screen.getByRole('button', { name: /criar/i }));

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent('Erro ao criar entrega.');
    });
  });

  it('deve mostrar Criando... durante o submit', async () => {
    const fakeFactory = new Factory(
      { name: 'Fabrica 1', location: new Coordinates({ lat: -23, lng: -46 }) },
      'fac1',
    );
    const fakeStore = new Store(
      { name: 'Loja 1', location: new Coordinates({ lat: -23, lng: -46 }), ownerId: 'own1' },
      'sto1',
    );
    const fakeDriver = new User({ email: 'driver@test.com', role: 'motorista' }, 'drv1');

    vi.mocked(usePlaces).mockReturnValue({
      factories: [fakeFactory],
      stores: [fakeStore],
      listFactories: mockListFactories,
      listStores: mockListStores,
      isLoading: false,
      error: '',
      createFactory: vi.fn(),
      createStore: vi.fn(),
    });

    vi.mocked(useUsers).mockReturnValue({
      drivers: [fakeDriver],
      fetchDrivers: mockFetchDrivers,
      isLoading: false,
      error: '',
    });

    vi.mocked(useDeliveries).mockReturnValue({
      createDelivery: mockCreateDelivery,
      isLoading: true,
      error: '',
      deliveries: [],
      fetchDeliveries: vi.fn(),
      updateDeliveryStatus: vi.fn(),
    });

    mockCreateDelivery.mockResolvedValue({ id: 'del1' });

    render(<CriarEntregaDialog open={true} onOpenChange={vi.fn()} />);

    fireEvent.click(screen.getByRole('button', { name: /selecione uma fábrica/i }));
    fireEvent.click(screen.getByText('Fabrica 1'));

    fireEvent.click(screen.getByRole('button', { name: /selecione uma loja/i }));
    fireEvent.click(screen.getByText('Loja 1'));

    fireEvent.click(screen.getByRole('button', { name: /selecione um motorista/i }));
    fireEvent.click(screen.getByText('driver@test.com'));

    const criarButton = screen.getByRole('button', { name: /criando/i });
    expect(criarButton).toBeDisabled();
  });
});
