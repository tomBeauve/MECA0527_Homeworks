import numpy as np
import matplotlib.pyplot as plt


#######################################
#           PARAMETERS                #
#######################################

report_params = {
    # Text Sizes (smaller, readable in print)
    'font.size': 18,            # General default
    'axes.labelsize': 18,       # x and y labels
    'axes.titlesize': 18,       # Title
    'xtick.labelsize': 16,      # Tick numbers
    'ytick.labelsize': 16,
    'legend.fontsize': 16,      # Legend text

    # Line & Marker Geometries (moderate for print)
    'lines.linewidth': 2.0,     # Thicker than default for clarity
    'lines.markersize': 4.0,    # Moderate marker size
    'lines.markeredgewidth': 0,  # Remove marker outline for cleaner look

    # Structural Geometries
    'axes.linewidth': 1.5,       # Thicker spines
    'xtick.major.width': 1.5,    # Thicker ticks
    'ytick.major.width': 1.5,
    'xtick.major.size': 6.0,     # Tick length
    'ytick.major.size': 6.0,

    # Fonts
    'font.family': 'DejaVu Serif',
    'font.serif': ['Times New Roman'],  # Standard report font

    # Figure layout
    'figure.autolayout': True,
    'figure.figsize': (8, 6),     # Smaller for print/report
}
slide_params = {
    # Text Sizes (Large for visibility)
    'font.size': 20,           # General default
    'axes.labelsize': 40,      # x and y labels, can be reduced
    'axes.titlesize': 24,      # Title
    'xtick.labelsize': 20,     # Tick numbers
    'ytick.labelsize': 20,
    'legend.fontsize': 18,     # Legend text

    # axes are dark grey => optional
    'axes.edgecolor': "#7D7D7D",    # Dark grey spines
    'xtick.color': '#7D7D7D',       # Dark grey ticks
    'ytick.color': '#7D7D7D',
    'axes.labelcolor': '#7D7D7D',

    # Line & Marker Geometries (Thick for projectors)
    'lines.linewidth': 5,    # Thicker data lines
    'lines.markersize': 2,    # Much larger markers (default was too small)
    'lines.markeredgewidth': 0,  # Remove marker outline for cleaner look

    # Structural Geometries
    'axes.linewidth': 2.0,     # Thicker spines (box)
    'xtick.major.width': 2.0,  # Thicker ticks
    'ytick.major.width': 2.0,
    'xtick.major.size': 8.0,   # Longer ticks
    'ytick.major.size': 8.0,

    # Slide Aesthetics
    'font.family': 'sans-serif',  # Sans-serif is more legible on slides than serif
    'figure.autolayout': True,   # Similar to tight_layout
    'figure.figsize': (12, 9),   # 4:3 Aspect Ratio by default
}
plt.rcParams.update(slide_params)


#######################################
#     UTILITY FUNCTIONS SLIDES        #
#######################################

def finalize_plot(filename: str, show_grid="horizontal", output_dir="", zero_lines=False):
    """
    Finalizes, formats, and exports the active Matplotlib figure.

    Parameters:
        filename (str): Output filename without extension.
        show_grid (bool or str): True (both), False (none), or "horizontal" (y-axis only).
        output_dir (str or Path): Target directory for export.
        zero_lines (bool): If True, draws distinct reference lines at X=0 and Y=0.
    """
    ax = plt.gca()

    # Relives top & right spine
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Horizontal Y-label formatting : set to horizontal
    ax.yaxis.label.set_rotation(0)
    ax.yaxis.label.set_horizontalalignment('right')
    ax.yaxis.label.set_verticalalignment('center')
    ax.yaxis.labelpad = 15

    # Grid control
    if show_grid == "horizontal":
        ax.grid(True, which='major', axis='y',
                linestyle='--', alpha=0.8, zorder=0)
    elif show_grid is True:
        ax.grid(True, which='major', axis='both',
                linestyle='--', alpha=0.8, zorder=0)
    elif show_grid is False:
        ax.grid(False)

    # Adds lines at 0 if asked
    if zero_lines:
        ax.axhline(0, color='#A0A0A0', linewidth=1.5, zorder=1)
        ax.axvline(0, color='#A0A0A0', linewidth=1.5, zorder=1)

    # Ensure elements like grids sit behind data lines
    ax.set_axisbelow(True)

    # Robust path handling

    plt.savefig(output_dir / f"{filename}.svg", bbox_inches='tight', dpi=300)
    plt.savefig(output_dir / f"{filename}.pdf", bbox_inches='tight', dpi=300)
    plt.close()


def annotate_curve(text, xy_data, xy_text_offset=(20, 10), color="#222222"):
    """
    Places a highly visible label directly next to a curve or data point, 
    eliminating the need for a distant legend box.
    """
    ax = plt.gca()
    ax.annotate(
        text,
        xy=xy_data,
        xytext=xy_text_offset,
        textcoords='offset points',
        fontsize=18,
        fontweight='bold',
        color=color,
        arrowprops=dict(arrowstyle="-", color=color, alpha=0.5, linewidth=1.5)
    )


#######################################
#    FIGURE GENERATION WORKFLOW       #
#######################################

x = np.linspace(0, 1, 10)
y = x

fig, ax = plt.subplots()

ax.plot(x, y, label=r"")
# ax.scatter(x_pts, y_pts, label="Data Points", color="#FF5500")

ax.set_xlabel(r"")
ax.set_ylabel(r"")

ax.set_xlim(min, max)
ax.set_ylim(min, max)

ax.set_xticks([])  # manual ticks
ax.set_yticks([])
# automatic tick locator : Restrict to a maximum of 5 bins
ax.locator_params(axis='both', nbins=5)

# Secondary Axis / TwinX
# ax2 = ax.twinx()
# ax2.plot(x, y2, color="red", linestyle=":")
# ax2.set_ylabel("")

# Annotations for curve name (instead of legend) and simple annotations
annotate_curve("text", xy_data=(x[-1], y[-1]), xy_text_offset=(0, 0) color="#0066CC")

# 8. Legend Deployment
ax.legend(loc="best", frameon=True, facecolor="white", edgecolor="none")

# 9. Finalize and Export
finalize_plot(
    filename="name",
    show_grid=True,
    output_dir="name",
    zero_lines=False
)
