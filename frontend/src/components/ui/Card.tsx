import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  variant?: 'default' | 'elevated' | 'outlined';
}

interface CardHeaderProps {
  children: React.ReactNode;
  className?: string;
}

interface CardTitleProps {
  children: React.ReactNode;
  className?: string;
}

interface CardContentProps {
  children: React.ReactNode;
  className?: string;
}

interface CardFooterProps {
  children: React.ReactNode;
  className?: string;
}

const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ children, className = '', variant = 'default' }, ref) => {
    const baseClasses = 'dashboard-card p-6';
    const variantClasses = {
      default: '',
      elevated: 'shadow-lg',
      outlined: 'border-2'
    };

    return (
      <div
        ref={ref}
        className={`${baseClasses} ${variantClasses[variant]} ${className}`}
      >
        {children}
      </div>
    );
  }
);

const CardHeader = React.forwardRef<HTMLDivElement, CardHeaderProps>(
  ({ children, className = '' }, ref) => (
    <div
      ref={ref}
      className={`flex flex-col space-y-1.5 pb-4 ${className}`}
    >
      {children}
    </div>
  )
);

const CardTitle = React.forwardRef<HTMLHeadingElement, CardTitleProps>(
  ({ children, className = '' }, ref) => (
    <h3
      ref={ref}
      className={`text-lg font-semibold leading-none tracking-tight text-[rgb(var(--color-text-primary))] ${className}`}
    >
      {children}
    </h3>
  )
);

const CardContent = React.forwardRef<HTMLDivElement, CardContentProps>(
  ({ children, className = '' }, ref) => (
    <div ref={ref} className={`${className}`}>
      {children}
    </div>
  )
);

const CardFooter = React.forwardRef<HTMLDivElement, CardFooterProps>(
  ({ children, className = '' }, ref) => (
    <div
      ref={ref}
      className={`flex items-center pt-4 ${className}`}
    >
      {children}
    </div>
  )
);

Card.displayName = 'Card';
CardHeader.displayName = 'CardHeader';
CardTitle.displayName = 'CardTitle';
CardContent.displayName = 'CardContent';
CardFooter.displayName = 'CardFooter';

export { Card, CardHeader, CardTitle, CardContent, CardFooter };
export default Card;