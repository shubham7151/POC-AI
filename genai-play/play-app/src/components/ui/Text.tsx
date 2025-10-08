import React from 'react';
import { Text as RNText, StyleSheet, TextProps } from 'react-native';
import { theme } from '../../styles/theme';

interface CustomTextProps extends TextProps {
  variant?: 'h1' | 'h2' | 'h3' | 'h4' | 'body' | 'bodySmall' | 'caption';
  color?: keyof typeof theme.colors;
  weight?: keyof typeof theme.typography.weights;
  children: React.ReactNode;
}

export const Text: React.FC<CustomTextProps> = ({
  variant = 'body',
  color = 'text',
  weight = 'regular',
  children,
  style,
  ...props
}) => {
  return (
    <RNText
      style={[
        styles.base,
        styles[variant],
        { color: theme.colors[color] },
        { fontWeight: theme.typography.weights[weight] },
        style,
      ]}
      {...props}
    >
      {children}
    </RNText>
  );
};

const styles = StyleSheet.create({
  base: {
    lineHeight: theme.typography.lineHeights.normal,
  },
  h1: { fontSize: theme.typography.h1 },
  h2: { fontSize: theme.typography.h2 },
  h3: { fontSize: theme.typography.h3 },
  h4: { fontSize: theme.typography.h4 },
  body: { fontSize: theme.typography.body },
  bodySmall: { fontSize: theme.typography.bodySmall },
  caption: { fontSize: theme.typography.caption },
});