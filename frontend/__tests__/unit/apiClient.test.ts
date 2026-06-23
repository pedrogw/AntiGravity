import { apiClient } from '../../src/infrastructure/api/api_client';
import { isTokenExpired } from '../../src/utils/jwt';

type AxiosInterceptorHandler = (config: Record<string, unknown>) => Record<string, unknown>;
type AxiosInterceptorManager = { handlers: Array<{ fulfilled: AxiosInterceptorHandler; rejected: AxiosInterceptorHandler }> };

vi.mock('../../src/utils/jwt', () => ({
  isTokenExpired: vi.fn(),
}));

function getRequestInterceptor(): AxiosInterceptorHandler {
  return (apiClient.interceptors.request as unknown as AxiosInterceptorManager).handlers[0].fulfilled;
}

describe('API Client (Axios Interceptors)', () => {
  beforeEach(() => {
    Storage.prototype.getItem = vi.fn();
    Storage.prototype.removeItem = vi.fn();
    vi.clearAllMocks();
  });

  it('deve injetar o token JWT no cabeçalho se ele existir no localStorage', async () => {
    const fakeToken = 'meu_token_secreto';
    (Storage.prototype.getItem as vi.Mock).mockReturnValue(fakeToken);
    (isTokenExpired as vi.Mock).mockReturnValue(false);

    const interceptor = getRequestInterceptor();
    const config = { headers: {} as Record<string, string> };

    const resultConfig = interceptor(config);

    expect(Storage.prototype.getItem).toHaveBeenCalledWith('token');
    expect((resultConfig.headers as Record<string, string>).Authorization).toBe(`Bearer ${fakeToken}`);
  });

  it('não deve injetar o cabeçalho Authorization se não houver token', async () => {
    (Storage.prototype.getItem as vi.Mock).mockReturnValue(null);

    const interceptor = getRequestInterceptor();
    const config = { headers: {} as Record<string, string> };

    const resultConfig = interceptor(config);

    expect((resultConfig.headers as Record<string, string>).Authorization).toBeUndefined();
  });
});
