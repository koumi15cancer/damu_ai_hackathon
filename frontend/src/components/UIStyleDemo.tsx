import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from './ui/dialog';

const UIStyleDemo: React.FC = () => {
  const [inputValue, setInputValue] = useState('');
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [currentTheme, setCurrentTheme] = useState('default');

  const themes = [
    { name: 'default', label: 'Default', class: '' },
    { name: 'light-pink', label: 'Light Pink', class: 'light-pink' },
    { name: 'light-purple', label: 'Light Purple', class: 'light-purple' },
    { name: 'light-yellow', label: 'Light Yellow', class: 'light-yellow' },
    { name: 'light-orange', label: 'Light Orange', class: 'light-orange' },
    { name: 'light-green', label: 'Light Green', class: 'light-green' },
    { name: 'light-blue', label: 'Light Blue', class: 'light-blue' },
    { name: 'dark', label: 'Dark', class: 'dark' },
    { name: 'dark-pink', label: 'Dark Pink', class: 'dark-pink' },
    { name: 'dark-purple', label: 'Dark Purple', class: 'dark-purple' },
    { name: 'dark-yellow', label: 'Dark Yellow', class: 'dark-yellow' },
    { name: 'dark-orange', label: 'Dark Orange', class: 'dark-orange' },
    { name: 'dark-green', label: 'Dark Green', class: 'dark-green' },
    { name: 'dark-blue', label: 'Dark Blue', class: 'dark-blue' },
  ];

  const changeTheme = (themeClass: string) => {
    // Remove all theme classes from body (only non-empty ones)
    themes.forEach(theme => {
      if (theme.class && theme.class.trim() !== '') {
        document.body.classList.remove(theme.class);
      }
    });
    
    // Add the selected theme class (only if it's not empty)
    if (themeClass && themeClass.trim() !== '') {
      document.body.classList.add(themeClass);
    }
    
    setCurrentTheme(themeClass || 'default');
  };

  return (
    <div className="p-6 space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-foreground mb-2">
          Modern UI Components Demo
        </h1>
        <p className="text-muted-foreground">
          Showcasing the new design system with multiple theme colors
        </p>
      </div>

      {/* Theme Switcher */}
      <Card>
        <CardHeader>
          <CardTitle>Theme Switcher</CardTitle>
          <CardDescription>Switch between different color themes</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-2">
            {themes.map((theme) => (
              <Button
                key={theme.name}
                variant={currentTheme === theme.name ? "default" : "outline"}
                size="sm"
                onClick={() => changeTheme(theme.class)}
                className="text-xs"
              >
                {theme.label}
              </Button>
            ))}
          </div>
          <p className="text-sm text-muted-foreground mt-4">
            Current theme: <span className="font-medium">{themes.find(t => t.class === currentTheme)?.label || 'Default'}</span>
          </p>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Button Examples */}
        <Card>
          <CardHeader>
            <CardTitle>Buttons</CardTitle>
            <CardDescription>Various button styles and variants</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex flex-wrap gap-2">
              <Button variant="default">Default</Button>
              <Button variant="secondary">Secondary</Button>
              <Button variant="outline">Outline</Button>
              <Button variant="ghost">Ghost</Button>
              <Button variant="destructive">Destructive</Button>
            </div>
            <div className="flex flex-wrap gap-2">
              <Button size="sm">Small</Button>
              <Button size="default">Default</Button>
              <Button size="lg">Large</Button>
            </div>
          </CardContent>
        </Card>

        {/* Input Examples */}
        <Card>
          <CardHeader>
            <CardTitle>Inputs</CardTitle>
            <CardDescription>Form input components</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <Input
              placeholder="Enter your name"
              value={inputValue}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setInputValue(e.target.value)}
            />
            <Input
              type="email"
              placeholder="Enter your email"
            />
            <Input
              type="password"
              placeholder="Enter your password"
            />
          </CardContent>
        </Card>

        {/* Badge Examples */}
        <Card>
          <CardHeader>
            <CardTitle>Badges</CardTitle>
            <CardDescription>Status indicators and labels</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex flex-wrap gap-2">
              <Badge variant="default">Default</Badge>
              <Badge variant="secondary">Secondary</Badge>
              <Badge variant="destructive">Destructive</Badge>
              <Badge variant="outline">Outline</Badge>
            </div>
          </CardContent>
        </Card>

        {/* Dialog Example */}
        <Card>
          <CardHeader>
            <CardTitle>Dialog</CardTitle>
            <CardDescription>Modal dialogs and overlays</CardDescription>
          </CardHeader>
          <CardContent>
            <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
              <DialogTrigger asChild>
                <Button variant="outline">Open Dialog</Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Example Dialog</DialogTitle>
                  <DialogDescription>
                    This is an example of the new dialog component. It provides a modern,
                    accessible modal experience with smooth animations.
                  </DialogDescription>
                </DialogHeader>
                <div className="py-4">
                  <p className="text-sm text-muted-foreground">
                    You can put any content here. The dialog automatically handles
                    focus management, keyboard navigation, and screen reader support.
                  </p>
                </div>
                <DialogFooter>
                  <Button variant="outline" onClick={() => setIsDialogOpen(false)}>
                    Cancel
                  </Button>
                  <Button onClick={() => setIsDialogOpen(false)}>
                    Confirm
                  </Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          </CardContent>
        </Card>

        {/* Color Scheme Demo */}
        <Card>
          <CardHeader>
            <CardTitle>Color Scheme</CardTitle>
            <CardDescription>CSS custom properties for theming</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="bg-primary text-primary-foreground p-2 rounded">
                Primary
              </div>
              <div className="bg-secondary text-secondary-foreground p-2 rounded">
                Secondary
              </div>
              <div className="bg-muted text-muted-foreground p-2 rounded">
                Muted
              </div>
              <div className="bg-accent text-accent-foreground p-2 rounded">
                Accent
              </div>
              <div className="bg-destructive text-destructive-foreground p-2 rounded">
                Destructive
              </div>
              <div className="border border-border bg-background text-foreground p-2 rounded">
                Border
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Animation Demo */}
        <Card>
          <CardHeader>
            <CardTitle>Animations</CardTitle>
            <CardDescription>Smooth transitions and animations</CardDescription>
          </CardHeader>
          <CardContent>
            <Button 
              className="animate-in"
              onClick={() => {
                // This will trigger the animation
                const btn = document.querySelector('.animate-in');
                btn?.classList.remove('animate-in');
                setTimeout(() => btn?.classList.add('animate-in'), 100);
              }}
            >
              Click for Animation
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Theme Colors Showcase */}
      <Card>
        <CardHeader>
          <CardTitle>Available Theme Colors</CardTitle>
          <CardDescription>All available color themes in the design system</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4">
            {themes.map((theme) => (
              <div key={theme.name} className="text-center">
                <div 
                  className={`w-16 h-16 rounded-lg mx-auto mb-2 border-2 ${
                    currentTheme === theme.name ? 'border-primary' : 'border-border'
                  }`}
                  style={{
                    backgroundColor: theme.name.includes('pink') ? '#fdf2f8' :
                    theme.name.includes('purple') ? '#faf5ff' :
                    theme.name.includes('yellow') ? '#fffbeb' :
                    theme.name.includes('orange') ? '#fff7ed' :
                    theme.name.includes('green') ? '#f0fdf4' :
                    theme.name.includes('blue') ? '#eff6ff' :
                    theme.name.includes('dark') ? '#1f2937' : '#ffffff'
                  }}
                ></div>
                <p className="text-xs font-medium">{theme.label}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Integration Note */}
      <Card className="border-blue-200 bg-blue-50">
        <CardHeader>
          <CardTitle className="text-blue-900">Integration Note</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-blue-800">
            These new UI components can be used alongside your existing Material-UI components. 
            The design system provides consistent spacing, colors, and typography while maintaining 
            the flexibility to mix and match as needed. The theme system allows for easy customization
            and brand alignment.
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default UIStyleDemo; 