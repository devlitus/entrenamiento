import { useLocation, useNavigate } from 'react-router-dom';
import { useMemo } from 'react';
import { createNavigationItems, type NavigationItem } from '../components/navigation';

export const useNavigation = () => {
  const location = useLocation();
  const navigate = useNavigate();

  // Crear elementos de navegación con el path actual
  const navigationItems = useMemo(() => 
    createNavigationItems(location.pathname), 
    [location.pathname]
  );

  // Función para navegar a una ruta
  const navigateTo = (path: string) => {
    navigate(path);
  };

  // Función para manejar click en elemento de navegación
  const handleNavigationClick = (item: NavigationItem) => {
    if (item.path && item.path !== location.pathname) {
      navigateTo(item.path);
    }
  };

  // Obtener el elemento activo actual
  const activeItem = navigationItems.find(item => item.active);

  // Verificar si una ruta está activa
  const isRouteActive = (path: string): boolean => {
    return location.pathname === path;
  };

  return {
    currentPath: location.pathname,
    navigationItems,
    activeItem,
    navigateTo,
    handleNavigationClick,
    isRouteActive
  };
};

export default useNavigation;