# main.py
from fasthtml.common import *
import json # needed for hx_vals

GRID_ROWS = GRID_COLS = 9
COLORS = ["#FFFFFF", "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#CCCCCC", "#FF00FF", "#00FFFF", "#FFA500"] 
DEFAULT_COLOR = COLORS[0]
colormap = {color: i for i, color in enumerate(COLORS)}
mapcolor = {i:color for i, color in enumerate(COLORS)}

grid_state = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
app, rt = fast_app()

def create_cell(row: int, col: int, current_color: str = DEFAULT_COLOR):
    return Td(Div(id=f"val-{row}-{col}"),
        style=f"background-color: {current_color}; border: 1px solid black; width: 50px; height: 50px; cursor: pointer;",
        hx_post="/color-cell",
        hx_swap="outerHTML",
        hx_include="[name='selected_color']:checked", 
        hx_vals=json.dumps({"row": row, "col": col}))

@rt("/")
def get():
    color_selector = Group(
        H4("Choose Color:"),
        *[Label(
            Input(type="radio", name="selected_color", value=color, checked=(color == DEFAULT_COLOR)),
            Span(style=f"display: inline-block; width: 20px; height: 20px; background-color: {color}; vertical-align: middle;")
            ) for color in COLORS])
    grid_table = Table(
        *[Tr(*[create_cell(r, c, mapcolor[grid_state[r][c]]) for c in range(GRID_COLS)]) for r in range(GRID_ROWS)])
    return Titled("Queens solver", color_selector, grid_table, Button("Solve", hx_get="/solve", hx_swap="outerHTML"))

@rt("/color-cell")
def post(selected_color: str, row: int, col: int):
    print(f"Coloring cell ({row},{col}) with {selected_color}") # Log to console
    grid_state[row][col] = colormap[selected_color]
    return create_cell(row, col, current_color=selected_color)

def solve_queens(board, regions, row=0, n=None, cols=None, regions_used=None, last_col=None):
    """curtosy: deepseek v3"""
    if n is None:
        n = len(board)
    if cols is None:
        cols = set()
    if regions_used is None:
        regions_used = set()

    if row == n:
        return True  # All queens placed successfully

    for col in range(n):
        region = regions[row][col]
        # Check column, region, and neighboring column constraints
        if (col not in cols and 
            region not in regions_used and 
            (last_col is None or abs(col - last_col) > 1)):  # Neighboring column check
            board[row][col] = 'Q'  # Place queen
            cols.add(col)
            regions_used.add(region)

            if solve_queens(board, regions, row + 1, n, cols, regions_used, col):
                return True  # Solution found

            # Backtrack
            board[row][col] = '.'
            cols.remove(col)
            regions_used.remove(region)

    return False  # No solution for this path

@rt("/solve")
def get():
    board = [['.' for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    solve_queens(board, grid_state)
    return [
        Div("♛", style="color:black; font-weight:bold", id=f"val-{r}-{c}", hx_swap_oob="true", hx_swap='outerHTML')
        for r in range(GRID_ROWS)
        for c in range(GRID_COLS) if board[r][c] == 'Q']

serve()