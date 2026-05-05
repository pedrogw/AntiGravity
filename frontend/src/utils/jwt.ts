/**
 * Verifica se um token JWT está expirado baseado no claim 'exp'.
 * Caso o token seja inválido ou não contenha 'exp', retornamos true (expirado) por segurança.
 */
export function isTokenExpired(token: string | null): boolean {
  if (!token) return true;

  try {
    const [, payloadBase64] = token.split('.');
    if (!payloadBase64) return true;

    // A web atob ou buffer em node
    const payloadJson = typeof window !== 'undefined' 
      ? window.atob(payloadBase64)
      : Buffer.from(payloadBase64, 'base64').toString('ascii');

    const payload = JSON.parse(payloadJson);
    
    if (!payload.exp) return true;

    // JWT exp is in seconds, Date.now() is in milliseconds
    const currentTime = Math.floor(Date.now() / 1000);
    return payload.exp < currentTime;
  } catch (e) {
    // Qualquer erro de parsing tratamos como token inválido/expirado
    return true;
  }
}
