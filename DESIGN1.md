```markdown
# Design System Strategy: Industrial Precision & The Kinetic Foundry

## 1. Overview & Creative North Star

This design system is built to bridge the gap between raw industrial utility and high-precision artificial intelligence. Our Creative North Star is **"The Kinetic Foundry."** 

Unlike standard "SaaS-blue" dashboards that feel sterile and templated, this system treats the UI as a high-end control room interface—reminiscent of Unreal Engine 5 HUDs. We move beyond the "flat" web by utilizing **intentional asymmetry**, **glassmorphism**, and **tonal depth**. We are not building a website; we are crafting a digital cockpit for the future of resource management.

The experience is defined by high-contrast typography scales, where massive editorial display type meets hyper-technical monospaced data points, creating a rhythm that feels both authoritative and cutting-edge.

---

## 2. Color & Surface Architecture

The palette is rooted in deep anthracite and "Cyber Black" tones, designed to make the neon accents feel like light sources rather than mere colors.

### The "No-Line" Rule
To achieve a premium, seamless feel, **1px solid borders are strictly prohibited** for sectioning or layout containment. Boundaries must be defined through:
*   **Background Shifts:** Distinguish a sidebar from a main stage by moving from `surface` (#0d141c) to `surface-container-low` (#151c25).
*   **Tonal Transitions:** Use subtle shifts in the surface hierarchy to denote hierarchy without the visual noise of structural lines.

### Surface Hierarchy & Nesting
Treat the UI as physical layers of "Smart Glass."
*   **Base Layer:** `surface_container_lowest` (#080f17) for the global backdrop.
*   **Secondary Layer:** `surface` (#0d141c) for main content areas.
*   **Interactive/Elevated Layer:** `surface_container_high` (#242a34) for floating cards or active modules.
*   **The "Glass & Gradient" Rule:** Use `surface_variant` (#2e353f) at 40-60% opacity with a `20px` backdrop blur for modals and floating nav. Apply a subtle linear gradient (from `primary_container` to `secondary_container`) at 10% opacity to these glass elements to give them a "powered-on" soul.

---

## 3. Typography: The Editorial Tech-Stack

We utilize a dual-typeface system to balance high-end brand appeal with technical precision.

*   **Display & Headlines (Space Grotesk):** This is our "Editorial Voice." Use `display-lg` (3.5rem) with tight letter-spacing for hero metrics. It should feel aggressive, modern, and confident.
*   **Body & Titles (Inter/Outfit):** Our "Communication Voice." Clean, legible, and neutral. Use `title-md` (1.125rem) for section headers to maintain a sophisticated clarity.
*   **Labels & Technical Data (JetBrains Mono):** Our "Engine Voice." All technical readouts, timestamps, and AI confidence scores must use monospaced type. This reinforces the "Cyber-Future" aesthetic and ensures data alignment.

---

## 4. Elevation & Depth

We eschew traditional drop shadows for **Tonal Layering**.

*   **The Layering Principle:** Depth is achieved by "stacking" the surface tiers. A `surface-container-highest` element placed on a `surface` background provides a soft, natural lift that mimics high-end hardware.
*   **Ambient Shadows:** When an element must float (e.g., a critical alert), use a highly diffused shadow: `blur: 40px`, `spread: -5px`, `color: rgba(0, 255, 170, 0.08)`. The shadow color must match the `surface_tint` to simulate ambient light bleed from neon elements.
*   **The "Ghost Border":** For elements requiring high definition (like input fields), use the `outline_variant` (#3a4a40) at **15% opacity**. This provides a "hint" of a boundary that feels integrated into the glass surface.
*   **Corner Treatment:** All main containers must use the **xl (20px)** radius. Small utility components (chips/tooltips) use the **sm (4px)** radius to maintain a technical, sharp edge.

---

## 5. Components

### Buttons
*   **Primary:** High-impact. Background: `primary_container` (#00ffaa). Text: `on_primary_container`. Give it a `0 0 15px rgba(0, 255, 170, 0.4)` outer glow on hover to simulate a neon power-up.
*   **Secondary:** Glass-style. `surface_variant` at 20% opacity with a `Ghost Border`.
*   **Tertiary:** Text-only in `JetBrains Mono` with an underline that appears only on hover.

### Input Fields
*   **Structure:** No background fill. Use a `Ghost Border` on the bottom edge only.
*   **Labels:** Use `label-md` in `JetBrains Mono` with 1px tracking, always in uppercase for a "HUD" feel.
*   **Active State:** The bottom border transforms into a `primary` (#f6fff6) 2px line with a soft neon glow.

### Cards & Lists
*   **The "Anti-List" Rule:** Forbid the use of divider lines. Separate list items using `8px` of vertical white space and a 2% background shift on hover.
*   **Data Cards:** Use `surface_container_low` with a 20px radius. The top-right corner should feature a "Technical Tag" (e.g., a JetBrains Mono chip) indicating the AI status.

### AI Status Chips
*   **Active/Success:** Background: `primary_fixed_dim` (#00e296) at 10% opacity. Border: 1px `primary_fixed` at 20% opacity. Text: `primary_fixed`.
*   **Alert/Error:** Background: `error_container` at 10% opacity. Text: `error`.

---

## 6. Do's and Don'ts

### Do:
*   **Embrace Asymmetry:** Let a metric card span 60% of the grid while its neighbor spans 40%. This feels custom and intentional.
*   **Use Mono for Numbers:** Always use `JetBrains Mono` for numeric values to ensure they look like live data-stream readouts.
*   **Layer Glass:** Use backdrop-blur on overlapping elements to create "optical thickness."

### Don't:
*   **Don't use 100% White:** Use `primary` (#f6fff6) or `on_surface` (#dce3ef) for text. Pure #FFFFFF is too harsh for an industrial dark mode.
*   **Don't use standard Shadows:** Avoid the "Photoshop Drop Shadow" look. If it doesn't look like light glowing from a screen, don't use it.
*   **No "Boxy" Grids:** Avoid perfectly even 4x4 grids. Group related data into "clusters" using tonal shifts to make the UI feel like a bespoke instrument panel.

---

## 7. Signature Interaction Pattern
When an element is clicked, trigger a brief "system pulse"—a subtle, rapid expansion of a low-opacity `primary_container` ring. This reinforces the SmartRecycle AI's "Industrial Cyber" persona, making the dashboard feel reactive and alive.```