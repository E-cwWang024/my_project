import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

# ================== Basic Settings ==================
x = np.linspace(-2.5 * np.pi, 2.5 * np.pi, 1000)
y_true = np.sin(x)

def taylor_sin(x, n_terms):
    result = np.zeros_like(x)
    for k in range(n_terms):
        result += ((-1) ** k) * x ** (2 * k + 1) / math.factorial(2 * k + 1)
    return result

N_TERMS_MAX = 8
FPS = 30
HOLD_FRAMES = 25   
TRANS_FRAMES = 30  
frames_per_step = HOLD_FRAMES + TRANS_FRAMES
total_frames = N_TERMS_MAX * frames_per_step

def smoothstep(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3 - 2 * t)

def get_blended_curve(frame):
    step = frame // frames_per_step
    local = frame % frames_per_step
    idx_a = min(step, N_TERMS_MAX - 1)
    idx_b = min(step + 1, N_TERMS_MAX - 1)

    if local < HOLD_FRAMES:
        return taylor_sin(x, idx_a + 1), idx_a
    t = (local - HOLD_FRAMES) / TRANS_FRAMES
    w = smoothstep(t)
    y_a = taylor_sin(x, idx_a + 1)
    y_b = taylor_sin(x, idx_b + 1)
    return (1 - w) * y_a + w * y_b, (idx_b if w > 0.5 else idx_a)

# ================== Creating Canvas ==================
fig, ax = plt.subplots(figsize=(10, 6))
fig.subplots_adjust(top=0.85, bottom=0.12)

ax.plot(x, y_true, 'k--', linewidth=2, label='sin(x) (exact)')
line_approx, = ax.plot([], [], 'r-', linewidth=2.5, label='Taylor polynomial')

# text box
formula_text = ax.text(
    0.02, 0.97, '', transform=ax.transAxes,
    fontsize=14, verticalalignment='top',
    bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.95, edgecolor='orange')
)

ax.set_xlim(-2.5 * np.pi, 2.5 * np.pi)
ax.set_ylim(-3, 3)
# 坐标轴使用 Unicode 的 π
ax.set_xticks([-2*np.pi, -np.pi, 0, np.pi, 2*np.pi])
ax.set_xticklabels(['-2π', '-π', '0', 'π', '2π'], fontsize=12)
ax.set_xlabel('x', fontsize=14)
ax.set_ylabel('y', fontsize=14)
ax.set_title('Taylor expansion of sin(x)', fontsize=16, pad=15)
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='upper right', fontsize=12)
ax.axhline(0, color='gray', linewidth=0.8)
ax.axvline(0, color='gray', linewidth=0.8)

# Unicode Dictionary
SUP = {1:'¹',2:'²',3:'³',4:'⁴',5:'⁵',6:'⁶',7:'⁷',8:'⁸',
       9:'⁹',10:'¹⁰',11:'¹¹',12:'¹²',13:'¹³',14:'¹⁴',15:'¹⁵'}

def build_formula(term_idx):
    n_terms = term_idx + 1
    degree = 2 * n_terms - 1
    
    if n_terms == 1:
        return f'P_{degree}(x) = x', degree
        
    parts = ['x']
    for k in range(1, n_terms):
        sign = '-' if k % 2 == 1 else '+'
        p = 2*k+1
        parts.append(f'{sign} x{SUP[p]}/{p}!')
    return f'P_{degree}(x) = ' + ' '.join(parts), degree

# ================== Animation Updating ==================
def update(frame):
    y_curve, formula_idx = get_blended_curve(frame)
    line_approx.set_data(x, y_curve)
    
    formula, degree = build_formula(formula_idx)
    formula_text.set_text(formula + f'\ndegree n = {degree}')
    ax.set_title(f'Taylor expansion of sin(x)  —  current degree n = {degree}',
                 fontsize=16, pad=15)
    return line_approx, formula_text

ani = animation.FuncAnimation(
    fig, update, frames=total_frames, interval=1000/FPS,
    blit=False, repeat=True
)

plt.show()