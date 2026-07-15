"""PowerPoint-compatible jurisdiction-map facade.

This package intentionally shadows the legacy ``scripts/jurisdiction_map.py`` module.
The legacy implementation still owns the map data contract and editable overlays,
while this facade replaces only the base-picture writer.  The picture uses a PNG as
the primary Office blip and stores the SVG in the Office 2016 ``asvg:svgBlip``
extension.  Desktop PowerPoint can therefore use the vector source, while older or
less capable consumers retain a standards-compatible raster fallback.

The committed PNG uses the default light-theme land and border colours.  Runtime
theme recolouring is applied to the SVG source; clients that fall back to PNG will
see the default light map rather than custom map colours.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from typing import Any

from lxml import etree
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml.ns import qn
from pptx.oxml.xmlchemy import OxmlElement
from pptx.parts.image import ImagePart
from pptx.util import Cm

_REPO_ROOT = Path(__file__).resolve().parents[2]
_LEGACY_PATH = Path(__file__).resolve().parents[1] / "jurisdiction_map.py"
DEFAULT_MAP_FALLBACK = _REPO_ROOT / "assets" / "maps" / "world_equal_earth.png"
SVG_NAMESPACE = "http://schemas.microsoft.com/office/drawing/2016/SVG/main"
SVG_EXTENSION_URI = "{96DAC541-7B7A-43D3-8B79-37D633B846F1}"


def _load_legacy_module():
    module_name = "scripts._jurisdiction_map_legacy"
    existing = sys.modules.get(module_name)
    if existing is not None:
        return existing
    spec = importlib.util.spec_from_file_location(module_name, _LEGACY_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load legacy jurisdiction-map module: {_LEGACY_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_legacy = _load_legacy_module()


def _add_powerpoint_svg_picture(
    slide: Any,
    svg_bytes: bytes,
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    fallback_path: str | Path,
    filename: str = "world_equal_earth.svg",
) -> Any:
    """Add PNG primary blip plus Office SVG extension to one picture shape."""
    fallback = Path(fallback_path)
    if not fallback.is_file():
        raise FileNotFoundError(f"PNG map fallback not found: {fallback}")

    picture = slide.shapes.add_picture(
        str(fallback), Cm(x), Cm(y), width=Cm(w), height=Cm(h)
    )
    picture.name = "Jurisdiction map base"

    package = slide.part.package
    svg_partname = package.next_image_partname("svg")
    svg_part = ImagePart(svg_partname, "image/svg+xml", package, svg_bytes, filename)
    svg_rid = slide.part.relate_to(svg_part, RT.IMAGE)

    blip = picture._element.blipFill.blip
    ext_lst = blip.find(qn("a:extLst"))
    if ext_lst is None:
        ext_lst = OxmlElement("a:extLst")
        blip.append(ext_lst)
    ext = OxmlElement("a:ext")
    ext.set("uri", SVG_EXTENSION_URI)
    svg_blip = etree.Element(
        f"{{{SVG_NAMESPACE}}}svgBlip", nsmap={"asvg": SVG_NAMESPACE}
    )
    svg_blip.set(qn("r:embed"), svg_rid)
    ext.append(svg_blip)
    ext_lst.append(ext)
    return picture


def categorical_jurisdiction_map(*args: Any, map_fallback: str | Path | None = None, **kwargs: Any):
    """Render the legacy map with a PowerPoint-compatible dual image base.

    Deck assembly is intentionally single-process and serial, so temporarily swapping
    the legacy private writer is deterministic.  A custom SVG should normally provide
    a matching ``map_fallback`` PNG; otherwise the default Equal Earth fallback is used.
    """
    fallback = Path(map_fallback) if map_fallback else DEFAULT_MAP_FALLBACK
    original_writer = _legacy._add_svg_picture

    def compatible_writer(slide, svg_bytes, x, y, w, h, filename="world_equal_earth.svg"):
        return _add_powerpoint_svg_picture(
            slide, svg_bytes, x, y, w, h,
            fallback_path=fallback,
            filename=filename,
        )

    _legacy._add_svg_picture = compatible_writer
    try:
        manifest = _legacy.categorical_jurisdiction_map(*args, **kwargs)
    finally:
        _legacy._add_svg_picture = original_writer

    manifest["base_image"] = {
        "primary": "png_fallback",
        "vector_extension": "office_svg_blip",
        "svg_extension_uri": SVG_EXTENSION_URI,
        "fallback_asset": fallback.name,
        "fallback_theme": "default_light",
    }
    return manifest


# Public helpers remain source-compatible with the original module.
LabelBox = _legacy.LabelBox
load_map_theme = _legacy.load_map_theme
load_anchor_registry = _legacy.load_anchor_registry
write_exhibit_manifest = _legacy.write_exhibit_manifest


def __getattr__(name: str):
    return getattr(_legacy, name)


__all__ = [
    "DEFAULT_MAP_FALLBACK",
    "SVG_EXTENSION_URI",
    "LabelBox",
    "categorical_jurisdiction_map",
    "load_anchor_registry",
    "load_map_theme",
    "write_exhibit_manifest",
]
