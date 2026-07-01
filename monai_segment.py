"""
MONAI 3-D Mesh Extraction from CT DICOM
=========================================
Segments a CT series with TotalSegmentator and exports
each requested structure as a smoothed .stl mesh.

Usage examples
--------------
  # bones only
  python monai_3d.py --dicom ~/Downloads/series5 --bones

  # all three at once
  python monai_3d.py --dicom ~/Downloads/series5 --bones --heart --lungs

  # custom output folder + mesh simplification (0–1, smaller = lighter file)
  python monai_3d.py --dicom ~/Downloads/series5 --bones --lungs --out ./meshes --simplify 0.3

Outputs (per structure)
-----------------------
  output/
    bones.stl
    heart.stl
    lungs.stl
    preview.png          ← axial / coronal / sagittal overlay
    <structure>_info.txt ← volume, surface area, bounding box

Requirements
------------
  pip install totalsegmentator scikit-image trimesh monai pydicom nibabel matplotlib
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
# Subset of TotalSegmentator "total" task labels grouped by structure.
# Each value is a list of integer label IDs from the multi-label NIfTI.

STRUCTURE_LABELS = {
    "bones": [
        25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,  # vertebrae L-T
        41,42,43,44,45,46,47,48,49,50,                     # vertebrae C
        69,70,71,72,73,74,75,76,77,78,                     # limb girdle
        91,                                                 # skull
        92,93,94,95,96,97,98,99,100,101,102,103,           # ribs left
        104,105,106,107,108,109,110,111,112,113,114,115,   # ribs right
        116,117,                                            # sternum + costal cartilages
    ],
    "heart": [51, 52],          # heart + aorta
    "lungs": [10, 11, 12, 13, 14],
}

STRUCTURE_COLORS = {
    "bones": (0.9, 0.85, 0.75, 1.0),   # ivory
    "heart": (0.85, 0.15, 0.15, 1.0),  # red
    "lungs": (0.6,  0.8,  0.95, 1.0),  # light blue
}

# ── TotalSegmentator ───────────────────────────────────────────────────────────

def run_totalsegmentator(dicom_dir: str, tmp_dir: str, fast: bool = False) -> str:
    """
    Run TotalSegmentator on the DICOM series and return the path to the
    output directory containing per-structure NIfTI files.
    """
    from totalsegmentator.python_api import totalsegmentator

    seg_dir = os.path.join(tmp_dir, "segmentations")
    os.makedirs(seg_dir, exist_ok=True)

    print("  Running TotalSegmentator (this may take a few minutes) …")
    totalsegmentator(
        input      = dicom_dir,
        output     = seg_dir,
        task       = "total",
        fast       = fast,         # --fast for lower-res, quicker inference
        verbose    = False,
    )
    return seg_dir


# ── Mask assembly ──────────────────────────────────────────────────────────────

def load_structure_mask(seg_dir: str, structure: str) -> tuple[np.ndarray, np.ndarray]:
    """
    Merge all per-label NIfTI files for a structure into one binary mask.
    Returns (binary_mask, voxel_spacing_mm).
    """
    from totalsegmentator.map_to_binary import class_map
    all_labels = class_map["total"]                        # {id: name}
    wanted_ids = set(STRUCTURE_LABELS[structure])

    combined = None
    spacing   = np.array([1.0, 1.0, 1.0])

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
            f"No NIfTI files found for '{structure}' in {seg_dir}. "
            "Make sure TotalSegmentator ran successfully."
        )

    print(f"  {structure}: mask shape={combined.shape}, "
          f"voxels={combined.sum():,}, spacing={spacing} mm")
    return combined.astype(np.uint8), spacing


# ── Mesh extraction ────────────────────────────────────────────────────────────

def mask_to_mesh(
    mask: np.ndarray,
    spacing: np.ndarray,
    simplify_ratio: float = 1.0,
    close_radius: int = 2,
) -> trimesh.Trimesh:
    """
    Binary mask  →  smoothed, optionally simplified trimesh.Trimesh.

    Steps:
      1. Morphological closing (fills small holes)
      2. Marching cubes (iso-surface extraction)
      3. Scale vertices by voxel spacing → real-world mm coords
      4. Laplacian smoothing
      5. Optional mesh simplification
    """
    # 1. Close small holes
    if close_radius > 0:
        mask = binary_closing(mask, ball(close_radius)).astype(np.uint8)

    # 2. Marching cubes
    verts, faces, normals, _ = marching_cubes(mask, level=0.5, spacing=spacing)

    # 3. Build trimesh
    mesh = trimesh.Trimesh(vertices=verts, faces=faces,
                           vertex_normals=normals, process=True)

    # 4. Laplacian smooth (3 iterations keeps anatomy, removes staircase artefacts)
    trimesh.smoothing.filter_laplacian(mesh, iterations=3)

    # 5. Simplify
    # simplify_ratio = fraction of faces to KEEP (e.g. 0.5 = keep half).
    # trimesh expects target_reduction = fraction to REMOVE.
    if simplify_ratio < 1.0:
        mesh = mesh.simplify_quadric_decimation(percent=simplify_ratio)

    return mesh


# ── Export helpers ─────────────────────────────────────────────────────────────

def save_stl(mesh: trimesh.Trimesh, path: str) -> None:
    mesh.export(path)
    size_mb = os.path.getsize(path) / 1e6
    print(f"  ✓  STL saved → {path}  ({len(mesh.faces):,} faces, {size_mb:.1f} MB)")


def save_info(mesh: trimesh.Trimesh, structure: str, path: str) -> None:
    bb   = mesh.bounding_box.extents
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
    """
    Three-plane (axial / coronal / sagittal) overlay of all structure masks.
    """
    # pick the first mask to determine volume shape
    ref = next(iter(masks.values()))
    D, H, W = ref.shape

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.patch.set_facecolor("#1a1a2e")
    planes = [
        ("Axial",    ref[D//2, :, :],  {n: m[D//2, :, :]  for n,m in masks.items()}),
        ("Coronal",  ref[:, H//2, :],  {n: m[:, H//2, :]  for n,m in masks.items()}),
        ("Sagittal", ref[:, :, W//2],  {n: m[:, :, W//2]  for n,m in masks.items()}),
    ]

    cmap_bg = matplotlib.colors.ListedColormap(["#111111"])
    struct_cmaps = {
        "bones": matplotlib.colors.ListedColormap(["none", "#E8D5A3"]),
        "heart": matplotlib.colors.ListedColormap(["none", "#FF4444"]),
        "lungs": matplotlib.colors.ListedColormap(["none", "#88CCEE"]),
    }

    for ax, (title, _, slices) in zip(axes, planes):
        ax.set_title(title, color="white", fontsize=12, pad=6)
        ax.axis("off")
        # draw a dark background
        combined_bg = np.zeros_like(next(iter(slices.values())), dtype=float)
        ax.imshow(combined_bg, cmap=cmap_bg, vmin=0, vmax=1)
        for name, sl in slices.items():
            color = STRUCTURE_COLORS[name]
            cmap  = struct_cmaps.get(name)
            ax.imshow(np.ma.masked_where(sl == 0, sl),
                      cmap=cmap, vmin=0, vmax=1, alpha=0.85, interpolation="nearest")

    # legend
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
    print(f"  ✓  Preview saved → {out_path}")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="CT DICOM → 3-D STL meshes via TotalSegmentator + Marching Cubes"
    )
    parser.add_argument("--dicom",    required=True,
                        help="DICOM series directory")
    parser.add_argument("--bones",    action="store_true",
                        help="Extract bone mesh (vertebrae, ribs, skull, …)")
    parser.add_argument("--heart",    action="store_true",
                        help="Extract heart + aorta mesh")
    parser.add_argument("--lungs",    action="store_true",
                        help="Extract lung lobes mesh")
    parser.add_argument("--all",      action="store_true",
                        help="Extract all three structures")
    parser.add_argument("--simplify", type=float, default=0.5, metavar="RATIO",
                        help="Mesh simplification ratio 0–1 (default 0.5). "
                             "Lower = fewer faces = smaller file.")
    parser.add_argument("--fast",     action="store_true",
                        help="Use TotalSegmentator fast (lower-res) mode")
    parser.add_argument("--out",      default="./output_3d",
                        help="Output directory (default: ./output_3d)")
    args = parser.parse_args()

    # resolve requested structures
    requested = []
    if args.all or args.bones: requested.append("bones")
    if args.all or args.heart: requested.append("heart")
    if args.all or args.lungs: requested.append("lungs")

    if not requested:
        parser.error("Specify at least one of --bones, --heart, --lungs, --all")

    os.makedirs(args.out, exist_ok=True)
    print(f"\nStructures requested : {', '.join(requested)}")
    print(f"Output directory     : {args.out}")
    print(f"Mesh simplification  : {args.simplify}\n")

    # ── 1. Segmentation ──────────────────────────────────────────────────────
    print("── Step 1/3  TotalSegmentator ──────────────────────────────────────")
    tmp_dir = tempfile.mkdtemp(prefix="monai3d_")
    try:
        seg_dir = run_totalsegmentator(args.dicom, tmp_dir, fast=args.fast)

        # ── 2. Mask assembly + mesh extraction ──────────────────────────────
        print("\n── Step 2/3  Marching Cubes ────────────────────────────────────────")
        meshes = {}
        masks  = {}
        for structure in requested:
            print(f"\n  [{structure}]")
            mask, spacing = load_structure_mask(seg_dir, structure)
            masks[structure] = mask
            mesh = mask_to_mesh(mask, spacing, simplify_ratio=args.simplify)
            meshes[structure] = mesh

        # ── 3. Export ────────────────────────────────────────────────────────
        print("\n── Step 3/3  Exporting ─────────────────────────────────────────────")
        for structure, mesh in meshes.items():
            stl_path  = os.path.join(args.out, f"{structure}.stl")
            info_path = os.path.join(args.out, f"{structure}_info.txt")
            save_stl(mesh, stl_path)
            save_info(mesh, structure, info_path)

        if masks:
            save_preview(masks, os.path.join(args.out, "preview.png"))

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    print(f"\n✅  Done!  Files written to: {args.out}")
    print("   Open the .stl files in MeshLab, Blender, or any 3-D viewer.")


if __name__ == "__main__":
    main()
