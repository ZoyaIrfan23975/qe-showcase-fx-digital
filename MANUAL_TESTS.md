# Manual Test Pack - StreamDemo

These cases are deliberately **not automated**. Each one either requires human
judgement (does it *look* right, does it *feel* right) or tests something a
browser-based Playwright script cannot meaningfully assert on.

---

### MT-01: Focus visibility on dark backgrounds
**Area:** Accessibility / visual
**Steps:**
1. Open the app and press Tab repeatedly through every interactive element (search box, toggles, buttons)
2. Observe the browser's default focus outline as it moves

**Expected:** The outline should be clearly visible against the app's background at every stop.
**Why manual:** A script can assert an element *has* focus, but not whether a human eye can actually see the outline. This is a judgement call, especially relevant for a CTV product viewed from a couch a few metres from the screen.

---

### MT-02: D-pad-style arrow-key navigation between show cards
**Area:** CTV navigation
**Steps:**
1. Load the app, do not click into any text field
2. Press the Left/Right/Up/Down arrow keys
3. Observe whether focus moves between show cards

**Expected/Actual finding:** Currently, arrow keys only affect the numeric progress input's native spinner - there is no custom D-pad-style navigation between show cards.
**Why manual:** This is a genuine gap worth flagging rather than automating a test for a feature that doesn't exist. Real TV remotes are D-pad driven, not Tab driven, so this is a real risk to note for a CTV product, not a synthetic one.

---

### MT-03: Continue Watching row with many shows (overflow behaviour)
**Area:** Visual layout
**Steps:**
1. Set progress on all 5 shows to a value between 1-99% (so all appear in Continue Watching)
2. Observe how the row lays out - scrolling, wrapping, or cut-off cards

**Expected:** Content should remain legible and usable, however it overflows.
**Why manual:** "Does this look broken or intentional" is a subjective visual judgement call a script can't make - it can only confirm elements exist in the DOM, not whether the layout reads as coherent to a viewer.

---

### MT-04: Download button visual state clarity
**Area:** Visual / UX
**Steps:**
1. Toggle Premium and Storage on and off in different combinations
2. Watch the Download button as it becomes enabled/disabled each time

**Expected:** It should be immediately, visually obvious which state the button is in - not just technically enabled/disabled in the DOM.
**Why manual:** The automated decision-table tests already confirm the *logic* is correct (enabled/disabled at the right times). This case checks something different: whether a real user would visually notice the difference at a glance, which is a design/perception judgement, not a logic check.

---

### MT-05: Empty-state message tone and clarity
**Area:** Content / UX writing
**Steps:**
1. Search for a show that doesn't exist
2. Read the "no results" message shown

**Expected:** Message should read naturally and helpfully, not just "be present."
**Why manual:** The automated test already confirms the message *appears*. Whether its wording is clear, friendly, and on-brand is a judgement call about tone, not something a script can meaningfully assert.

---

### MT-06: Responsive layout at different window sizes
**Area:** Visual layout
**Steps:**
1. Resize the browser window to a few different widths/aspect ratios (e.g. simulating a widescreen TV vs a smaller monitor)
2. Observe whether the show grid, buttons, and text remain usable and readable at each size

**Expected:** No overlapping elements, no text or buttons cut off.
**Why manual:** Visual layout breakage is exactly the kind of thing exploratory, human-eye testing catches fastest - an automated check would need a screenshot-diff tool and a defined baseline per breakpoint, which is disproportionate effort for a demo app at this stage.
