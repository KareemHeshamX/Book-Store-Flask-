---
name: Modern Literary
colors:
  surface: '#faf9f5'
  surface-dim: '#dbdad6'
  surface-bright: '#faf9f5'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f4f4f0'
  surface-container: '#efeeea'
  surface-container-high: '#e9e8e4'
  surface-container-highest: '#e3e2df'
  on-surface: '#1b1c1a'
  on-surface-variant: '#444748'
  inverse-surface: '#2f312e'
  inverse-on-surface: '#f2f1ed'
  outline: '#747878'
  outline-variant: '#c4c7c7'
  surface-tint: '#5f5e5e'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#1c1b1b'
  on-primary-container: '#858383'
  inverse-primary: '#c8c6c5'
  secondary: '#4e635a'
  on-secondary: '#ffffff'
  secondary-container: '#cee5da'
  on-secondary-container: '#52675e'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#370e00'
  on-tertiary-container: '#ba7153'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e5e2e1'
  primary-fixed-dim: '#c8c6c5'
  on-primary-fixed: '#1c1b1b'
  on-primary-fixed-variant: '#474746'
  secondary-fixed: '#d1e8dd'
  secondary-fixed-dim: '#b5ccc1'
  on-secondary-fixed: '#0b1f18'
  on-secondary-fixed-variant: '#374b43'
  tertiary-fixed: '#ffdbce'
  tertiary-fixed-dim: '#ffb598'
  on-tertiary-fixed: '#370e00'
  on-tertiary-fixed-variant: '#71361d'
  background: '#faf9f5'
  on-background: '#1b1c1a'
  surface-variant: '#e3e2df'
typography:
  display-lg:
    fontFamily: Bodoni Moda
    fontSize: 64px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Bodoni Moda
    fontSize: 40px
    fontWeight: '600'
    lineHeight: '1.2'
  headline-lg-mobile:
    fontFamily: Bodoni Moda
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Bodoni Moda
    fontSize: 28px
    fontWeight: '500'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Hanken Grotesk
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Hanken Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-md:
    fontFamily: Hanken Grotesk
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Hanken Grotesk
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1.2'
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 8px
  container-max-width: 1280px
  gutter: 24px
  margin-mobile: 20px
  margin-desktop: 64px
  section-gap: 80px
---

## Brand & Style
This design system embodies the quiet authority of a curated private library transitioned into a digital space. The brand personality is scholarly yet accessible, trading clinical minimalism for a warm, editorial sophistication. It targets a discerning audience of bibliophiles and collectors who value the tactile quality of a physical book and the clarity of a focused reading environment.

The visual style is **High-End Minimalism** with a strong emphasis on **Editorial Typography**. It utilizes generous whitespace to create a sense of "breathing room," mimicking the wide margins of a luxury hardback edition. Subtle border treatments replace heavy shadows to maintain a flat, paper-like depth that feels intentional and refined.

## Colors
The palette is rooted in the physical materials of bookmaking: "Ink" (#1A1A1A) for primary text and core structural elements, and "Paper" (#FDFCF8) for the foundational background. The "Sage" (#8DA399) accent provides a calming, organic counterpoint for secondary actions and success states, while "Terracotta" (#C67B5C) is used sparingly for highlights, notifications, or call-to-actions that require warmth.

Avoid pure blacks or stark whites; the "Ink" and "Paper" combination reduces eye strain and reinforces the literary metaphor. Use subtle variations of the neutral "Paper" color (adding 2-4% darkness) for container backgrounds to define layout sections without introducing harsh lines.

## Typography
The typography system relies on a high-contrast pairing that defines the "Modern Literary" aesthetic. **Bodoni Moda** is used for headlines and display text, evoking the elegance of high-end publishing. Its sharp serifs and extreme stroke contrast require generous line height to maintain its prestigious character.

**Hanken Grotesk** serves as the functional workhorse for body copy and UI components. Its contemporary, geometric clarity ensures readability in long-form descriptions and data-heavy interfaces. Use the uppercase label style with slight tracking for navigation and metadata to create a rhythmic, structured hierarchy that doesn't compete with the serif headlines.

## Layout & Spacing
The design system employs a **Fixed Grid** philosophy for desktop to maintain the feel of a carefully typeset page, while transitioning to a fluid model for mobile devices. Layouts should prioritize vertical rhythm and intentional asymmetry.

- **Desktop:** 12-column grid with a 1280px max-width, centered.
- **Margins:** Generous outer margins (64px+) are essential to the "high-end" feel. 
- **Sectioning:** Use a 10-unit scale (80px) for vertical gaps between major content blocks to emphasize the spaciousness.
- **Negative Space:** Don't fear empty columns; allow content to occupy the center or specific thirds of the grid to create an editorial look.

## Elevation & Depth
Depth is conveyed through **Low-Contrast Outlines** and **Tonal Layers** rather than shadows. This mimics the flat, physical nature of paper and ink.

- **Borders:** Use 1px solid lines in a slightly darkened version of the "Paper" color (#E5E1D8) for card containers and dividers.
- **Tonal Stacking:** Raise elements by switching background colors from the base "Paper" to a pure white (#FFFFFF) or a very light "Sage" tint.
- **Shadows:** Only used in "Ink" (#1A1A1A) at 5-10% opacity with a large blur (20px+) for floating menus or modals to provide a soft, ambient lift without breaking the minimalist aesthetic.

## Shapes
The shape language is primarily **Soft (0.25rem)**. While a sharp edge feels traditional, a very subtle radius introduces a "modern" touch that feels intentional and precision-crafted.

- **Small Components:** Buttons and input fields use a 4px radius.
- **Large Components:** Book covers and featured cards use an 8px (rounded-lg) radius to feel like high-quality bound objects.
- **Interactive States:** Use sharp corners for underlines and decorative accents to maintain the scholarly precision.

## Components
### Buttons
Primary buttons are solid "Ink" (#1A1A1A) with "Paper" (#FDFCF8) text. Secondary buttons utilize a thin 1px "Ink" border with no fill. All buttons should have generous horizontal padding (24px+) to appear elongated and elegant.

### Input Fields
Inputs should be minimalist, using only a bottom border (1px) in a neutral gray until focused. Upon focus, the border transitions to "Sage" (#8DA399). Labels use the `label-md` uppercase style.

### Cards
Cards for books or articles should be flat with a 1px #E5E1D8 border. Imagery within cards should have a "muted" or "atmospheric" filter applied, ensuring that the "Paper" background remains the dominant visual tone.

### Chips & Metadata
Use "Sage" (#8DA399) or "Terracotta" (#C67B5C) as light, transparent background fills for category chips. The text should remain "Ink" for maximum legibility.

### List Items
Lists in a bookstore context (search results, bibliography) should have high vertical padding and be separated by a hairline divider. Hover states should subtly shift the background to a 2% darker "Paper" tint.