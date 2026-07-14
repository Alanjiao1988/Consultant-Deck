"""Render-level smoke QA for the jurisdiction-map demo.

This is intentionally a structural visual gate rather than a pixel-perfect golden
image comparison. It catches blank SVGs, missing map/rail regions, gross clipping
and all-white output while tolerating minor font and renderer differences across
PowerPoint and LibreOffice versions.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from PIL import Image


@dataclass
class Finding:
    severity: str
    check: str
    message: str


def _ratio(image: Image.Image, predicate) -> float:
    pixels = list(image.getdata())
    return sum(1 for pixel in pixels if predicate(pixel)) / max(len(pixels), 1)


def _crop_fraction(image: Image.Image, left: float, top: float, right: float, bottom: float) -> Image.Image:
    width, height = image.size
    return image.crop((int(width * left), int(height * top), int(width * right), int(height * bottom)))


def inspect_rendered_png(path: Path) -> list[Finding]:
    image = Image.open(path).convert("RGB")
    findings: list[Finding] = []
    if image.width < 1200 or image.height < 650:
        findings.append(Finding("error", "render_resolution", f"Rendered image is too small: {image.size}"))

    regions = {
        "all": (image, 0.15, 0.55),
        "title": (_crop_fraction(image, 0.0, 0.0, 1.0, 0.18), 0.025, 0.25),
        "map": (_crop_fraction(image, 0.08, 0.22, 0.68, 0.82), 0.12, 0.45),
        "rail": (_crop_fraction(image, 0.70, 0.15, 0.98, 0.92), 0.65, 0.99),
    }
    for name, (region, minimum, maximum) in regions.items():
        non_white = _ratio(region, lambda pixel: min(pixel) < 245)
        if not minimum <= non_white <= maximum:
            findings.append(Finding(
                "error",
                "render_structure",
                f"{name} non-white ratio {non_white:.3f} is outside {minimum:.3f}-{maximum:.3f}",
            ))

    dark_ratio = _ratio(image, lambda pixel: max(pixel) < 120)
    if not 0.005 <= dark_ratio <= 0.08:
        findings.append(Finding(
            "error", "render_contrast", f"Dark-pixel ratio {dark_ratio:.3f} suggests missing text or excessive fill"
        ))

    quantized = image.quantize(colors=32)
    used_colours = len(quantized.getcolors(maxcolors=32) or [])
    if used_colours < 12:
        findings.append(Finding("error", "render_palette", f"Only {used_colours} quantized colours detected"))
    return findings


def render_pptx(pptx_path: Path, output_dir: Path) -> Path:
    soffice = shutil.which("libreoffice") or shutil.which("soffice")
    pdftoppm = shutil.which("pdftoppm")
    if not soffice or not pdftoppm:
        missing = [name for name, value in (("libreoffice", soffice), ("pdftoppm", pdftoppm)) if not value]
        raise RuntimeError("Missing render tools: " + ", ".join(missing))
    subprocess.run(
        [soffice, "--headless", "--convert-to", "pdf", "--outdir", str(output_dir), str(pptx_path)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    pdf_path = output_dir / f"{pptx_path.stem}.pdf"
    png_base = output_dir / pptx_path.stem
    subprocess.run(
        [pdftoppm, "-png", "-f", "1", "-singlefile", "-r", "120", str(pdf_path), str(png_base)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return png_base.with_suffix(".png")


def run_qa(pptx_path: Path, rendered_png: Path | None = None) -> tuple[list[Finding], Path]:
    if rendered_png is not None:
        return inspect_rendered_png(rendered_png), rendered_png
    with tempfile.TemporaryDirectory(prefix="jurisdiction-map-render-") as tmp:
        png_path = render_pptx(pptx_path, Path(tmp))
        findings = inspect_rendered_png(png_path)
        retained = pptx_path.with_suffix(".rendered.png")
        shutil.copy2(png_path, retained)
        return findings, retained


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run render-level jurisdiction-map smoke QA")
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--rendered-png", type=Path, default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    findings, rendered = run_qa(args.pptx, args.rendered_png)
    if args.json:
        print(json.dumps({"rendered": str(rendered), "findings": [asdict(item) for item in findings]}, indent=2))
    else:
        print(f"Rendered: {rendered}")
        for item in findings:
            print(f"[{item.severity}] {item.check}: {item.message}")
    return 1 if any(item.severity == "error" for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
