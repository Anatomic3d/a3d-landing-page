"""
MONAI 3-D Mesh Extraction from CT DICOM
=========================================
Segments a CT series with TotalSegmentator and exports each requested
structure as a smoothed STL + AR-ready GLB (binary glTF).

Usage — full pipeline
---------------------
  python monai_3d.py --dicom ~/Downloads/series5 --bones
  python monai_3d.py --dicom ~/Downloads/series5 --bones --heart --lungs
  python monai_3d.py --dicom ~/Downloads/series5 --all --simplify 0.3 --fast

Usage — convert existing STL(s) to GLB
---------------------------------------
  python monai_3d.py --to-glb bones.stl
  python monai_3d.py --to-glb bones.stl heart.stl lungs.stl
  python monai_3d.py --to-glb output_3d/*.stl --out ./ar_ready

Outputs (per structure)
-----------------------
  output_3d/
    bones.stl            ← mesh (MeshLab, Blender, 3D Slicer …)
    bones.glb            ← AR-ready binary glTF (WebXR, iOS AR Quick Look …)
    heart.stl / heart.glb
    lungs.stl  / lungs.glb
    viewer.html          ← drag-and-drop into browser → AR button on mobile
    preview.png          ← axial / coronal / sagittal overlay
    <structure>_info.txt ← volume, surface area, bounding box

Requirements
------------
  pip install totalsegmentator scikit-image trimesh fast-simplification
              monai pydicom nibabel matplotlib
"""

import argparse
import os
import shutil
import tempfile
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import nibabel as nib
import trimesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from skimage.measure import marching_cubes
from skimage.morphology import binary_closing, ball

# ── Label map ─────────────────────────────────────────────────────────────────

STRUCTURE_LABELS = {
    "bones": [
        25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,
        41,42,43,44,45,46,47,48,49,50,
        69,70,71,72,73,74,75,76,77,78,
        91,
        92,93,94,95,96,97,98,99,100,101,102,103,
        104,105,106,107,108,109,110,111,112,113,114,115,
        116,117,
    ],
    "heart": [51, 52],
    "lungs": [10, 11, 12, 13, 14],
}

# RGBA 0-1 used for GLB vertex colours
STRUCTURE_COLORS = {
    "bones": (0.90, 0.85, 0.64, 1.0),   # ivory
    "heart": (0.85, 0.15, 0.15, 1.0),   # red
    "lungs": (0.60, 0.80, 0.95, 1.0),   # light blue
}

DEFAULT_COLOR = (0.70, 0.70, 0.70, 1.0)  # grey fallback for unknown structures

# ── GLB / glTF export ─────────────────────────────────────────────────────────

# PBR material properties per structure.
# roughnessFactor: 0=mirror, 1=fully matte.  metallicFactor: 0=plastic, 1=metal.
STRUCTURE_PBR = {
    "bones": dict(roughnessFactor=0.65, metallicFactor=0.05),   # dry bone — slight sheen
    "heart": dict(roughnessFactor=0.55, metallicFactor=0.0),    # wet tissue — softer sheen
    "lungs": dict(roughnessFactor=0.80, metallicFactor=0.0),    # spongy — very matte
}
DEFAULT_PBR = dict(roughnessFactor=0.70, metallicFactor=0.0)


def mesh_to_glb(
    mesh: trimesh.Trimesh,
    color_rgba: tuple = DEFAULT_COLOR,
    pbr: dict | None = None,
) -> trimesh.Trimesh:
    """
    Apply a PBR material so the model responds to lighting in model-viewer.
    Flat vertex colors look washed-out; PBR gives shading, highlights, and
    surface detail that make anatomy much easier to read.
    """
    pbr = pbr or DEFAULT_PBR
    material = trimesh.visual.material.PBRMaterial(
        baseColorFactor=list(color_rgba),
        roughnessFactor=pbr["roughnessFactor"],
        metallicFactor=pbr["metallicFactor"],
        doubleSided=True,   # no culling artefacts on thin structures
    )
    mesh = mesh.copy()
    mesh.visual = trimesh.visual.TextureVisuals(material=material)
    return mesh


def save_glb(mesh: trimesh.Trimesh, path: str,
             color_rgba: tuple = DEFAULT_COLOR,
             pbr: dict | None = None) -> None:
    """Apply PBR material + export as binary glTF (.glb)."""
    coloured = mesh_to_glb(mesh, color_rgba, pbr)
    coloured.export(path)
    size_kb = os.path.getsize(path) / 1e3
    print(f"  ✓  GLB saved  → {path}  ({size_kb:.0f} KB)")


def convert_stl_to_glb(
    stl_path: str,
    out_path: str | None = None,
    color_rgba: tuple | None = None,
) -> str:
    """
    Standalone STL → GLB conversion.
    Guesses colour + PBR properties from the filename if not provided.
    Returns the path to the written GLB.
    """
    mesh = trimesh.load(stl_path, force="mesh")
    if not isinstance(mesh, trimesh.Trimesh):
        mesh = trimesh.util.concatenate(list(mesh.geometry.values()))

    name       = os.path.splitext(os.path.basename(stl_path))[0].lower()
    color_rgba = color_rgba or STRUCTURE_COLORS.get(name, DEFAULT_COLOR)
    pbr        = STRUCTURE_PBR.get(name, DEFAULT_PBR)

    if out_path is None:
        out_path = os.path.splitext(stl_path)[0] + ".glb"

    save_glb(mesh, out_path, color_rgba, pbr)
    return out_path


# ── HTML viewer ───────────────────────────────────────────────────────────────

def write_html_viewer(glb_files: list[str], out_path: str) -> None:
    """
    Self-contained HTML page using Google's <model-viewer> web component.
    Works on desktop and mobile; shows an 'AR' button on Android Chrome
    and iOS Safari (iOS 12+, Safari AR Quick Look).

    Contrast improvements vs the previous version:
      - Per-structure background chosen to contrast with the mesh colour
      - environment-image="neutral" gives even, studio-style IBL lighting
      - exposure tuned per structure so no channel clips or washes out
      - shadow-softness reduces harsh hard shadows
      - tone-mapping="agx" improves mid-tone separation
      - PBR materials (set in save_glb) react to the lighting correctly
      - bg toggle button lets the user flip between dark/light backgrounds
    """
    # background that contrasts with each structure colour
    BG = {
        "bones": ("#2c2c2c", "#e8e8e8"),   # dark charcoal / light grey
        "heart": ("#1a1a2e", "#dde8f0"),   # dark navy / pale blue
        "lungs": ("#1a1a1a", "#f0ece4"),   # near-black / warm white
    }
    DEFAULT_BG = ("#222222", "#eeeeee")

    # exposure: bones need a touch more light; lungs are matte so less
    EXPOSURE = {"bones": "0.72", "heart": "0.85", "lungs": "0.80"}

    tabs = ""
    viewers = ""
    bg_data = []   # list of (dark, light) per viewer

    for i, glb in enumerate(glb_files):
        fname   = os.path.splitext(os.path.basename(glb))[0]
        name    = fname.capitalize()
        rel     = os.path.relpath(glb, os.path.dirname(out_path))
        active  = "active" if i == 0 else ""
        hidden  = "" if i == 0 else 'style="display:none"'
        dark_bg, light_bg = BG.get(fname.lower(), DEFAULT_BG)
        exposure = EXPOSURE.get(fname.lower(), "1.0")
        bg_data.append((dark_bg, light_bg))

        tabs += f'<button class="tab {active}" onclick="show({i})">{name}</button>\n'
        viewers += f"""
    <div class="viewer-wrap" id="viewer{i}" {hidden} data-dark="{dark_bg}" data-light="{light_bg}">
      <model-viewer
        src="{rel}"
        ar
        ar-modes="webxr scene-viewer quick-look"
        camera-controls
        auto-rotate
        auto-rotate-delay="500"
        rotation-per-second="20deg"
        environment-image="neutral"
        exposure="{exposure}"
        shadow-intensity="0.6"
        shadow-softness="0.8"
        tone-mapping="agx"
        style="width:100%;height:75vh;background:{dark_bg};--progress-bar-color:#0074D9">
        <button slot="ar-button"
          style="background:#0074D9;color:#fff;border:none;padding:10px 20px;
                 border-radius:6px;font-size:14px;cursor:pointer;margin:8px;
                 box-shadow:0 2px 8px rgba(0,0,0,.4)">
          📱 View in AR
        </button>
      </model-viewer>
    </div>"""

    # serialise bg_data for JS
    bg_json = str(bg_data).replace("'", "\"")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Medical 3D Viewer</title>
  <script type="module"
    src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: #111; color: #eee; font-family: system-ui, sans-serif; }}

    header {{
      display: flex; align-items: center; justify-content: space-between;
      padding: 12px 20px; background: #1a1a1a;
      border-bottom: 1px solid #333;
    }}
    header h1  {{ font-size: 1.1rem; color: #ddd; font-weight: 600; }}
    header p   {{ font-size: 0.75rem; color: #888; margin-top: 3px; }}

    .controls {{
      display: flex; align-items: center; gap: 10px; flex-shrink: 0;
    }}

    /* background toggle */
    .bg-toggle {{
      display: flex; align-items: center; gap: 6px;
      font-size: 12px; color: #aaa; user-select: none; cursor: pointer;
    }}
    .bg-toggle input {{ accent-color: #0074D9; cursor: pointer; }}

    .tabs {{
      display: flex; gap: 6px; padding: 10px 20px;
      background: #1a1a1a; flex-wrap: wrap;
      border-bottom: 1px solid #333;
    }}
    .tab {{
      background: #2a2a2a; color: #bbb; border: 1px solid #444;
      padding: 7px 18px; border-radius: 20px; cursor: pointer;
      font-size: 13px; font-weight: 500; transition: all 0.15s;
    }}
    .tab:hover  {{ background: #3a3a3a; color: #eee; }}
    .tab.active {{ background: #0074D9; color: #fff; border-color: #0074D9; }}

    .viewer-wrap {{ background: #111; }}

    model-viewer {{
      display: block;
      --poster-color: transparent;
    }}

    footer {{
      text-align: center; padding: 10px;
      color: #444; font-size: 11px; background: #1a1a1a;
      border-top: 1px solid #2a2a2a;
    }}
  </style>
</head>
<body>
  <header>
    <div>
      <h1>🫀 Medical 3D Viewer</h1>
      <p>Rotate: drag &nbsp;·&nbsp; Zoom: scroll / pinch &nbsp;·&nbsp; AR: tap button on mobile</p>
    </div>
    <div class="controls">
      <label class="bg-toggle">
        <input type="checkbox" id="bgToggle" onchange="toggleBg(this.checked)">
        Light background
      </label>
    </div>
  </header>

  <div class="tabs">{tabs}</div>

  {viewers}

  <footer>Generated by monai_3d.py &nbsp;·&nbsp; <model-viewer> by Google</footer>

  <script>
    const bgData   = {bg_json};
    let   lightMode = false;
    let   current   = 0;

    function show(i) {{
      current = i;
      document.querySelectorAll('.viewer-wrap').forEach((el, j) => {{
        el.style.display = (i === j) ? '' : 'none';
      }});
      document.querySelectorAll('.tab').forEach((el, j) => {{
        el.classList.toggle('active', i === j);
      }});
      applyBg();
    }}

    function toggleBg(isLight) {{
      lightMode = isLight;
      document.body.style.background    = isLight ? '#f5f5f5' : '#111';
      document.querySelector('header').style.background = isLight ? '#fff'  : '#1a1a1a';
      document.querySelector('.tabs').style.background  = isLight ? '#fff'  : '#1a1a1a';
      applyBg();
    }}

    function applyBg() {{
      document.querySelectorAll('.viewer-wrap').forEach((el, j) => {{
        const [dark, light] = bgData[j];
        const bg = lightMode ? light : dark;
        el.style.background = bg;
        const mv = el.querySelector('model-viewer');
        if (mv) mv.style.background = bg;
      }});
    }}
  </script>
</body>
</html>"""

    with open(out_path, "w") as f:
        f.write(html)
    print(f"  ✓  HTML viewer → {out_path}  (open in browser; AR button on mobile)")


# ── TotalSegmentator ───────────────────────────────────────────────────────────

def run_totalsegmentator(dicom_dir: str, tmp_dir: str, fast: bool = False) -> str:
    from totalsegmentator.python_api import totalsegmentator
    seg_dir = os.path.join(tmp_dir, "segmentations")
    os.makedirs(seg_dir, exist_ok=True)
    print("  Running TotalSegmentator (this may take a few minutes) …")
    totalsegmentator(
        input=dicom_dir, output=seg_dir,
        task="total", fast=fast, verbose=False,
    )
    return seg_dir


# ── Mask assembly ──────────────────────────────────────────────────────────────

def load_structure_mask(seg_dir: str, structure: str) -> tuple[np.ndarray, np.ndarray]:
    from totalsegmentator.map_to_binary import class_map
    all_labels = class_map["total"]
    wanted_ids = set(STRUCTURE_LABELS[structure])
    combined   = None
    spacing    = np.array([1.0, 1.0, 1.0])

    for label_id, label_name in all_labels.items():
        if label_id not in wanted_ids:
            continue
        nii_path = os.path.join(seg_dir, f"{label_name}.nii.gz")
        if not os.path.isfile(nii_path):
            continue
        img     = nib.load(nii_path)
        data    = img.get_fdata(dtype=np.float32) > 0.5
        spacing = np.abs(np.diag(img.affine)[:3])
        combined = data if combined is None else (combined | data)

    if combined is None:
        raise RuntimeError(
            f"No NIfTI files found for '{structure}' in {seg_dir}."
        )
    print(f"  {structure}: shape={combined.shape}, "
          f"voxels={combined.sum():,}, spacing={np.round(spacing,3)} mm")
    return combined.astype(np.uint8), spacing


# ── Mesh extraction ────────────────────────────────────────────────────────────

def mask_to_mesh(
    mask: np.ndarray,
    spacing: np.ndarray,
    simplify_ratio: float = 1.0,
    close_radius: int = 2,
) -> trimesh.Trimesh:
    if close_radius > 0:
        mask = binary_closing(mask, ball(close_radius)).astype(np.uint8)
    verts, faces, normals, _ = marching_cubes(mask, level=0.5, spacing=spacing)
    mesh = trimesh.Trimesh(vertices=verts, faces=faces,
                           vertex_normals=normals, process=True)
    trimesh.smoothing.filter_laplacian(mesh, iterations=3)
    if simplify_ratio < 1.0:
        mesh = mesh.simplify_quadric_decimation(percent=simplify_ratio)
    return mesh


# ── STL / info export ─────────────────────────────────────────────────────────

def save_stl(mesh: trimesh.Trimesh, path: str) -> None:
    mesh.export(path)
    size_mb = os.path.getsize(path) / 1e6
    print(f"  ✓  STL saved  → {path}  ({len(mesh.faces):,} faces, {size_mb:.1f} MB)")


def save_info(mesh: trimesh.Trimesh, structure: str, path: str) -> None:
    bb = mesh.bounding_box.extents
    with open(path, "w") as f:
        f.write(f"Structure    : {structure}\n")
        f.write(f"Vertices     : {len(mesh.vertices):,}\n")
        f.write(f"Faces        : {len(mesh.faces):,}\n")
        f.write(f"Volume       : {mesh.volume:.1f} mm³  ({mesh.volume/1000:.1f} cm³)\n")
        f.write(f"Surface area : {mesh.area:.1f} mm²\n")
        f.write(f"Bounding box : {bb[0]:.1f} × {bb[1]:.1f} × {bb[2]:.1f} mm\n")
        f.write(f"Watertight   : {mesh.is_watertight}\n")
    print(f"  ✓  Info saved → {path}")


# ── Preview image ──────────────────────────────────────────────────────────────

def save_preview(masks: dict[str, np.ndarray], out_path: str) -> None:
    ref = next(iter(masks.values()))
    D, H, W = ref.shape
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.patch.set_facecolor("#1a1a2e")
    planes = [
        ("Axial",    {n: m[D//2, :, :]  for n, m in masks.items()}),
        ("Coronal",  {n: m[:, H//2, :]  for n, m in masks.items()}),
        ("Sagittal", {n: m[:, :, W//2]  for n, m in masks.items()}),
    ]
    struct_cmaps = {
        "bones": matplotlib.colors.ListedColormap(["none", "#E8D5A3"]),
        "heart": matplotlib.colors.ListedColormap(["none", "#FF4444"]),
        "lungs": matplotlib.colors.ListedColormap(["none", "#88CCEE"]),
    }
    for ax, (title, slices) in zip(axes, planes):
        ax.set_title(title, color="white", fontsize=12, pad=6)
        ax.axis("off")
        bg = np.zeros_like(next(iter(slices.values())), dtype=float)
        ax.imshow(bg, cmap=matplotlib.colors.ListedColormap(["#111111"]), vmin=0, vmax=1)
        for name, sl in slices.items():
            ax.imshow(np.ma.masked_where(sl == 0, sl),
                      cmap=struct_cmaps.get(name),
                      vmin=0, vmax=1, alpha=0.85, interpolation="nearest")
    from matplotlib.patches import Patch
    patches = [Patch(color=STRUCTURE_COLORS[n][:3], label=n.capitalize())
               for n in masks]
    axes[1].legend(handles=patches, loc="lower center",
                   bbox_to_anchor=(0.5, -0.08), ncol=len(patches),
                   framealpha=0.6, fontsize=10, facecolor="#222", labelcolor="white")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  ✓  Preview    → {out_path}")



# ── Local HTTP server ─────────────────────────────────────────────────────────

def serve_viewer(out_dir: str, port: int = 8000) -> None:
    """
    Serve out_dir over HTTP and open viewer.html in the default browser.
    Blocks until Ctrl-C.  Needed because browsers block file:// GLB loads
    (CORS policy).
    """
    import http.server
    import socketserver
    import threading
    import webbrowser

    abs_dir = os.path.abspath(out_dir)

    # find a free port if the requested one is busy
    httpd = None
    for p in range(port, port + 20):
        try:
            socketserver.TCPServer.allow_reuse_address = True
            httpd = socketserver.TCPServer(
                ("", p),
                lambda *a, directory=abs_dir, **kw: http.server.SimpleHTTPRequestHandler(
                    *a, directory=directory, **kw
                ),
            )
            port = p
            break
        except OSError:
            continue

    if httpd is None:
        print(f"  Could not find a free port. Run manually:\n"
              f"  cd {abs_dir} && python -m http.server 8000")
        return

    url = f"http://localhost:{port}/viewer.html"
    print(f"\n  Serving at {url}")
    print("  Open that URL on your phone (same Wi-Fi) for the AR button.")
    print("  Press Ctrl-C to stop.\n")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        httpd.shutdown()


def _print_serve_hint(out_dir: str, port: int = 8000) -> None:
    abs_dir = os.path.abspath(out_dir)
    print(f"\n  viewer.html needs HTTP — browsers block file:// GLB requests.")
    print(f"  Start the viewer with:")
    print(f"    python monai_3d.py --serve --out {abs_dir}")
    print(f"  or manually:")
    print(f"    cd {abs_dir} && python -m http.server {port}")


# ── Vercel deployment ─────────────────────────────────────────────────────────

def write_vercel_config(out_dir: str) -> str:
    """
    Write vercel.json into out_dir so that `vercel deploy out_dir` works:
      - treats the folder as a plain static site (no framework auto-detection)
      - serves .glb with the correct MIME type + CORS header
      - rewrites /viewer → /viewer.html (clean URL)
    """
    import json
    config = {
        "version": 2,
        "buildCommand": None,
        "outputDirectory": ".",
        "headers": [
            {
                "source": "/(.*)\.glb",
                "headers": [
                    {"key": "Content-Type",                "value": "model/gltf-binary"},
                    {"key": "Access-Control-Allow-Origin", "value": "*"},
                    {"key": "Cache-Control",               "value": "public, max-age=31536000, immutable"},
                ]
            },
            {
                "source": "/(.*)\.html",
                "headers": [
                    {"key": "Cache-Control", "value": "no-cache"},
                ]
            }
        ],
        "rewrites": [
            {"source": "/viewer", "destination": "/viewer.html"}
        ]
    }
    path = os.path.join(out_dir, "vercel.json")
    with open(path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"  ✓  vercel.json  → {path}")
    return path


def deploy_to_vercel(out_dir: str, prod: bool = False) -> None:
    """
    Run `vercel deploy` on out_dir.
    Requires the Vercel CLI: npm i -g vercel
    """
    import subprocess
    cmd = ["vercel", os.path.abspath(out_dir), "--yes"]
    if prod:
        cmd.append("--prod")
    print(f"\n  Running: {' '.join(cmd)}")
    print("  (You may be prompted to log in on first run)\n")
    try:
        result = subprocess.run(cmd, check=True)
    except FileNotFoundError:
        print("  ✗  Vercel CLI not found. Install it with:")
        print("       npm i -g vercel")
        print("  Then deploy manually:")
        print(f"      vercel {os.path.abspath(out_dir)} --yes")
    except subprocess.CalledProcessError as e:
        print(f"  ✗  vercel exited with code {e.returncode}")



# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="CT DICOM → STL + GLB meshes  |  or  STL → GLB converter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  # full pipeline
  python monai_3d.py --dicom ~/series5 --bones --heart --lungs

  # convert existing STLs to GLB
  python monai_3d.py --to-glb bones.stl
  python monai_3d.py --to-glb bones.stl heart.stl lungs.stl --out ./ar
        """,
    )

    # ── mode A: full pipeline ──────────────────────────────────────────────
    pipe = parser.add_argument_group("full pipeline")
    pipe.add_argument("--dicom",    metavar="DIR",
                      help="DICOM series directory")
    pipe.add_argument("--bones",    action="store_true",
                      help="Extract bone mesh")
    pipe.add_argument("--heart",    action="store_true",
                      help="Extract heart + aorta mesh")
    pipe.add_argument("--lungs",    action="store_true",
                      help="Extract lung lobes mesh")
    pipe.add_argument("--all",      action="store_true",
                      help="Extract all three structures")
    pipe.add_argument("--simplify", type=float, default=0.5, metavar="RATIO",
                      help="Faces to keep 0–1 (default 0.5)")
    pipe.add_argument("--fast",     action="store_true",
                      help="TotalSegmentator fast (lower-res) mode")

    # ── mode B: standalone STL → GLB ──────────────────────────────────────
    conv = parser.add_argument_group("STL → GLB converter")
    conv.add_argument("--to-glb",   nargs="+", metavar="FILE",
                      help="One or more .stl files to convert to .glb")

    # ── shared ────────────────────────────────────────────────────────────
    parser.add_argument("--out",   default="./output_3d",
                        help="Output directory (default: ./output_3d)")
    parser.add_argument("--serve", action="store_true",
                        help="After export, serve viewer.html over HTTP and open browser")
    parser.add_argument("--port",  type=int, default=8000,
                        help="Port for --serve (default 8000)")

    args = parser.parse_args()

    # ── Mode B: pure conversion ───────────────────────────────────────────
    if args.to_glb:
        os.makedirs(args.out, exist_ok=True)
        glb_files = []
        print(f"\nConverting {len(args.to_glb)} STL file(s) → GLB …\n")
        for stl_path in args.to_glb:
            if not os.path.isfile(stl_path):
                print(f"  ⚠  Not found, skipping: {stl_path}")
                continue
            name     = os.path.splitext(os.path.basename(stl_path))[0]
            glb_path = os.path.join(args.out, f"{name}.glb")
            convert_stl_to_glb(stl_path, glb_path)
            glb_files.append(glb_path)

        if glb_files:
            viewer_path = os.path.join(args.out, "viewer.html")
            write_html_viewer(glb_files, viewer_path)

        print(f"\n✅  Done!  {len(glb_files)} GLB(s) written to: {args.out}")
        return

    # ── Mode A: full pipeline ─────────────────────────────────────────────
    if not args.dicom:
        parser.error("Provide --dicom DIR for the full pipeline, "
                     "or --to-glb FILE(S) for conversion.")

    requested = []
    if args.all or args.bones: requested.append("bones")
    if args.all or args.heart: requested.append("heart")
    if args.all or args.lungs: requested.append("lungs")
    if not requested:
        parser.error("Specify at least one of --bones, --heart, --lungs, --all")

    os.makedirs(args.out, exist_ok=True)
    print(f"\nStructures : {', '.join(requested)}")
    print(f"Output     : {args.out}")
    print(f"Simplify   : {args.simplify}\n")

    print("── Step 1/3  TotalSegmentator ──────────────────────────────────────")
    tmp_dir = tempfile.mkdtemp(prefix="monai3d_")
    try:
        seg_dir = run_totalsegmentator(args.dicom, tmp_dir, fast=args.fast)

        print("\n── Step 2/3  Marching Cubes ────────────────────────────────────────")
        meshes = {}
        masks  = {}
        for structure in requested:
            print(f"\n  [{structure}]")
            mask, spacing = load_structure_mask(seg_dir, structure)
            masks[structure] = mask
            meshes[structure] = mask_to_mesh(mask, spacing,
                                             simplify_ratio=args.simplify)

        print("\n── Step 3/3  Exporting ─────────────────────────────────────────────")
        glb_files = []
        for structure, mesh in meshes.items():
            stl_path  = os.path.join(args.out, f"{structure}.stl")
            glb_path  = os.path.join(args.out, f"{structure}.glb")
            info_path = os.path.join(args.out, f"{structure}_info.txt")
            color     = STRUCTURE_COLORS.get(structure, DEFAULT_COLOR)

            save_stl(mesh, stl_path)
            save_glb(mesh, glb_path, color)
            save_info(mesh, structure, info_path)
            glb_files.append(glb_path)

        viewer_path = os.path.join(args.out, "viewer.html")
        write_html_viewer(glb_files, viewer_path)

        if masks:
            save_preview(masks, os.path.join(args.out, "preview.png"))

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    print(f"\n✅  Done!  Files in: {args.out}")
    print("   → Open viewer.html in a browser (AR button appears on mobile)")
    print("   → Upload .glb files to Sketchfab / HoloLens / Quest directly")


if __name__ == "__main__":
    main()
