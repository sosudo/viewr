import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Define custom "warmrainbow" colormap
warmrainbow = LinearSegmentedColormap.from_list(
    "warmrainbow", ["#ffffcc", "#ffcc00", "#ff6600", "#cc0000"], N=256
)

# Ask for input file
tfile = input("Input file name: ")

labeling = input("Label grid? (y/n): ")

if labeling == "n":
  label = False
else:
  label = True

# Read data
with open(tfile, 'r') as f:
    r = f.readlines()
    out = list(map(lambda s: list(map(int, s.split())), r))  # DO NOT CHANGE
npout = np.array(out)
rows, cols = npout.shape

highlight = input("Highlight min/max values? (y/n): ")

if highlight == 'y':
    min_val = npout.min()
    max_val = npout.max()

# Optional: axis labels
x_labels = [f"" for _ in range(cols)]
y_labels = [f"" for _ in range(rows)]

# Add our custom colormap to the list
available_cmaps = {
    "viridis": plt.cm.viridis,
    "plasma": plt.cm.plasma,
    "inferno": plt.cm.inferno,
    "magma": plt.cm.magma,
    "cividis": plt.cm.cividis,
    "Blues": plt.cm.Blues,
    "Greens": plt.cm.Greens,
    "Reds": plt.cm.Reds,
    "Purples": plt.cm.Purples,
    "Spectral": plt.cm.Spectral,
    "coolwarm": plt.cm.coolwarm,
    "seismic": plt.cm.seismic,
    "ocean": plt.cm.ocean,
    "terrain": plt.cm.terrain,
    "hasitakv": warmrainbow
}

print("Available color schemes:")
print(", ".join(available_cmaps.keys()))

cmap_name = input("Choose a colormap: ").strip()
if cmap_name not in available_cmaps:
    print(f"'{cmap_name}' not recognized. Using default: 'hasitakv'")
    cmap_name = "warmrainbow"

cmap = available_cmaps[cmap_name]

# Create figure and axis
fig, ax = plt.subplots(figsize=(cols * 0.6 + 2, rows * 0.6 + 2))

# Heatmap
if not label:
    im = ax.imshow(npout, cmap=cmap, interpolation='none')
else:
    im = ax.imshow(npout, cmap=cmap)

# Colorbar
cbar = ax.figure.colorbar(im, ax=ax)
cbar.ax.set_ylabel("Value", rotation=-90, va="bottom", fontsize=12)

# Ticks and grid
ax.set_xticks(np.arange(cols))
ax.set_yticks(np.arange(rows))
ax.set_xticklabels(x_labels, fontsize=10, rotation=45, ha="right", rotation_mode="anchor")
ax.set_yticklabels(y_labels, fontsize=10)

for edge in ax.spines.values():
    edge.set_visible(False)

if label:
    ax.set_xticks(np.arange(cols + 1) - .5, minor=True)
    ax.set_yticks(np.arange(rows + 1) - .5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=2)
    ax.tick_params(which="minor", bottom=False, left=False)
else:
    ax.grid(False)
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

# Annotate
for i in range(rows):
    for j in range(cols):
        val = npout[i, j]
        text_color = "white" if val > (npout.max() / 2) else "black"
        if label:
          if highlight:
            if val == min_val or val == max_val:
              ax.text(j, i, str(val), ha="center", va="center", color="cyan" if val == min_val else "red", fontsize=9, weight="bold")
            else:
              ax.text(j, i, str(val), ha="center", va="center", color=text_color, fontsize=9, weight="bold")
          else:
            ax.text(j, i, str(val), ha="center", va="center", color=text_color, fontsize=9, weight="bold")

# Title + layout
ax.set_title(f"Heatmap of {tfile} (colormap: {cmap_name})", fontsize=16, pad=20)
fig.tight_layout()

# Save
filename = input("Save file as: ").strip()
if not label:
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
if filename:
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    print(f"Saved to '{filename}'.")

plt.show()
