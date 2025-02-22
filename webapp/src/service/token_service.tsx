export function removeTokenFromStorage(): void {
  localStorage.removeItem("access_token");
}

export function getTokenFromStorage(): string | null {
  return localStorage.getItem("access_token");
}
