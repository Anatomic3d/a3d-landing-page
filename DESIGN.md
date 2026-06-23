---
name: Clinical Precision
colors:
  surface: '#f8f9ff'
  surface-dim: '#ccdbf3'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e6eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d5e3fc'
  on-surface: '#0d1c2e'
  on-surface-variant: '#434653'
  inverse-surface: '#233144'
  inverse-on-surface: '#eaf1ff'
  outline: '#737784'
  outline-variant: '#c3c6d5'
  surface-tint: '#2559bd'
  primary: '#00327d'
  on-primary: '#ffffff'
  primary-container: '#0047ab'
  on-primary-container: '#a5bdff'
  inverse-primary: '#b1c5ff'
  secondary: '#006875'
  on-secondary: '#ffffff'
  secondary-container: '#00e3fd'
  on-secondary-container: '#00616d'
  tertiary: '#343739'
  on-tertiary: '#ffffff'
  tertiary-container: '#4b4e50'
  on-tertiary-container: '#bcbfc1'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae2ff'
  primary-fixed-dim: '#b1c5ff'
  on-primary-fixed: '#001946'
  on-primary-fixed-variant: '#00419e'
  secondary-fixed: '#9cf0ff'
  secondary-fixed-dim: '#00daf3'
  on-secondary-fixed: '#001f24'
  on-secondary-fixed-variant: '#004f58'
  tertiary-fixed: '#e0e3e5'
  tertiary-fixed-dim: '#c4c7c9'
  on-tertiary-fixed: '#191c1e'
  on-tertiary-fixed-variant: '#444749'
  background: '#f8f9ff'
  on-background: '#0d1c2e'
  surface-variant: '#d5e3fc'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-technical:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.02em
  caption:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-max: 1440px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 48px
---

## Brand & Style
The design system is engineered to bridge the gap between advanced additive manufacturing and clinical surgical environments. The personality is **authoritative, hyper-precise, and life-saving**, prioritizing clarity and technical sophistication above all else.

The design style is **Corporate / Modern** with a focus on high-tech clinical utility. It utilizes a "Sterile Layering" approach—using whitespace and subtle tonal shifts to define hierarchy rather than heavy decoration. This ensures that complex 3D anatomical data and surgical plans remain the focal point of the interface. The aesthetic evokes the cleanliness of an operating room combined with the innovative edge of a high-tech laboratory.

## Colors
The palette is rooted in medical reliability and technical precision. 

- **Primary (Deep Surgical Blue):** Used for primary actions, navigation headers, and authoritative branding elements. It conveys trust and stability.
- **Secondary (Sterile Cyan):** Used sparingly for interactive accents, progress indicators, and highlighting critical data points in 3D visualizations. 
- **Neutral (Medical Greys):** A range of cool-toned greys used for text and iconography to maintain a high-contrast, professional reading environment.
- **Background (Clean Medical White):** A slightly cool-tinted white base to reduce eye strain during long surgical planning sessions while maintaining a "sterile" feel.

## Typography
The typography system prioritizes legibility and a systematic, developer-friendly feel. **Inter** is the primary typeface, chosen for its exceptional readability in data-dense interfaces and its neutral, professional tone. 

For technical data, coordinates, and 3D printing parameters, **Geist** is introduced as a secondary label font to provide a clean, monospaced-adjacent aesthetic that signals "technical precision." Headlines use tighter letter-spacing and heavier weights to establish a strong hierarchy, while body text maintains generous line heights for clinical reports and documentation.

## Layout & Spacing
The layout follows a **Fluid Grid** model with a strict 8px spacing rhythm. In a medical context, density must be balanced with "breathing room" to prevent cognitive overload during critical decision-making.

- **Desktop:** A 12-column grid with 24px gutters. Side panels (used for 3D toolsets) are pinned to the right with a fixed width of 320px.
- **Tablet:** A 6-column grid with 20px gutters. 3D viewports expand to fill the screen width.
- **Mobile:** A 4-column grid with 16px margins. Complex 3D interactions are simplified into sequential steps.

Layouts should favor top-down hierarchies with consistent padding inside "Medical Cards" to ensure data points are never crowded.

## Elevation & Depth
This design system uses **Tonal Layers** and **Ambient Shadows** to create a focused, professional depth. 

Shadows are used sparingly; they are highly diffused and slightly tinted with the Primary Blue to prevent a "dirty" look. Most depth is communicated through subtle border-bottoms and background color shifts (e.g., using a slightly darker grey for a "Sunken" 3D viewport and a pure white for "Elevated" control modals). 

Hover states utilize a subtle inner-glow or a change in border-weight rather than heavy drop shadows, maintaining the "flat-yet-tactile" precision required for medical software.

## Shapes
The shape language is **Rounded**, opting for a 0.5rem (8px) base radius. This softens the technical nature of the software, making it feel approachable and modern without losing the "grid-aligned" precision of the medical industry. 

Large containers, such as 3D viewports or image galleries, use `rounded-xl` (24px) to create a distinct frame, while functional elements like input fields and buttons stay at the base `rounded` level for a more compact, tool-like feel.

## Components
- **Buttons:** Primary buttons are solid Deep Surgical Blue with white text. Secondary buttons use a Sterile Cyan ghost-border. State changes (hover/active) should be subtle shifts in saturation.
- **Input Fields:** Use a light grey fill with a 1px stroke. On focus, the stroke changes to Primary Blue with a very soft, 2px outer glow. Labels are always positioned above the field using the `label-technical` style.
- **3D Viewport Cards:** These are the centerpiece. They should have a deep grey background to make anatomical models (usually white/bone or red/tissue) pop. Controls are overlaid using semi-transparent "Glass" panels.
- **Status Chips:** Used for "In Printing," "Sterilized," or "Shipped." These use high-contrast backgrounds with white text: Green for success, Cyan for active, and Navy for pending.
- **Anatomical Lists:** Use high-density rows with "Micro-Thumbnails" of the 3D part. Zebra-striping is used in long data tables to ensure horizontal scanning accuracy.
- **Progress Steppers:** For surgical planning workflows, use a linear stepper at the top of the interface, using the Secondary Cyan to indicate the "Current Active" path.