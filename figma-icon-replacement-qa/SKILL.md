---
name: figma-icon-replacement-qa
description: Replace and refine icons in the user's currently selected Figma page/frame using supplied SVG resources, with strict visual consistency, zoom QA, and SVG asset packaging.
metadata:
  short-description: Figma icon replacement QA
---

# Figma Icon Replacement QA

Use this skill when the user wants icons replaced or refined in a currently selected Figma page/frame, especially when they reference previous requirements for SolaStyle/LONGi page icon work.

## Core Contract

- Treat the user's current Figma selection as the work scope unless they explicitly name another frame or page.
- Replace only the old icons the user marks or describes. Do not change text, fonts, font sizes, colors, layout, spacing, cards, navigation, backgrounds, images, or unrelated icons.
- If the user numbers icons in a screenshot, preserve that numbering in your plan, implementation notes, and final summary.
- If any meaning, target, color, replacement range, or asset choice is unclear, ask before editing. Do not guess.
- Prefer the user's supplied icon resource package. Choose icons by semantic fit first, then refine them into a unified visual system.
- If no suitable supplied SVG exists, tell the user which icon is missing and offer search keywords or generate a clean editable SVG only after the user agrees or asks.

## Selection And Replacement

Before editing Figma:

- Inspect the selected Figma frame/page and identify the exact icon node IDs, container sizes, and module grouping.
- Inspect the supplied SVG resource package when provided.
- Match each old icon to the best replacement by meaning, not merely by original file style.
- When multiple candidate SVGs could fit, prefer the one whose silhouette communicates the module best and can be simplified into the same style as its neighbors.

When replacing:

- Keep each icon inside its original icon container unless the user explicitly asks to move the area.
- Preserve the original icon area's position and size.
- Preserve existing background shapes such as pale red circles unless the user asks to replace them.
- Use editable SVG/vector content, not raster images.
- Return all mutated and created Figma node IDs from every write operation.

## Visual Consistency Requirements

For icons in the same module, make these visually consistent:

- Stroke thickness, linecap, linejoin, corner radius, and endpoint treatment.
- Overall visual size, not only numeric width and height.
- Complexity and detail density. Avoid one icon being overly detailed while another is too simple.
- Large position inside the container: icons should sit on the same optical center.
- Small distances around the icon: top, bottom, left, right padding should feel balanced.
- Distance from icon to background circle, text, card edges, and neighboring icons.
- Color, including required red/black variants. Use the page's existing color behavior unless the user specifies a color.

For red support/homepage icons, keep the red consistent with the existing site icon red when known: `#E50914`.

## Refinement Standards

Refine SVGs when needed:

- Remove rough protruding segments, accidental overlaps, broken joins, floating pieces, and jagged-looking corners.
- Avoid stroke intersections that make small icons look filled or muddy.
- Use masks or background-colored fills carefully only when needed to create clean cutouts, such as hollow vehicle wheels.
- Make vehicle wheels visibly hollow when requested. Wheel centers must not be crossed by body or axle strokes.
- Simplify overly complex source icons so they match the module's visual density.
- Avoid copying a reference icon exactly when the user says it is only a proportion/style reference.

## QA Before Finishing

Do not finish immediately after replacement. Perform a self-check first:

- Capture an overall screenshot of the module.
- Inspect at least the changed icon containers at higher zoom or by node bounds/stroke data.
- Confirm no icon exceeds its original container unless explicitly intended.
- Confirm strokes are consistent and there are no negative offsets, out-of-frame edges, clipped lines, rough protrusions, disconnected segments, or accidental filled-looking areas.
- Confirm icon-to-text and icon-to-background spacing still matches the module.
- If the visual check reveals an issue, fix it before final response.

Only claim visual QA that was actually performed.

## Asset Packaging

After finalizing replacements:

- Save the actual final SVGs used in Figma into the user's requested icon folder.
- If no folder is specified, ask for the folder before writing outside the workspace.
- Use clear filenames that map to the page/module and icon meaning.
- Keep SVGs editable, with explicit `viewBox`, `fill="none"` for line icons where appropriate, and consistent stroke settings.
- Validate SVG syntax when possible, for example with `xmllint --noout`.

## Final Response

Keep the final response concise and concrete:

- List which numbered icons changed and what they changed to.
- State what was intentionally left untouched.
- Mention the self-check performed.
- Provide a clickable link to the final SVG folder or files when assets were written.
