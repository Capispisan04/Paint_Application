
# Paint_Application

## REQUIREMENTS COMPLETED:

Whole UI Design:
![Whole Code](Screenshots/Screenshot%202026-11-27%20015557.png)


### ✓ Bigger Brush Range

What I did here was increase the maximum brush size from 30 to 100. Originally, the brush size slider only allowed users to select a value between 1 and 30. I changed the maximum value to 100 so users can draw with thicker brush strokes.

**Original Code:**


![Snippet of the original code:](Screenshots/old_brush_range.png)


To increase the brush size range, I simply changed the `to` value from `30` to `100`.
new_brush_range.png

**Updated Code:**


![Updated code:](Screenshots/new_brush_range.png)


**Result:**

![Result:](Screenshots/Result.png)


### ✓ Undo Button

I added an Undo button so that users can reverse their most recent drawing action. This feature was not available in the original application. With this improvement, users can easily undo a drawing if they make a mistake without having to clear the entire canvas.

**Code:**

![Undo Code](Screenshots/undo_code.png)


**Result:**

![Undo Button Result](Screenshots/Undo_button.png)

### ✓ Filled Shapes

I added a feature that allows users to create filled shapes instead of drawing only their outlines. Users can now draw solid rectangles and ovals, making the drawing application more useful and flexible.

**Fill Code:**

![Filled Shapes Code](Screenshots/fill_code.png)

**Result:**

![Filled Shapes Result](Screenshots/fill_function.png)


### ✓ Triangle Tool

I added a Triangle Tool that allows users to draw triangle shapes on the canvas. Users can select the Triangle button and drag their mouse to create a triangle. This gives users another shape option aside from lines, rectangles, and ovals.

**Code:**

![Triangle Tool Code](Screenshots/triangle_code.png)

**Result:**

![Triangle Tool Result](Screenshots/triangle_result.png)

### ✓ Confirm Before Clearing

**Example:**

I improved the existing Clear function by adding a confirmation dialog before removing the drawing. In the original application, clicking the Clear button immediately erased everything on the canvas. I added a confirmation message asking users if they really want to clear their drawing. This helps prevent accidental deletion.

**Original Code:**

![Original Clear Function](Screenshots/old_clear.png)

**Updated Code:**

![Updated Clear Function](Screenshots/clear_code.png)

**Result:**

![Clear Confirmation Result](Screenshots/clear_confirmation.png)


### ✓ Quick Colors

I added Quick Colors buttons to make color selection easier and faster. In the original application, users had to click the Choose Color button and select a color from the color picker. With this improvement, users can now select commonly used colors directly from the toolbar, such as Black, Red, Blue, Green, Yellow, and Purple.

**Updated Code:**

![Quick Colors Code](Screenshots/quick_color_code.png)

**Result:**

![Quick Colors Result](Screenshots/quick_color.png)
