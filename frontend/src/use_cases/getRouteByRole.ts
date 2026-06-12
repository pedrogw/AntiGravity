export function getRouteByRole(role: string): string {
  if (role === 'lojista') {
    return '/dashboard';
  }

  if (role === 'motorista') {
    return '/drive';
  }

  return '/';
}
