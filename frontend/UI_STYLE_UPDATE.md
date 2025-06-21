# UI Style Update Documentation

## Overview
This document describes the UI style updates that have been applied to the damu_ai_hackathon frontend, copying the modern design system from talent-acquisitioner-prototype.

## Changes Made

### 1. Dependencies Added
- **Tailwind CSS**: Modern utility-first CSS framework
- **Radix UI**: Accessible, unstyled UI primitives
- **Class Variance Authority**: For component variant management
- **Lucide React**: Modern icon library
- **Tailwind Merge**: For efficient class name merging

### 2. Configuration Files
- `tailwind.config.js`: Tailwind configuration with custom design tokens
- `postcss.config.js`: PostCSS configuration for Tailwind processing
- Updated `src/index.css`: Modern CSS custom properties and Tailwind directives

### 3. UI Components Created
Located in `src/components/ui/`:
- `button.tsx`: Modern button component with multiple variants
- `card.tsx`: Card layout components (Card, CardHeader, CardContent, etc.)
- `input.tsx`: Form input component
- `badge.tsx`: Status indicator component
- `dialog.tsx`: Modal dialog component

### 4. Utility Functions
- `src/lib/utils.ts`: Contains the `cn()` function for combining class names

### 5. Demo Component
- `src/components/UIStyleDemo.tsx`: Showcases all new UI components with theme switcher

## Design System Features

### Color Scheme
The design system uses CSS custom properties for consistent theming:
- `--primary`: Primary brand color
- `--secondary`: Secondary color
- `--muted`: Muted text and backgrounds
- `--accent`: Accent color for highlights
- `--destructive`: Error/danger color
- `--border`: Border colors
- `--background`: Background colors
- `--foreground`: Text colors

### Available Themes
The design system includes **14 different color themes**:

#### Light Themes
- **Default**: Clean, neutral theme
- **Light Pink**: Soft pink color scheme
- **Light Purple**: Gentle purple theme
- **Light Yellow**: Warm yellow theme
- **Light Orange**: Vibrant orange theme
- **Light Green**: Fresh green theme
- **Light Blue**: Cool blue theme

#### Dark Themes
- **Dark**: Classic dark theme
- **Dark Pink**: Dark pink color scheme
- **Dark Purple**: Deep purple theme
- **Dark Yellow**: Dark yellow theme
- **Dark Orange**: Dark orange theme
- **Dark Green**: Dark green theme
- **Dark Blue**: Dark blue theme

### Typography
- Consistent font sizing and spacing
- Proper contrast ratios for accessibility
- Responsive text scaling

### Spacing
- Consistent spacing scale using Tailwind's spacing utilities
- Responsive padding and margins

### Animations
- Smooth transitions for interactive elements
- Fade-in animations for content
- Hover effects for buttons and interactive elements

## Usage

### Basic Button
```tsx
import { Button } from './components/ui/button';

<Button variant="default">Click me</Button>
<Button variant="outline">Outline Button</Button>
<Button variant="destructive">Delete</Button>
```

### Card Layout
```tsx
import { Card, CardHeader, CardTitle, CardContent } from './components/ui/card';

<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
  </CardHeader>
  <CardContent>
    Card content goes here
  </CardContent>
</Card>
```

### Form Input
```tsx
import { Input } from './components/ui/input';

<Input placeholder="Enter your name" />
```

### Badge
```tsx
import { Badge } from './components/ui/badge';

<Badge variant="default">New</Badge>
<Badge variant="secondary">Draft</Badge>
```

### Theme Switching
```tsx
// Switch to a specific theme
const changeTheme = (themeClass: string) => {
  // Remove all theme classes
  document.body.classList.remove('light-pink', 'light-purple', 'dark', 'dark-pink', etc...);
  
  // Add the selected theme class
  if (themeClass) {
    document.body.classList.add(themeClass);
  }
};

// Example usage
changeTheme('light-pink'); // Switch to light pink theme
changeTheme('dark-blue');  // Switch to dark blue theme
changeTheme('');           // Switch to default theme
```

## Integration with Existing Components

The new UI components can be used alongside existing Material-UI components. The design system provides:
- Consistent spacing and typography
- Complementary color schemes
- Modern, accessible components
- Flexible theming options

## Running the Demo

To see the new UI components in action:
1. Import the `UIStyleDemo` component
2. Add it to your app's routing or main component
3. The demo showcases all available components and their variants
4. Use the theme switcher to see all available color themes

## Theme Customization

### Adding Custom Themes
To add a custom theme, add a new CSS class in `src/index.css`:

```css
.custom-theme {
  color-scheme: light;
  
  --background: 200 100% 97%;
  --foreground: 200 21% 41%;
  --primary: 200 34% 48%;
  --primary-foreground: 200 100% 93%;
  /* ... other color variables */
}
```

### Theme Classes
Available theme classes to apply to the `<body>` element:
- `light-pink`, `light-purple`, `light-yellow`, `light-orange`, `light-green`, `light-blue`
- `dark`, `dark-pink`, `dark-purple`, `dark-yellow`, `dark-orange`, `dark-green`, `dark-blue`

## Next Steps

1. **Gradual Migration**: Replace Material-UI components with new ones as needed
2. **Customization**: Adjust the design tokens in `tailwind.config.js` to match your brand
3. **Additional Components**: Add more components from the talent-acquisitioner-prototype as needed
4. **Theme Support**: Implement theme persistence and user preferences
5. **Brand Integration**: Customize themes to match your brand colors

## Browser Support

The new UI system supports:
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers
- Accessibility features (screen readers, keyboard navigation)
- CSS custom properties (CSS variables) 