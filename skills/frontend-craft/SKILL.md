---
name: frontend-craft
description: Design and implement polished, well-crafted user
  interfaces. Use for creating new frontend pages, components,
  dashboards, and substantial visual redesigns. Do not use
  for backend work or purely functional UI bug fixes.
---

# Frontend Craft

Create interfaces that are clear, complete, and quietly
well-crafted.

For product and app UI (settings, tools, dashboards, forms),
clarity and completing the user's task come first; good design
shows through hierarchy, restraint, and handled details, not
through added decoration. Reserve a more distinctive, expressive
direction for marketing, landing, and brand-led pages.

## Design Direction

Before implementation, determine:
- The product's purpose and target users.
- The appropriate visual character.
- The desired information density.
- The primary interaction and visual hierarchy.

Choose a coherent visual direction and commit to it.

## Visual Defaults

Use the project's design tokens when they exist; these are
fallbacks, not overrides.

- Hierarchy: distinguish levels with one lever at a time (size,
  weight, or color); reserve combined emphasis for the single most
  important element. De-emphasize labels and metadata relative
  to values.
- Spacing: use a consistent scale (e.g., 4/8/12/16/24/32/48).
  Gaps between groups must be clearly larger than within groups.
  Density follows the product: tools and data views are compact;
  marketing and reading pages are airier.
- Typography: one family unless the direction calls for a pairing;
  about 4 sizes per screen; tight line height for headings, relaxed
  for body; constrain reading width to ~65ch.
- Color: mostly neutrals with slightly tinted grays; one accent used
  sparingly for primary actions and state. Meet contrast minimums
  (4.5:1 body text, 3:1 large text). Don't rely on color alone.
- Surfaces: separate content with spacing, alignment, and subtle
  dividers before reaching for borders, shadows, or cards. Use
  shadows only for real elevation (menus, popovers, modals).
- Layout: left-align by default; center only short, standalone
  content. Choose proportions based on content, not fixed grids.
- Make interactive states (hover, focus, active, selected, disabled)
  visually clear and consistent.

## Avoid Generic AI Patterns

Unless the context justifies them, avoid:
- Default purple or blue gradient aesthetics.
- Excessive rounded cards and floating panels.
- Unnecessary shadows, borders, and decorative effects.
- Generic dashboard layouts for every application.
- Excessive whitespace in information-dense applications.
- Repeated card grids where tables or lists work better.
- Decorative icons that add no information.

## Content Scope

Build what the task needs; do not add content to make the page
look designed. Unless requested or clearly required, do not add:
- Invented brand chrome: logos, app headers, nav, or footers.
- Taglines, slogans, mood copy, or decorative eyebrow labels.
- Decorative summary stats or metrics.
- Extra banners, tips, or explanatory panels.
- Controls the realistic data size does not need (tabs, filters,
  bulk actions for a short list).

Copy should state function or consequence, not mood. Let users
complete the primary task in the fewest reasonable steps.

## Existing Products

When working in an existing application:
- Preserve its established visual language.
- Reuse its design tokens and component system.
- Do not redesign unrelated screens.
- Favor consistency over novelty.

## Implementation

- Produce working, responsive UI.
- Design loading, empty, error, and disabled states, not only the
  happy path.
- Use realistic content and concise, specific microcopy; no
  placeholder text like "Item 1" or lorem ipsum.
- Handle long text, extreme values, and narrow viewports.
- On narrow viewports, reflow tables and multi-column rows into
  stacked layouts; keep primary actions and controls visible and
  untruncated, without relying on horizontal scrolling.
- Preserve accessibility and keyboard navigation.
- Prefer existing dependencies.
- Avoid unnecessary animation and heavyweight libraries.
- Verify layout, overflow, and interaction states.
- Inspect actual rendered output when preview tools exist.

## Final Quality Check

Evaluate whether:
- The hierarchy is immediately understandable, and still reads
  when blurred or viewed in grayscale.
- The visual style matches the product's purpose.
- Information density is appropriate.
- Every prominent element and line of copy has a functional
  reason to exist; nothing was added only for decoration.
- The interface avoids an obvious template-generated look.
- At ~375px wide, all content and actions remain usable.

Iterate on visible weaknesses when practical.

