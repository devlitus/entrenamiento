import React from 'react';

export interface NavigationItem {
  id: string;
  label: string;
  icon: React.ReactNode;
  path: string;
  active?: boolean;
  onClick?: () => void;
}

interface NavigationProps {
  items: NavigationItem[];
  currentPath?: string;
  onItemClick?: (item: NavigationItem) => void;
  className?: string;
}

interface NavItemProps {
  item: NavigationItem;
  isActive: boolean;
  onClick: () => void;
}

const NavItem: React.FC<NavItemProps> = ({ item, isActive, onClick }) => (
  <button
    onClick={onClick}
    className={`w-full flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors ${
      isActive
        ? 'bg-[rgb(var(--color-primary))] text-white'
        : 'text-[rgb(var(--color-text-secondary))] hover:bg-[rgb(var(--color-surface))] hover:text-[rgb(var(--color-text-primary))]'
    }`}
    aria-current={isActive ? 'page' : undefined}
  >
    <span className="mr-3">{item.icon}</span>
    {item.label}
  </button>
);

export const Navigation: React.FC<NavigationProps> = ({ 
  items, 
  currentPath = '', 
  onItemClick,
  className = '' 
}) => {
  const handleItemClick = (item: NavigationItem) => {
    if (item.onClick) {
      item.onClick();
    }
    if (onItemClick) {
      onItemClick(item);
    }
  };

  return (
    <nav className={`space-y-2 ${className}`} role="navigation" aria-label="Navegación principal">
      {items.map((item) => {
        const isActive = item.active || currentPath === item.path;
        
        return (
          <NavItem
            key={item.id}
            item={item}
            isActive={isActive}
            onClick={() => handleItemClick(item)}
          />
        );
      })}
    </nav>
  );
};

export default Navigation;