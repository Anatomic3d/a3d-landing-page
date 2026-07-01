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

def mesh_to_glb(
    mesh: trimesh.Trimesh,
    color_rgba: tuple = DEFAULT_COLOR,
) -> trimesh.Trimesh:
    """
    Apply a flat vertex colour to every vertex and return a GLB-ready mesh.
    GLB (binary glTF 2.0) is the standard for WebXR, iOS AR Quick Look,
    Android Scene Viewer, HoloLens, Meta Quest, and Sketchfab.
    """
    r, g, b, a = [int(c * 255) for c in color_rgba]
    vertex_colors = np.tile([r, g, b, a], (len(mesh.vertices), 1)).astype(np.uint8)
    mesh.visual = trimesh.visual.ColorVisuals(
        mesh=mesh, vertex_colors=vertex_colors
    )
    return mesh


def save_glb(mesh: trimesh.Trimesh, path: str, color_rgba: tuple = DEFAULT_COLOR) -> None:
    """Colour + export as binary glTF (.glb)."""
    coloured = mesh_to_glb(mesh.copy(), color_rgba)
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
    Guesses the colour from the filename if not provided.
    Returns the path to the written GLB.
    """
    mesh = trimesh.load(stl_path, force="mesh")
    if not isinstance(mesh, trimesh.Trimesh):
        # Some STLs load as a Scene; merge into single mesh
        mesh = trimesh.util.concatenate(
            [g for g in mesh.geometry.values()]
        )

    # auto-detect colour from filename
    if color_rgba is None:
        name = os.path.splitext(os.path.basename(stl_path))[0].lower()
        color_rgba = STRUCTURE_COLORS.get(name, DEFAULT_COLOR)

    if out_path is None:
        out_path = os.path.splitext(stl_path)[0] + ".glb"

    save_glb(mesh, out_path, color_rgba)
    return out_path


# ── HTML viewer ───────────────────────────────────────────────────────────────

def write_html_viewer(glb_files: list[str], out_path: str) -> None:
    """
    Self-contained HTML page using Google's <model-viewer> web component.
    Works on desktop and mobile; shows an 'AR' button on Android Chrome
    and iOS Safari (iOS 12+, Safari AR Quick Look).
    """
    tabs = ""
    viewers = ""
    for i, glb in enumerate(glb_files):
        name    = os.path.splitext(os.path.basename(glb))[0].capitalize()
        rel     = os.path.relpath(glb, os.path.dirname(out_path))
        active  = "active" if i == 0 else ""
        hidden  = "" if i == 0 else 'style="display:none"'
        tabs    += f'<button class="tab {active}" onclick="show({i})">{name}</button>\n'
        viewers += f"""
    <div class="viewer-wrap" id="viewer{i}" {hidden}>
      <model-viewer
        src="{rel}"
        ar
        ar-modes="webxr scene-viewer quick-look"
        camera-controls
        auto-rotate
        shadow-intensity="1"
        style="width:100%;height:75vh;background:#1a1a2e">
        <button slot="ar-button"
          style="background:#0074D9;color:#fff;border:none;padding:10px 20px;
                 border-radius:6px;font-size:14px;cursor:pointer;margin:8px">
          📱 View in AR
        </button>
      </model-viewer>
    </div>"""

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
    body {{ background: #1a1a2e; color: #eee; font-family: sans-serif; }}
    header {{ padding: 16px 24px; background: #16213e;
              border-bottom: 1px solid #0f3460; }}
    header h1 {{ font-size: 1.2rem; color: #88ccee; }}
    header p  {{ font-size: 0.8rem; color: #888; margin-top: 4px; }}
    .tabs {{ display: flex; gap: 8px; padding: 12px 24px;
             background: #16213e; flex-wrap: wrap; }}
    .tab {{ background: #0f3460; color: #ccc; border: none;
            padding: 8px 20px; border-radius: 6px; cursor: pointer;
            font-size: 14px; transition: background 0.2s; }}
    .tab:hover  {{ background: #1a4a80; }}
    .tab.active {{ background: #0074D9; color: #fff; }}
    .viewer-wrap {{ padding: 0 24px 24px; }}
    footer {{ text-align: center; padding: 12px; color: #555; font-size: 12px; }}
  </style>
</head>
<body>
  <header>
    <h1>🫀 Medical 3D Viewer</h1>
    <p>Rotate: drag &nbsp;|&nbsp; Zoom: scroll / pinch &nbsp;|&nbsp;
       AR: tap "View in AR" on mobile</p>
  </header>
  <div class="tabs">
    {tabs}
  </div>
  {viewers}
  <footer>Generated by monai_3d.py &nbsp;·&nbsp;
    <model-viewer> powered by Google</footer>
  <script>
    function show(i) {{
      document.querySelectorAll('.viewer-wrap').forEach((el, j) => {{
        el.style.display = (i === j) ? '' : 'none';
      }});
      document.querySelectorAll('.tab').forEach((el, j) => {{
        el.classList.toggle('active', i === j);
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
    parser.add_argument("--out", default="./output_3d",
                        help="Output directory (default: ./output_3d)")

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
