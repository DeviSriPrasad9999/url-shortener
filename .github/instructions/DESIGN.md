---
name: SNIPURL Liquid Glass
colors:
  surface: '#0d1515'
  surface-dim: '#0d1515'
  surface-bright: '#333b3b'
  surface-container-lowest: '#080f10'
  surface-container-low: '#151d1e'
  surface-container: '#192122'
  surface-container-high: '#232b2c'
  surface-container-highest: '#2e3637'
  on-surface: '#dce4e5'
  on-surface-variant: '#b9cacb'
  inverse-surface: '#dce4e5'
  inverse-on-surface: '#2a3233'
  outline: '#849495'
  outline-variant: '#3b494b'
  surface-tint: '#00dbe9'
  primary: '#dbfcff'
  on-primary: '#00363a'
  primary-container: '#00f0ff'
  on-primary-container: '#006970'
  inverse-primary: '#006970'
  secondary: '#dcb8ff'
  on-secondary: '#480081'
  secondary-container: '#7701d0'
  on-secondary-container: '#dcb7ff'
  tertiary: '#fff5de'
  on-tertiary: '#3b2f00'
  tertiary-container: '#fed639'
  on-tertiary-container: '#715d00'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#7df4ff'
  primary-fixed-dim: '#00dbe9'
  on-primary-fixed: '#002022'
  on-primary-fixed-variant: '#004f54'
  secondary-fixed: '#efdbff'
  secondary-fixed-dim: '#dcb8ff'
  on-secondary-fixed: '#2c0051'
  on-secondary-fixed-variant: '#6700b5'
  tertiary-fixed: '#ffe179'
  tertiary-fixed-dim: '#eac324'
  on-tertiary-fixed: '#231b00'
  on-tertiary-fixed-variant: '#554500'
  background: '#0d1515'
  on-background: '#dce4e5'
  surface-variant: '#2e3637'
typography:
  display-lg:
    fontFamily: Sora
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Sora
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Sora
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: 0.05em
  headline-lg-mobile:
    fontFamily: Sora
    fontSize: 28px
    fontWeight: '600'
    lineHeight: '1.2'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  container-max: 1200px
  gutter: 24px
---

## Brand & Style

This design system embodies a "Liquid Glass" aesthetic—a fusion of cinematic depth and high-tech precision. It is designed for a premium audience that values speed, security, and sophistication. The visual narrative centers on the concept of "instant redirection," visualized through light traveling through crystalline structures.

The style leverages **Glassmorphism** heavily, utilizing deep backdrop blurs and semi-transparent surfaces to create a sense of physical layering. The interface feels like a high-end heads-up display (HUD), where elements float over a vast, dark obsidian void. Motion is fluid and frictionless, mimicking the behavior of light and liquid.

## Colors

The palette is anchored in **Obsidian Black**, providing a cinematic stage for vibrant, luminescent accents. 

- **Primary (Electric Cyan):** Represents the "energy" of the link redirection. Used for primary actions and critical path highlights.
- **Secondary (Neon Violet):** Used for branding elements and secondary interactions to provide a rich, multi-chromatic depth.
- **Glass Surfaces:** Low-opacity whites create the "frosted" effect, while borders use higher opacity to define the "edge" of the glass.
- **Functional Colors:** Error and Success states are filtered through a neon lens—using high-saturation reds and greens that glow against the dark background.

## Typography

Typography is clean and technical. **Sora** is utilized for headlines to provide a geometric, futuristic feel with its distinct "ink traps" and wide stance. **Inter** is used for body and labels to ensure maximum legibility at small sizes during rapid navigation.

- **Headlines:** Should always have a slight "optical" weight—bold but never chunky. 
- **Labels:** Set in uppercase with increased letter spacing for a refined, data-driven look.
- **Body Text:** Uses a high-contrast white (90% opacity) against the obsidian background to maintain readability without harshness.

## Layout & Spacing

The layout follows a **Fluid Grid** model with generous safe areas to emphasize the premium, airy feel. 

- **Grid:** A 12-column system is used for desktop, collapsing to 4 columns for mobile. 
- **Rhythm:** Spacing follows a 4px base unit. Larger gaps (40px+) are encouraged between sections to allow the glass components to "breathe" against the background.
- **Mobile:** Margins are reduced to 16px, and components like the URL input field scale to full-width to provide a "tool-first" experience.

## Elevation & Depth

Depth is achieved through layering translucent surfaces rather than traditional shadows.

- **The Void (Base):** The #050505 background.
- **Layer 1 (Cards/Panels):** `backdrop-filter: blur(20px)` with a `1px` solid border (`rgba(255, 255, 255, 0.1)`).
- **Layer 2 (Modals/Popovers):** `backdrop-filter: blur(40px)` with a subtle inner glow (`box-shadow: inset 0 0 20px rgba(255, 255, 255, 0.05)`).
- **Interactions:** When hovered, glass elements should increase in border brightness and background saturation, creating a "charged" effect.

## Shapes

The design system uses a **Rounded** shape language to soften the high-tech aesthetic and make it feel more approachable. 

- **Default:** 8px (0.5rem) for buttons and input fields.
- **Large:** 16px (1rem) for primary cards and content containers.
- **Extra Large:** 24px (1.5rem) for main dashboard sections.
- **Pill:** Reserved specifically for "Copy" badges and status indicators to differentiate them from functional buttons.

## Components

### Buttons
- **Primary:** Gradient background (Cyan to Violet), no border, white text with a subtle text-shadow. On hover, the gradient should "pulse" or shift.
- **Secondary (Glass):** Semi-transparent background with a 1px white border (15% opacity). On hover, increase border opacity to 40%.

### Input Fields
- **URL Input:** Large-scale input with a blur background. Focus state triggers a 1px glow using the Cyan accent color and a subtle "liquid" transition of the border.

### Cards
- **Link Card:** A frosted glass container. Includes a "micro-sparkline" of link clicks in the background, rendered in low-opacity Cyan.

### Redirection Animation
- A custom component showing a horizontal "light streak" that travels from the original URL to the SnipURL, signifying the speed of the service.

### Chips/Badges
- Small, pill-shaped glass elements used for tags or analytics counts. Use a high-blur backdrop to ensure text remains legible over background gradients.