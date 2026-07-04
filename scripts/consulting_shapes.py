"""PowerPoint-native consulting shapes for python-pptx."""
from pptx.util import Cm, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn

PRIMARY = "1F3864"
ACCENT = "C00000"
GRAY_TEXT = "333333"
GRAY_2 = "595959"
GRAY_3 = "A6A6A6"
GRAY_LINE = "D9D9D9"
GRAY_FILL = "F2F2F2"
FONT_LATIN = "Arial"
FONT_EA = "Microsoft YaHei"


def set_font(run, size_pt=11, bold=False, color=GRAY_TEXT, italic=False):
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor.from_string(color)
    run.font.name = FONT_LATIN
    rPr = run._r.get_or_add_rPr()
    ea = rPr.find(qn("a:ea"))
    if ea is None:
        ea = rPr.makeelement(qn("a:ea"), {})
        rPr.append(ea)
    ea.set("typeface", FONT_EA)


def add_textbox(slide, text, x, y, w, h, size=11, bold=False, color=GRAY_TEXT,
                align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, italic=False):
    tb = slide.shapes.add_textbox(Cm(x), Cm(y), Cm(w), Cm(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    set_font(run, size, bold, color, italic)
    return tb


def _solid(shape, hex_color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor.from_string(hex_color)


def _line(shape, hex_color=None, width_pt=0.75):
    if hex_color is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = RGBColor.from_string(hex_color)
        shape.line.width = Pt(width_pt)


def harvey_ball(slide, x, y, fill_pct, diameter=0.55):
    d = Cm(diameter)
    ring = slide.shapes.add_shape(MSO_SHAPE.OVAL, Cm(x), Cm(y), d, d)
    _solid(ring, "FFFFFF")
    _line(ring, PRIMARY, 1.0)
    if fill_pct >= 100:
        _solid(ring, PRIMARY)
    return ring


def matrix_2x2(slide, x, y, size_cm, x_label, y_label, points=None, quadrant_labels=None):
    half = size_cm / 2
    for qx, qy, fill in [(0, half, "FFFFFF"), (half, half, "FFFFFF"), (0, 0, "FFFFFF"), (half, 0, GRAY_FILL)]:
        r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Cm(x + qx), Cm(y + qy), Cm(half), Cm(half))
        _solid(r, fill)
        _line(r, GRAY_LINE)
    add_textbox(slide, x_label, x, y + size_cm + 0.15, size_cm, 0.5, 10, True, GRAY_2, PP_ALIGN.CENTER)
    add_textbox(slide, y_label, x - 0.6, y - 0.7, size_cm, 0.5, 10, True, GRAY_2)
    if quadrant_labels:
        for label, (qx, qy) in zip(quadrant_labels, [(0, half), (half, half), (0, 0), (half, 0)]):
            add_textbox(slide, label, x + qx + 0.15, y + qy + 0.1, half - 0.3, 0.5, 9, False, GRAY_3, italic=True)
    if points:
        for name, px, py in points:
            d = 0.45
            cx = x + px * size_cm - d / 2
            cy = y + (1 - py) * size_cm - d / 2
            dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Cm(cx), Cm(cy), Cm(d), Cm(d))
            _solid(dot, PRIMARY)
            _line(dot, None)
            add_textbox(slide, name, cx + d + 0.08, cy - 0.05, 3.5, 0.5, 9)


def matrix_2x2_with_insights(slide, x, y, size_cm, x_label, y_label, points=None,
                             quadrant_labels=None, quadrant_implications=None, insight_title="Implications"):
    matrix_2x2(slide, x, y, size_cm, x_label, y_label, points, quadrant_labels)
    if quadrant_implications:
        ix = x + size_cm + 0.8
        add_textbox(slide, insight_title, ix, y, 10, 0.6, 11, True, PRIMARY)
        cy = y + 0.8
        for label, implication in quadrant_implications:
            add_textbox(slide, label, ix, cy, 2.8, 0.45, 9, True, PRIMARY)
            add_textbox(slide, implication, ix + 3.0, cy, 10.5, 0.8, 9.5)
            cy += 1.0


def waterfall(slide, items, x, y, w, h, unit=""):
    starts = [v for _, v, k in items if k == "start"]
    ends = [v for _, v, k in items if k == "end"]
    deltas = [v for _, v, k in items if k == "delta"]
    if starts and ends and abs(starts[0] + sum(deltas) - ends[0]) > 1e-6:
        raise ValueError("waterfall does not reconcile")
    vals = []
    run = 0
    for _, v, k in items:
        if k in ("start", "end"):
            run = v
            vals.append(v)
        else:
            vals += [run, run + v]
            run += v
    vmin, vmax = min(vals + [0]), max(vals + [0])
    span = vmax - vmin or 1
    bar_w = w / (len(items) * 1.5)
    gap = bar_w * 0.5
    zero_y = y + h - 0.5 - (0 - vmin) * ((h - 1.2) / span)
    scale = (h - 1.2) / span
    run = 0
    for i, (label, value, kind) in enumerate(items):
        bx = x + i * (bar_w + gap)
        if kind in ("start", "end"):
            top = zero_y - value * scale
            height = abs(value) * scale
            run = value
            fill = GRAY_2
        else:
            y0 = zero_y - run * scale
            run += value
            y1 = zero_y - run * scale
            top = min(y0, y1)
            height = abs(value) * scale
            fill = PRIMARY if value >= 0 else ACCENT
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Cm(bx), Cm(top), Cm(bar_w), Cm(height))
        _solid(bar, fill)
        _line(bar, None)
        add_textbox(slide, f"{value:+g}{unit}" if kind == "delta" else f"{value:g}{unit}", bx - 0.2, top - 0.55, bar_w + 0.4, 0.5, 9, True, align=PP_ALIGN.CENTER)
        add_textbox(slide, label, bx - 0.3, y + h - 0.4, bar_w + 0.6, 0.8, 8.5, align=PP_ALIGN.CENTER)


def native_chart(slide, chart_type, categories, series, x, y, w, h, show_legend=None, show_values=True,
                 show_axis=True, show_gridlines=False, value_format=None, highlight_series=0):
    from pptx.chart.data import CategoryChartData
    from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
    mapping = {"bar": XL_CHART_TYPE.COLUMN_CLUSTERED, "column": XL_CHART_TYPE.COLUMN_CLUSTERED,
               "stacked_bar": XL_CHART_TYPE.COLUMN_STACKED, "line": XL_CHART_TYPE.LINE}
    if chart_type not in mapping:
        raise ValueError(f"unsupported chart_type: {chart_type}")
    if not categories or not series:
        raise ValueError("categories and series are required")
    for name, values in series:
        if len(values) != len(categories):
            raise ValueError(f"series length mismatch: {name}")
    data = CategoryChartData()
    data.categories = categories
    for name, values in series:
        data.add_series(name, values)
    frame = slide.shapes.add_chart(mapping[chart_type], Cm(x), Cm(y), Cm(w), Cm(h), data)
    chart = frame.chart
    palette = [PRIMARY, "6C86B3", GRAY_3, "A9B9D6"]
    for i, s in enumerate(chart.series):
        color = PRIMARY if i == highlight_series else palette[i % len(palette)]
        if chart_type == "line":
            s.format.line.color.rgb = RGBColor.from_string(color)
            s.format.line.width = Pt(2)
        else:
            s.format.fill.solid()
            s.format.fill.fore_color.rgb = RGBColor.from_string(color)
            s.format.line.fill.background()
            if show_values:
                s.data_labels.show_value = True
                s.data_labels.font.size = Pt(9)
                s.data_labels.font.name = FONT_LATIN
                if value_format:
                    s.data_labels.number_format = value_format
    chart.has_legend = (len(series) > 1) if show_legend is None else bool(show_legend)
    if chart.has_legend:
        chart.legend.position = XL_LEGEND_POSITION.BOTTOM
        chart.legend.include_in_layout = False
        chart.legend.font.size = Pt(9)
    try:
        chart.category_axis.visible = bool(show_axis)
        chart.value_axis.visible = bool(show_axis)
        chart.value_axis.has_major_gridlines = bool(show_gridlines)
        if value_format:
            chart.value_axis.tick_labels.number_format = value_format
    except Exception:
        pass
    return frame


def option_evaluation_table(slide, options, criteria, scores, x, y, w, h):
    nr, nc = len(options), len(criteria)
    label_w = w * 0.28
    col_w = (w - label_w) / nc
    row_h = (h - 0.8) / nr
    add_textbox(slide, "Option", x, y, label_w, 0.7, 9.5, True, GRAY_2)
    for j, c in enumerate(criteria):
        add_textbox(slide, c, x + label_w + j * col_w, y, col_w, 0.7, 9, True, GRAY_2, PP_ALIGN.CENTER)
    max_by_col = [max(row[j] for row in scores) for j in range(nc)]
    for i, opt in enumerate(options):
        ry = y + 0.8 + i * row_h
        add_textbox(slide, opt, x, ry + 0.05, label_w - 0.1, row_h, 9.3, True)
        for j, value in enumerate(scores[i]):
            cell = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Cm(x + label_w + j * col_w), Cm(ry), Cm(col_w - 0.05), Cm(row_h - 0.05))
            best = value == max_by_col[j]
            _solid(cell, "D6DEEC" if best else "FFFFFF")
            _line(cell, GRAY_LINE, 0.5)
            tf = cell.text_frame
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            r = p.add_run(); r.text = str(value)
            set_font(r, 9.5, best, PRIMARY if best else GRAY_TEXT)


def risk_matrix(slide, risks, x, y, w, h):
    cell_w, cell_h = w / 5, h / 5
    for i in range(5):
        for j in range(5):
            sev = i + j
            fill = "FFFFFF" if sev < 4 else (GRAY_FILL if sev < 6 else "D6DEEC")
            cell = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Cm(x + i * cell_w), Cm(y + (4 - j) * cell_h), Cm(cell_w), Cm(cell_h))
            _solid(cell, fill); _line(cell, GRAY_LINE, 0.5)
    add_textbox(slide, "Likelihood", x, y + h + 0.15, w, 0.45, 9.5, True, GRAY_2, PP_ALIGN.CENTER)
    add_textbox(slide, "Impact", x - 0.7, y - 0.45, h, 0.45, 9.5, True, GRAY_2)
    for name, likelihood, impact, _ in risks:
        d = 0.55
        px = x + (max(1, min(5, likelihood)) - 0.5) * cell_w - d / 2
        py = y + (5 - max(1, min(5, impact)) + 0.5) * cell_h - d / 2
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Cm(px), Cm(py), Cm(d), Cm(d))
        _solid(dot, ACCENT if likelihood + impact >= 8 else PRIMARY)
        _line(dot, None)
        add_textbox(slide, name, px + d + 0.08, py - 0.02, 3.2, 0.45, 8.5)


def raci_matrix(slide, activities, roles, assignments, x, y, w, h):
    label_w = w * 0.34
    col_w = (w - label_w) / len(roles)
    row_h = (h - 0.8) / len(activities)
    add_textbox(slide, "Activity", x, y, label_w, 0.7, 9.5, True, GRAY_2)
    for j, role in enumerate(roles):
        add_textbox(slide, role, x + label_w + j * col_w, y, col_w, 0.7, 8.5, True, GRAY_2, PP_ALIGN.CENTER)
    for i, act in enumerate(activities):
        ry = y + 0.8 + i * row_h
        add_textbox(slide, act, x, ry + 0.05, label_w - 0.1, row_h, 9)
        for j, role in enumerate(roles):
            val = assignments.get((act, role), "")
            cell = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Cm(x + label_w + j * col_w), Cm(ry), Cm(col_w - 0.05), Cm(row_h - 0.05))
            _solid(cell, "FFFFFF"); _line(cell, GRAY_LINE, 0.5)
            if val:
                p = cell.text_frame.paragraphs[0]
                p.alignment = PP_ALIGN.CENTER
                r = p.add_run(); r.text = val
                set_font(r, 10, True, PRIMARY if val in ("A", "R") else GRAY_2)
