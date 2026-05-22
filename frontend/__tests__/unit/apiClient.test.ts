import { apiClient } from '../../src/infrastructure/api/api_client';
import { isTokenExpired } from '../../src/utils/jwt';

vi.mock('../../src/utils/jwt', () => ({
  isTokenExpired: vi.fn(),
}));
describe('API Client (Axios Interceptors)', () => {
  beforeEach(() => {
    // Mock local storage and window
    Storage.prototype.getItem = vi.fn();
    Storage.prototype.removeItem = vi.fn();
    
    // Clear interceptors to avoid side effects between tests
    vi.clearAllMocks();
  });

  it('deve injetar o token JWT no cabeçalho se ele existir no localStorage', async () => {
    const fakeToken = 'meu_token_secreto';
    (Storage.prototype.getItem as vi.Mock).mockReturnValue(fakeToken);
    (isTokenExpired as vi.Mock).mockReturnValue(false);

    // Mock an axios request using the internal request interceptor
    const interceptor = (apiClient.interceptors.request as any).handlers[0].fulfilled;
    const config = { headers: {} as any };
    
    const resultConfig = interceptor(config);
    
    expect(Storage.prototype.getItem).toHaveBeenCalledWith('token');
    expect(resultConfig.headers.Authorization).toBe(`Bearer ${fakeToken}`);
  });

  it('não deve injetar o cabeçalho Authorization se não houver token', async () => {
    (Storage.prototype.getItem as vi.Mock).mockReturnValue(null);

    const interceptor = (apiClient.interceptors.request as any).handlers[0].fulfilled;
    const config = { headers: {} as any };
    
    const resultConfig = interceptor(config);
    
    expect(resultConfig.headers.Authorization).toBeUndefined();
  });
});
