export interface TokenStorageProtocol {
  getToken(): string | null;
  saveToken(token: string): void;
  removeToken(): void;
}

export class TokenStorageAdapter implements TokenStorageProtocol {
  private readonly TOKEN_KEY = 'token';

  getToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem(this.TOKEN_KEY);
  }

  saveToken(token: string): void {
    if (typeof window === 'undefined') return;
    localStorage.setItem(this.TOKEN_KEY, token);
  }

  removeToken(): void {
    if (typeof window === 'undefined') return;
    localStorage.removeItem(this.TOKEN_KEY);
  }
}
