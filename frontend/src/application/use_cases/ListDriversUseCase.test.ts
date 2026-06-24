import { describe, it, expect, vi, beforeEach } from 'vitest';
import { ListDriversUseCase } from './ListDriversUseCase';
import { UserRepositoryProtocol } from '../../domain/repositories/UserRepositoryProtocol';
import { User } from '../../domain/entities/User';

describe('ListDriversUseCase', () => {
  let mockRepo: UserRepositoryProtocol;
  let useCase: ListDriversUseCase;

  beforeEach(() => {
    mockRepo = { listDrivers: vi.fn() };
    useCase = new ListDriversUseCase(mockRepo);
  });

  it('deve listar motoristas chamando o repositorio', async () => {
    const mockUser = new User({ email: 'driver@test.com', role: 'motorista' }, 'user1');
    vi.mocked(mockRepo.listDrivers).mockResolvedValue([mockUser]);

    const result = await useCase.execute();

    expect(mockRepo.listDrivers).toHaveBeenCalledOnce();
    expect(result).toHaveLength(1);
    expect(result[0].id).toBe('user1');
    expect(result[0].email).toBe('driver@test.com');
    expect(result[0].isMotorista()).toBe(true);
  });

  it('deve retornar lista vazia se nao houver motoristas', async () => {
    vi.mocked(mockRepo.listDrivers).mockResolvedValue([]);

    const result = await useCase.execute();

    expect(result).toEqual([]);
  });
});
