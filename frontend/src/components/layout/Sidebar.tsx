import React from 'react';
import { Button } from '../ui/Button';
import { Navigation } from '../navigation';
import { useNavigation } from '../../hooks/useNavigation';

interface SidebarProps {
  onClose?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ onClose }) => {
  const { navigationItems, handleNavigationClick } = useNavigation();

  const toggleTheme = () => {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
  };

  return (
    <div className="flex h-full flex-col bg-[rgb(var(--color-card))] border-r border-[rgb(var(--color-border))]">
      {/* Header del sidebar */}
      <div className="flex items-center justify-between p-6 border-b border-[rgb(var(--color-border))]">
        <div className="flex items-center">
          <div className="w-8 h-8 bg-[rgb(var(--color-primary))] rounded-lg flex items-center justify-center">
            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <span className="ml-3 text-lg font-semibold text-[rgb(var(--color-text-primary))]">
            Neural Trainer
          </span>
        </div>
        
        {onClose && (
          <button
            onClick={onClose}
            className="lg:hidden p-1 rounded-md text-[rgb(var(--color-text-secondary))] hover:text-[rgb(var(--color-text-primary))] hover:bg-[rgb(var(--color-surface))]"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>

      {/* Navegación */}
      <Navigation 
        items={navigationItems}
        onItemClick={handleNavigationClick}
        className="flex-1 px-4 py-6"
      />

      {/* Footer con toggle de tema */}
      <div className="p-4 border-t border-[rgb(var(--color-border))]">
        <Button
          variant="ghost"
          size="sm"
          onClick={toggleTheme}
          className="w-full justify-start"
        >
          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
          </svg>
          Cambiar tema
        </Button>
        
        <div className="mt-3 pt-3 border-t border-[rgb(var(--color-border))]">
          <div className="flex items-center">
            <div className="w-8 h-8 bg-[rgb(var(--color-primary))] rounded-full flex items-center justify-center">
              <span className="text-sm font-medium text-white">U</span>
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-[rgb(var(--color-text-primary))]">Usuario</p>
              <p className="text-xs text-[rgb(var(--color-text-secondary))]">usuario@ejemplo.com</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;