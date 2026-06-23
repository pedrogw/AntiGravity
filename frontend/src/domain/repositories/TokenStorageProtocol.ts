export interface TokenStorageProtocol {
  getToken(): string | null;
  saveToken(token: string): void;
  removeToken(): void;
  getRefreshToken(): string | null;
  saveRefreshToken(token: string): void;
  clearTokens(): void;
}
