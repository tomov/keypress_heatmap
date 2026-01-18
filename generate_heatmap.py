import re
import os
import matplotlib.pyplot as plt
from collections import Counter

# Configuration
LOG_FILE = 'physical_keys_log.txt'
LAYOUT_FILE = 'kinesis_layout.txt'

# Comprehensive mapping for Dvorak layout on Kinesis Advantage2
KEY_MAP = {
    'KEY_A': 'A', 'KEY_B': 'B', 'KEY_C': 'C', 'KEY_D': 'D', 'KEY_E': 'E',
    'KEY_F': 'F', 'KEY_G': 'G', 'KEY_H': 'H', 'KEY_I': 'I', 'KEY_J': 'J',
    'KEY_K': 'K', 'KEY_L': 'L', 'KEY_M': 'M', 'KEY_N': 'N', 'KEY_O': 'O',
    'KEY_P': 'P', 'KEY_Q': 'Q', 'KEY_R': 'R', 'KEY_S': 'S', 'KEY_T': 'T',
    'KEY_U': 'U', 'KEY_V': 'V', 'KEY_W': 'W', 'KEY_X': 'X', 'KEY_Y': 'Y',
    'KEY_Z': 'Z', 'KEY_1': '1', 'KEY_2': '2', 'KEY_3': '3', 'KEY_4': '4',
    'KEY_5': '5', 'KEY_6': '6', 'KEY_7': '7', 'KEY_8': '8', 'KEY_9': '9',
    'KEY_0': '0', 'KEY_EQUAL': '+', 'KEY_MINUS': '-', 'KEY_APOSTROPHE': "'",
    'KEY_COMMA': ',', 'KEY_SEMICOLON': ';', 'KEY_DOT': '.', 'KEY_SLASH': '/',
    'KEY_BACKSLASH': '\\', 'KEY_TAB': 'Tab', 'KEY_CAPSLOCK': 'Caps',
    'KEY_LEFTSHIFT': 'Shft', 'KEY_RIGHTSHIFT': 'Shft', 'KEY_ENTER': 'Entr',
    'KEY_KPENTER': 'Entr', 'KEY_BACKSPACE': 'Bksp', 'KEY_DELETE': 'Del',
    'KEY_SPACE': 'Spc', 'KEY_ESC': 'Esc', 'KEY_LEFT': '<-', 'KEY_RIGHT': '->',
    'KEY_UP': 'Up', 'KEY_DOWN': 'Dn', 'KEY_HOME': 'Home', 'KEY_END': 'End',
    'KEY_PAGEUP': 'PgUp', 'KEY_PAGEDOWN': 'PgDn', 'KEY_LEFTCTRL': 'Ctrl',
    'KEY_LEFTALT': 'Alt', 'KEY_LEFTMETA': 'Cmd', 'KEY_RIGHTMETA': 'Cmd',
    'KEY_GRAVE': '`', 'KEY_LEFTBRACE': '[', 'KEY_RIGHTBRACE': ']'
}

def generate_heatmap():
    if not os.path.exists(LAYOUT_FILE):
        print(f"Error: {LAYOUT_FILE} not found.")
        return

    # 1. Parse Layout and calculate true coordinates
    with open(LAYOUT_FILE, 'r') as f:
        content = f.read()
    
    cleaned_layout = re.sub(r'\\s*', '', content)
    lines = cleaned_layout.split('\n')
    max_width = max(len(line) for line in lines)

    label_to_coords = []
    for row_idx, line in enumerate(lines):
        # Improved regex to find exact matches from our KEY_MAP
        matches = re.finditer(r'[A-Za-z0-9\+\-\'\,\;\.\/\\<>\`\[\]]+', line)
        for m in matches:
            label = m.group()
            if set(label).issubset(set('-_|¯ ')): continue
            
            label_to_coords.append({
                'label': label,
                'row': row_idx,
                'col': (m.start() + m.end()) / 2
            })

    # 2. Process Log Data
    counts = Counter()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            for line in f:
                if ' - ' in line:
                    code = line.split(' - ')[1].strip()
                    counts[code] += 1

    # 3. Visualization Setup
    plt.figure(figsize=(16, 10))
    ax = plt.gca()
    ax.invert_yaxis()

    # Draw the background ASCII underlay character by character for alignment
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char.strip():  # Skip whitespace
                ax.text(j, i, char, family='monospace', color='#d3d3d3',
                        va='center', ha='center', fontsize=10, zorder=1)

    # Prepare scatter data
    plot_x, plot_y, plot_colors, plot_labels = [], [], [], []
    for item in label_to_coords:
        label = item['label']
        total_presses = sum(counts[k] for k, v in KEY_MAP.items() if v == label)
        
        plot_x.append(item['col'])
        plot_y.append(item['row'])
        plot_colors.append(total_presses)
        plot_labels.append(f"{label}\n{total_presses}" if total_presses > 0 else label)

    # 4. Draw Heatmap (Larger Circles)
    # 's' is area in points^2; increased significantly for visibility
    scatter = ax.scatter(plot_x, plot_y, s=1200, c=plot_colors, 
                         cmap='YlOrRd', edgecolors='black', linewidths=1.5,
                         alpha=0.9, zorder=2)
    
    # 5. Overlay Labels
    for x, y, lbl, val in zip(plot_x, plot_y, plot_labels, plot_colors):
        text_color = 'white' if val > (max(plot_colors or [1]) * 0.6) else 'black'
        ax.text(x, y, lbl, ha='center', va='center', fontsize=8, 
                fontweight='bold', color=text_color, zorder=3)

    plt.colorbar(scatter, label='Total Physical Keypresses')
    plt.title("Heatmap: Kinesis Advantage2 Dvorak (Physical Only)", fontsize=15)
    
    # Force axes to match ASCII dimensions to prevent stretching
    plt.xlim(-1, max_width + 1)
    plt.ylim(len(lines), -1)
    plt.axis('off')

    # 6. Output
    plt.savefig('kinesis_heatmap.png', dpi=300, bbox_inches='tight')
    print("Heatmap saved as kinesis_heatmap.png")
    
    # Automatically open the visualization window
    plt.show()

if __name__ == "__main__":
    generate_heatmap()