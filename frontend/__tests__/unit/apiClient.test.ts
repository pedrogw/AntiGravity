import { apiClient } from '../../src/infrastructure/api/api_client';
import { isTokenExpired } from '../../src/utils/jwt';

jest.mock('../../src/utils/jwt', () => ({
  isTokenExpired: jest.fn(),
}));
describe('API Client (Axios Interceptors)', () => {
  beforeEach(() => {
    // Mock local storage and window
    Storage.prototype.getItem = jest.fn();
    Storage.prototype.removeItem = jest.fn();
    
    // Clear interceptors to avoid side effects between tests
    jest.clearAllMocks();
  });

  it('deve injetar o token JWT no cabeçalho se ele existir no localStorage', async () => {
    const fakeToken = 'meu_token_secreto';
    (Storage.prototype.getItem as jest.Mock).mockReturnValue(fakeToken);
    (isTokenExpired as jest.Mock).mockReturnValue(false);

    // Mock an axios request using the internal request interceptor
    const interceptor = (apiClient.interceptors.request as any).handlers[0].fulfilled;
    const config = { headers: {} as any };
    
    const resultConfig = interceptor(config);
    
    expect(Storage.prototype.getItem).toHaveBeenCalledWith('token');
    expect(resultConfig.headers.Authorization).toBe(`Bearer ${fakeToken}`);
  });

  it('não deve injetar o cabeçalho Authorization se não houver token', async () => {
    (Storage.prototype.getItem as jest.Mock).mockReturnValue(null);

    const interceptor = (apiClient.interceptors.request as any).handlers[0].fulfilled;
    const config = { headers: {} as any };
    
    const resultConfig = interceptor(config);
    
    expect(resultConfig.headers.Authorization).toBeUndefined();
  });
});
