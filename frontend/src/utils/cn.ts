/**
 * Utilidad para combinar clases CSS de manera condicional
 * Similar a clsx pero más simple para nuestras necesidades
 */
export function cn(...classes: (string | undefined | null | false)[]): string {
  return classes
    .filter(Boolean)
    .join(' ')
    .trim();
}