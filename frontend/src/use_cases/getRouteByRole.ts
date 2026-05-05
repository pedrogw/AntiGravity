/**
 * Determina a rota de destino baseada no papel (role) do usuário.
 * 
 * Seguindo Clean Architecture, esta regra de negócio é isolada
 * e puramente funcional, fácil de testar.
 */
export function getRouteByRole(role: string): string {
  if (role === 'lojista') {
    return '/dashboard';
  }
  
  if (role === 'motorista') {
    return '/drive';
  }

  // Fallback de segurança: qualquer anomalia manda pro login
  return '/';
}
