import streamlit as st
import numpy as np
import random
import time

# Configuration
GRID_WIDTH = 40
GRID_HEIGHT = 40
CELL_SIZE = 15
UPDATE_INTERVAL = 0.05  # Higher frame rate (20 FPS)

# Initialize session state
if 'positions' not in st.session_state:
    st.session_state.positions = set()
if 'playing' not in st.session_state:
    st.session_state.playing = False
if 'generation' not in st.session_state:
    st.session_state.generation = 0

def gen(num):
    """Generate random alive cells"""
    return set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])

def get_neighbors(pos):
    """Get all neighbors of a cell"""
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx >= GRID_WIDTH:
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy >= GRID_HEIGHT:
                continue
            if dx == 0 and dy == 0:
                continue
            neighbors.append((x + dx, y + dy))
    return neighbors

def adjust_grid(positions):
    """Calculate next generation based on Conway's rules"""
    all_neighbors = set()
    new_positions = set()

    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)
        alive_neighbors = [n for n in neighbors if n in positions]
        
        if len(alive_neighbors) in [2, 3]:
            new_positions.add(position)
    
    for position in all_neighbors:
        neighbors = get_neighbors(position)
        alive_neighbors = [n for n in neighbors if n in positions]
        
        if len(alive_neighbors) == 3:
            new_positions.add(position)
    
    return new_positions

def create_grid_svg(positions):
    """Create SVG representation of the grid"""
    width = GRID_WIDTH * CELL_SIZE
    height = GRID_HEIGHT * CELL_SIZE
    
    svg = f'<svg width="{width}" height="{height}" style="border: 2px solid black;">'
    
    # Draw grid background
    svg += f'<rect width="{width}" height="{height}" fill="#808080"/>'
    
    # Draw alive cells in green
    for col, row in positions:
        x = col * CELL_SIZE
        y = row * CELL_SIZE
        svg += f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" fill="#00FF00"/>'
    
    # Draw grid lines
    for i in range(GRID_HEIGHT + 1):
        y = i * CELL_SIZE
        svg += f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="black" stroke-width="1"/>'
    
    for i in range(GRID_WIDTH + 1):
        x = i * CELL_SIZE
        svg += f'<line x1="{x}" y1="0" x2="{x}" y2="{height}" stroke="black" stroke-width="1"/>'
    
    svg += '</svg>'
    return svg

def main():
    st.set_page_config(page_title="Conway's Game of Life", layout="centered")
    st.title("🎮 Conway's Game of Life")
    
    # Instructions in collapsible expander
    with st.expander("ℹ️ Instructions ", expanded=False):
        st.markdown("""
        ### How to use:
        - **Start/Pause**: Toggle the simulation on/off
        - **Stop**: Stop and clear the grid
        - **Random**: Generate random pattern
        - **Clear**: Clear all cells
        - **Click cells below**: Toggle individual cells alive/dead (when paused)
        
        ### Conway's Game of Life Rules:
        1. Any live cell with 2-3 neighbors survives
        2. Any dead cell with exactly 3 neighbors becomes alive
        3. All other cells die or stay dead
        """)
    
    st.markdown("---")
    
    # Control buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        button_text = "⏸️ Pause" if st.session_state.playing else "▶️ Start"
        if st.button(button_text, use_container_width=True):
            st.session_state.playing = not st.session_state.playing
    
    with col2:
        if st.button("⏹️ Stop", use_container_width=True):
            st.session_state.playing = False
            st.session_state.positions = set()
            st.session_state.generation = 0
    
    with col3:
        if st.button("🎲 Random", use_container_width=True):
            st.session_state.positions = gen(random.randrange(200, 400))
            st.session_state.generation = 0
    
    with col4:
        if st.button("🔄 Clear", use_container_width=True):
            st.session_state.positions = set()
            st.session_state.generation = 0
    
    # Display generation counter
    st.write(f"**Generation:** {st.session_state.generation} | **Alive Cells:** {len(st.session_state.positions)} | **Status:** {'▶️ Playing' if st.session_state.playing else '⏸️ Paused'}")
    
    # Display grid
    grid_placeholder = st.empty()
    
    # Game loop
    if st.session_state.playing:
        st.session_state.positions = adjust_grid(st.session_state.positions)
        st.session_state.generation += 1
        grid_placeholder.markdown(create_grid_svg(st.session_state.positions), unsafe_allow_html=True)
        time.sleep(UPDATE_INTERVAL)
        st.rerun()
    else:
        grid_placeholder.markdown(create_grid_svg(st.session_state.positions), unsafe_allow_html=True)

if __name__ == "__main__":
    main()