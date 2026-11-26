import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk

# 1. COLORS AND FONT
PEACH_BG = "#10489C"
PEACH_PANEL = "#EAF1F8"
PEACH_BUTTON = "#8DC3FC"
PEACH_HOVER = "#8FAFD3"
TEXT_COLOR = "#183153"
FONT_MAIN = ("Arial", 10, "bold")

# 2. WINDOW AND CANVAS SETTINGS
CANVAS_WIDTH = 900
CANVAS_HEIGHT = 550

root = tk.Tk()
root.title("My Paint Application")
root.geometry("1000x760")
root.configure(bg=PEACH_BG)

canvas_frame = tk.Frame(root, bg=PEACH_BUTTON, padx=4, pady=4)
canvas_frame.pack(padx=20, pady=12)

canvas = tk.Canvas(
    canvas_frame,
    width=CANVAS_WIDTH,
    height=CANVAS_HEIGHT,
    bg="white",
    cursor="cross",
    highlightthickness=0
)
canvas.pack()

# Pillow image is the permanent drawing used for saving.
image = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), "white")
draw = ImageDraw.Draw(image)
canvas_image = None

# 3. DRAWING SETTINGS
current_color = "black"
brush_size = 5
tool = "brush"
start_x = start_y = None
stroke_points = []
stroke_item = None
preview_shape = None

undo_history = []
MAX_UNDO = 30
fill_shapes = tk.BooleanVar(master=root, value=False)


# 4. HELPER FUNCTIONS
def save_undo_state():
    """Save the current image before a new drawing action."""
    undo_history.append(image.copy())

    if len(undo_history) > MAX_UNDO:
        undo_history.pop(0)


def undo():
    """Restore the image from before the latest action."""
    global image, draw, preview_shape, stroke_item, stroke_points

    if undo_history:
        image = undo_history.pop()
        draw = ImageDraw.Draw(image)

        preview_shape = None
        stroke_item = None
        stroke_points = []

        refresh_canvas()

    else:
        messagebox.showinfo("Undo", "There is no action to undo.")


def set_color(new_color):
    global current_color

    current_color = new_color
    color_button.config(bg=current_color)


def choose_color():
    selected = colorchooser.askcolor(title="Choose a color")

    if selected[1] is not None:
        set_color(selected[1])


def set_tool(selected_tool):
    global tool
    tool = selected_tool


def change_brush_size(value):
    global brush_size
    brush_size = int(float(value))


def get_triangle_points(x1, y1, x2, y2):
    """Return the three corners of a triangle based on the drag area."""
    middle_x = (x1 + x2) // 2

    return [
        (middle_x, y1),
        (x2, y2),
        (x1, y2)
    ]


# 5. MOUSE DRAWING FUNCTIONS
def start_drawing(event):
    """Start a new brush stroke or shape."""
    global start_x, start_y, stroke_points
    global stroke_item, preview_shape

    start_x, start_y = event.x, event.y

    stroke_points = []
    stroke_item = None
    preview_shape = None

    # Save one undo point for every new drawing action.
    save_undo_state()

    if tool in ("brush", "eraser"):

        stroke_points = [(event.x, event.y)]

        color = "white" if tool == "eraser" else current_color

        stroke_item = canvas.create_line(
            event.x, event.y, event.x, event.y,
            fill=color,
            width=brush_size,
            capstyle=tk.ROUND,
            joinstyle=tk.ROUND
        )


def draw_motion(event):
    """Update the brush stroke or shape preview while dragging."""
    global stroke_points

    if tool in ("brush", "eraser"):

        if stroke_item is None:
            return

        stroke_points.append((event.x, event.y))

        coordinates = [
            value
            for point in stroke_points
            for value in point
        ]

        canvas.coords(stroke_item, *coordinates)

    else:
        preview_shape_drawing(event)


# 6. SHAPE PREVIEW
def preview_shape_drawing(event):
    """Display a temporary preview of the selected shape."""
    global preview_shape

    if preview_shape is not None:
        canvas.delete(preview_shape)
        preview_shape = None

    outline_width = brush_size

    shape_fill = current_color if fill_shapes.get() else ""

    if tool == "line":

        preview_shape = canvas.create_line(
            start_x, start_y, event.x, event.y,
            fill=current_color,
            width=outline_width
        )

    elif tool == "rectangle":

        preview_shape = canvas.create_rectangle(
            start_x, start_y, event.x, event.y,
            outline=current_color,
            fill=shape_fill,
            width=outline_width
        )

    elif tool == "oval":

        preview_shape = canvas.create_oval(
            start_x, start_y, event.x, event.y,
            outline=current_color,
            fill=shape_fill,
            width=outline_width
        )

    elif tool == "triangle":

        points = get_triangle_points(
            start_x, start_y, event.x, event.y
        )

        flat_points = [
            value
            for point in points
            for value in point
        ]

        preview_shape = canvas.create_polygon(
            flat_points,
            outline=current_color,
            fill=shape_fill,
            width=outline_width
        )


# 7. FINISH DRAWING
def finish_drawing(event):
    """Save the completed brush stroke or shape to the Pillow image."""

    global preview_shape, stroke_points, stroke_item
    global start_x, start_y

    if start_x is None or start_y is None:
        return

    # BRUSH AND ERASER
    if tool in ("brush", "eraser"):

        color = "white" if tool == "eraser" else current_color

        if not stroke_points:
            stroke_points = [(start_x, start_y)]

        if stroke_points[-1] != (event.x, event.y):
            stroke_points.append((event.x, event.y))

        coordinates = [
            value
            for point in stroke_points
            for value in point
        ]

        if len(stroke_points) == 1:

            x, y = stroke_points[0]
            radius = brush_size / 2

            draw.ellipse(
                (
                    x - radius,
                    y - radius,
                    x + radius,
                    y + radius
                ),
                fill=color
            )

        else:

            draw.line(
                coordinates,
                fill=color,
                width=brush_size,
                joint="curve"
            )

            radius = brush_size / 2

            for x, y in (stroke_points[0], stroke_points[-1]):

                draw.ellipse(
                    (
                        x - radius,
                        y - radius,
                        x + radius,
                        y + radius
                    ),
                    fill=color
                )

        stroke_points = []
        stroke_item = None

        refresh_canvas()

        start_x = start_y = None

        return

    # SHAPE SETTINGS
    outline_width = brush_size

    shape_fill = current_color if fill_shapes.get() else None

    box = (
        start_x,
        start_y,
        event.x,
        event.y
    )

    # LINE
    if tool == "line":

        draw.line(
            box,
            fill=current_color,
            width=outline_width
        )

    # RECTANGLE
    elif tool == "rectangle":

        draw.rectangle(
            box,
            outline=current_color,
            fill=shape_fill,
            width=outline_width
        )

    # OVAL
    elif tool == "oval":

        draw.ellipse(
            box,
            outline=current_color,
            fill=shape_fill,
            width=outline_width
        )

    # TRIANGLE
    elif tool == "triangle":

        points = get_triangle_points(
            start_x, start_y, event.x, event.y
        )

        draw.polygon(
            points,
            fill=shape_fill,
            outline=current_color,
            width=outline_width
        )

    preview_shape = None

    refresh_canvas()

    start_x = start_y = None


# 8. CANVAS MANAGEMENT
def refresh_canvas():
    """Display the saved Pillow image on the Tkinter canvas."""
    global canvas_image

    canvas.delete("all")

    canvas_image = ImageTk.PhotoImage(image)

    canvas.create_image(
        0, 0,
        anchor="nw",
        image=canvas_image
    )


def clear_canvas():
    """Ask before clearing the drawing."""

    global image, draw, preview_shape
    global stroke_points, stroke_item

    answer = messagebox.askyesno(
        "Clear Canvas",
        "Are you sure you want to clear the canvas?"
    )

    if answer:

        save_undo_state()

        image = Image.new(
            "RGB",
            (CANVAS_WIDTH, CANVAS_HEIGHT),
            "white"
        )

        draw = ImageDraw.Draw(image)

        preview_shape = None
        stroke_points = []
        stroke_item = None

        refresh_canvas()


# 9. OPEN AND SAVE IMAGE
def open_image():

    global image, draw

    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.bmp")
        ]
    )

    if file_path:

        try:

            opened_image = Image.open(file_path).convert("RGB")

            opened_image = opened_image.resize(
                (CANVAS_WIDTH, CANVAS_HEIGHT)
            )

            save_undo_state()

            image = opened_image

            draw = ImageDraw.Draw(image)

            refresh_canvas()

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Could not open image:\n{error}"
            )


def save_image():

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",

        filetypes=[
            ("PNG Image", "*.png"),
            ("JPEG Image", "*.jpg"),
            ("Bitmap Image", "*.bmp")
        ]
    )

    if file_path:

        try:

            image.save(file_path)

            messagebox.showinfo(
                "Saved",
                "Your drawing has been saved!"
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Could not save image:\n{error}"
            )


# 10. BUTTON DESIGN
def make_button(parent, text, command):

    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=PEACH_BUTTON,
        fg=TEXT_COLOR,
        activebackground=PEACH_HOVER,
        activeforeground=TEXT_COLOR,
        font=FONT_MAIN,
        relief="flat",
        padx=9,
        pady=4,
        cursor="hand2"
    )


def make_quick_color_button(parent, text, color):

    text_color = TEXT_COLOR if color == "yellow" else "white"

    return tk.Button(
        parent,
        text=text,
        command=lambda selected_color=color: set_color(selected_color),
        bg=color,
        fg=text_color,
        activebackground=color,
        font=FONT_MAIN,
        relief="raised",
        padx=5,
        pady=4,
        cursor="hand2"
    )


# 11. TOOLBAR
toolbar = tk.Frame(
    root,
    bg=PEACH_PANEL,
    padx=8,
    pady=8
)

toolbar.pack(pady=5)

tool_row = tk.Frame(toolbar, bg=PEACH_PANEL)
tool_row.pack()

color_row = tk.Frame(toolbar, bg=PEACH_PANEL)
color_row.pack(pady=(6, 0))


# DRAWING TOOLS
make_button(
    tool_row, "Brush",
    lambda: set_tool("brush")
).pack(side="left", padx=3)

make_button(
    tool_row, "Eraser",
    lambda: set_tool("eraser")
).pack(side="left", padx=3)

make_button(
    tool_row, "Line",
    lambda: set_tool("line")
).pack(side="left", padx=3)

make_button(
    tool_row, "Rectangle",
    lambda: set_tool("rectangle")
).pack(side="left", padx=3)

make_button(
    tool_row, "Oval",
    lambda: set_tool("oval")
).pack(side="left", padx=3)

make_button(
    tool_row, "Triangle",
    lambda: set_tool("triangle")
).pack(side="left", padx=3)


# BRUSH SIZE
tk.Label(
    tool_row,
    text="Brush Size:",
    bg=PEACH_PANEL,
    fg=TEXT_COLOR,
    font=FONT_MAIN
).pack(side="left", padx=(8, 3))


size_slider = tk.Scale(
    tool_row,
    from_=1,
    to=100,
    orient="horizontal",
    command=change_brush_size,
    length=125,
    bg=PEACH_PANEL,
    fg=TEXT_COLOR,
    troughcolor=PEACH_BUTTON,
    highlightthickness=0
)

size_slider.set(5)
size_slider.pack(side="left", padx=3)


# FILL SHAPES CHECKBOX
fill_checkbox = tk.Checkbutton(
    tool_row,
    text="Fill Shapes",
    variable=fill_shapes,
    bg=PEACH_PANEL,
    fg=TEXT_COLOR,
    activebackground=PEACH_PANEL,
    selectcolor=PEACH_BUTTON,
    font=FONT_MAIN
)

fill_checkbox.pack(side="left", padx=5)


# QUICK COLORS
tk.Label(
    color_row,
    text="Quick Colors:",
    bg=PEACH_PANEL,
    fg=TEXT_COLOR,
    font=FONT_MAIN
).pack(side="left", padx=(2, 4))


make_quick_color_button(
    color_row, "Black", "black"
).pack(side="left", padx=2)

make_quick_color_button(
    color_row, "Red", "red"
).pack(side="left", padx=2)

make_quick_color_button(
    color_row, "Blue", "blue"
).pack(side="left", padx=2)

make_quick_color_button(
    color_row, "Green", "green"
).pack(side="left", padx=2)

make_quick_color_button(
    color_row, "Yellow", "yellow"
).pack(side="left", padx=2)

make_quick_color_button(
    color_row, "Purple", "purple"
).pack(side="left", padx=2)


# OTHER BUTTONS
color_button = make_button(
    color_row,
    "Choose Color",
    choose_color
)

color_button.pack(side="left", padx=(6, 2))


make_button(
    color_row, "Undo", undo
).pack(side="left", padx=2)

make_button(
    color_row, "Clear", clear_canvas
).pack(side="left", padx=2)

make_button(
    color_row, "Open", open_image
).pack(side="left", padx=2)

make_button(
    color_row, "Save", save_image
).pack(side="left", padx=2)


# 12. MOUSE EVENTS AND SHORTCUTS
canvas.bind("<Button-1>", start_drawing)
canvas.bind("<B1-Motion>", draw_motion)
canvas.bind("<ButtonRelease-1>", finish_drawing)

root.bind("<Control-z>", lambda event: undo())


# 13. RUN APPLICATION
refresh_canvas()

root.mainloop()