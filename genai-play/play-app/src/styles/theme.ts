// src/styles/theme.ts
export const colors = {
  // Primary AJ Bell colors from the images
  primary: '#E91E63', // AJ Bell pink/red
  primaryDark: '#C2185B',
  primaryLight: '#F8BBD9',
  
  // Background and surface colors
  background: '#FFFFFF',
  surface: '#F5F5F5',
  card: '#FFFFFF',
  
  // Text colors
  text: '#333333',
  textSecondary: '#666666',
  textLight: '#999999',
  textWhite: '#FFFFFF',
  
  // Status colors
  success: '#4CAF50', // Green for cash/positive amounts
  warning: '#FF9800',
  error: '#F44336',
  info: '#2196F3',
  
  // UI colors
  border: '#E0E0E0',
  divider: '#EEEEEE',
  shadow: 'rgba(0, 0, 0, 0.1)',
  
  // PLA specific colors
  plaHighlight: '#E91E63', // Same as primary for consistency
  plaBackground: 'rgba(233, 30, 99, 0.05)',
  plaBorder: 'rgba(233, 30, 99, 0.2)',
};

export const typography = {
  // Font sizes matching the Dodl design
  h1: 28,
  h2: 24,
  h3: 20,
  h4: 18,
  body: 16,
  bodySmall: 14,
  caption: 12,
  
  // Font weights
  weights: {
    light: '300' as const,
    regular: '400' as const,
    medium: '500' as const,
    bold: '700' as const,
  },
  
  // Line heights
  lineHeights: {
    tight: 1.2,
    normal: 1.4,
    loose: 1.6,
  },
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

export const borderRadius = {
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  full: 9999,
};

export const shadows = {
  sm: {
    shadowColor: colors.shadow,
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  md: {
    shadowColor: colors.shadow,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 4,
    elevation: 4,
  },
  lg: {
    shadowColor: colors.shadow,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 8,
  },
};

// Export combined theme object
export const theme = {
  colors,
  typography,
  spacing,
  borderRadius,
  shadows,
} as const;

export type Theme = typeof theme;