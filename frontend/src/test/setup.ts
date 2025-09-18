import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mock de fetch global para tests que usan API calls
globalThis.fetch = vi.fn();

// Mock de window.matchMedia para componentes que usan media queries
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Suprimir warnings específicos de React en tests
const originalError = console.error;
console.error = (...args: any[]) => {
  if (
    typeof args[0] === 'string' &&
    (args[0].includes('Warning: ReactDOM.render is no longer supported') ||
     args[0].includes('Warning: React.createFactory() is deprecated'))
  ) {
    return;
  }
  originalError.call(console, ...args);
};
