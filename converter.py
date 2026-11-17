"""
Universal Document & Media Converter for Koç University ELC INT 07 AI Hub.
Supports robust conversions across PDF, Word (.docx), Excel (.xlsx, .csv),
PowerPoint (.pptx), Images (.jpg, .png, .webp), and Text (.txt, .md).
"""
import io
import os
import csv
from typing import Tuple

# Image conversion
from PIL import Image

# Docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor

# PDF Reader
from pypdf import PdfReader

# Excel
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

# PPTX
from pptx import Presentation

# ReportLab for PDF generation
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

SUPPORTED_CONVERSIONS = {
    "docx": ["pdf", "txt", "html"],
    "pdf": ["docx", "txt", "html"],
    "xlsx": ["csv", "pdf", "html", "txt"],
    "xls": ["csv", "xlsx", "txt"],
    "csv": ["xlsx", "pdf", "html", "txt"],
    "pptx": ["pdf", "docx", "txt", "html"],
    "png": ["jpg", "webp", "pdf"],
    "jpg": ["png", "webp", "pdf"],
    "jpeg": ["png", "webp", "pdf"],
    "webp": ["png", "jpg", "pdf"],
    "bmp": ["png", "jpg", "pdf"],
    "txt": ["pdf", "docx", "html"],
    "md": ["pdf", "docx", "html", "txt"]
}

MIME_TYPES = {
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "csv": "text/csv",
    "txt": "text/plain",
    "html": "text/html",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "webp": "image/webp",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation"
}

def detect_file_type(filename: str, header_bytes: bytes = b"") -> str:
    """Detects extension and normalized format name."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext

def clean_xml_text(text: str) -> str:
    """Sanitizes text for safe ReportLab XML paragraph rendering."""
    if not text:
        return ""
    sanitized = "".join(ch for ch in text if ch in ("\n", "\r", "\t") or ord(ch) >= 32)
    return sanitized.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def convert_file(file_bytes: bytes, original_filename: str, target_format: str) -> Tuple[bytes, str, str]:
    """
    Converts file_bytes of original_filename to target_format.
    Returns: (converted_bytes, output_filename, mime_type)
    Output filename format: <base_name>_convertedelcai07.<target_format>
    """
    base_name = original_filename.rsplit(".", 1)[0] if "." in original_filename else original_filename
    src_ext = original_filename.rsplit(".", 1)[-1].lower() if "." in original_filename else ""
    target_ext = target_format.lower().lstrip(".")
    out_filename = f"{base_name}_convertedelcai07.{target_ext}"
    mime = MIME_TYPES.get(target_ext, "application/octet-stream")

    # If already target format, return as is
    if src_ext == target_ext:
        return file_bytes, out_filename, mime

    # 1. IMAGE CONVERSIONS (PNG, JPG, WEBP, BMP to PNG, JPG, WEBP, PDF)
    if src_ext in ["jpg", "jpeg", "png", "webp", "bmp", "gif"]:
        img = Image.open(io.BytesIO(file_bytes))
        out_buf = io.BytesIO()

        if target_ext in ["jpg", "jpeg"]:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(out_buf, format="JPEG", quality=92)
            return out_buf.getvalue(), out_filename, "image/jpeg"

        elif target_ext == "png":
            img.save(out_buf, format="PNG")
            return out_buf.getvalue(), out_filename, "image/png"

        elif target_ext == "webp":
            img.save(out_buf, format="WEBP", quality=90)
            return out_buf.getvalue(), out_filename, "image/webp"

        elif target_ext == "pdf":
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(out_buf, format="PDF", resolution=100.0)
            return out_buf.getvalue(), out_filename, "application/pdf"

    # 2. DOCX CONVERSIONS
    if src_ext == "docx":
        doc = Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        for table in doc.tables:
            for row in table.rows:
                cells = [c.text.strip() for c in row.cells if c.text.strip()]
                if cells:
                    paragraphs.append(" | ".join(cells))

        if target_ext == "txt":
            content = "\n\n".join(paragraphs).encode("utf-8")
            return content, out_filename, "text/plain"

        elif target_ext == "html":
            html_parts = [f"<h1>{base_name}</h1>"]
            for p in paragraphs:
                html_parts.append(f"<p>{p}</p>")
            html_content = f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>{base_name}</title><style>body{{font-family:sans-serif;max-width:800px;margin:20px auto;line-height:1.6;}}</style></head><body>{''.join(html_parts)}</body></html>"
            return html_content.encode("utf-8"), out_filename, "text/html"

        elif target_ext == "pdf":
            out_buf = io.BytesIO()
            doc_pdf = SimpleDocTemplate(out_buf, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
            styles = getSampleStyleSheet()
            normal_style = styles["Normal"]
            normal_style.fontSize = 11
            normal_style.leading = 15
            title_style = styles["Title"]
            title_style.fontSize = 18
            title_style.textColor = colors.HexColor("#A6192E")

            story = [Paragraph(f"<b>{clean_xml_text(base_name)}</b>", title_style), Spacer(1, 15)]
            for p in paragraphs:
                safe_text = clean_xml_text(p)
                story.append(Paragraph(safe_text, normal_style))
                story.append(Spacer(1, 8))
            doc_pdf.build(story)
            return out_buf.getvalue(), out_filename, "application/pdf"

    # 3. PDF CONVERSIONS
    if src_ext == "pdf":
        reader = PdfReader(io.BytesIO(file_bytes))
        pages_text = []
        for idx, page in enumerate(reader.pages):
            txt = page.extract_text() or ""
            pages_text.append(txt)

        full_text = "\n\n".join(pages_text)

        if target_ext == "txt":
            return full_text.encode("utf-8"), out_filename, "text/plain"

        elif target_ext == "docx":
            new_doc = Document()
            new_doc.add_heading(base_name, 0)
            for page_idx, p_text in enumerate(pages_text):
                if page_idx > 0:
                    new_doc.add_page_break()
                new_doc.add_heading(f"Page {page_idx + 1}", level=2)
                for line in p_text.splitlines():
                    line = line.strip()
                    if line:
                        new_doc.add_paragraph(line)
            out_buf = io.BytesIO()
            new_doc.save(out_buf)
            return out_buf.getvalue(), out_filename, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

        elif target_ext == "html":
            html_parts = [f"<h1>{base_name} (PDF Extracted)</h1>"]
            for idx, p_text in enumerate(pages_text):
                html_parts.append(f"<div style='border:1px solid #ccc;padding:12px;margin-bottom:12px;'><h3>Page {idx+1}</h3>")
                for line in p_text.splitlines():
                    if line.strip():
                        html_parts.append(f"<p>{line.strip()}</p>")
                html_parts.append("</div>")
            html_content = f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>{base_name}</title><style>body{{font-family:sans-serif;max-width:800px;margin:20px auto;line-height:1.6;}}</style></head><body>{''.join(html_parts)}</body></html>"
            return html_content.encode("utf-8"), out_filename, "text/html"

    # 4. EXCEL & CSV CONVERSIONS
    if src_ext in ["xlsx", "xls", "csv"]:
        rows = []
        if src_ext == "csv":
            text_str = file_bytes.decode("utf-8", errors="replace")
            reader = csv.reader(io.StringIO(text_str))
            rows = list(reader)
        elif src_ext in ["xlsx", "xls"]:
            wb = openpyxl.load_workbook(io.BytesIO(file_bytes), data_only=True)
            ws = wb.active
            for row in ws.iter_rows(values_only=True):
                rows.append([str(c) if c is not None else "" for c in row])

        if target_ext == "csv":
            out_str = io.StringIO()
            writer = csv.writer(out_str)
            for r in rows:
                writer.writerow(r)
            return out_str.getvalue().encode("utf-8"), out_filename, "text/csv"

        elif target_ext == "xlsx":
            new_wb = openpyxl.Workbook()
            new_ws = new_wb.active
            new_ws.title = "Data"
            for r_idx, r in enumerate(rows, 1):
                for c_idx, val in enumerate(r, 1):
                    cell = new_ws.cell(row=r_idx, column=c_idx, value=val)
                    if r_idx == 1:
                        cell.font = Font(bold=True, color="FFFFFF")
                        cell.fill = PatternFill(start_color="A6192E", end_color="A6192E", fill_type="solid")
            out_buf = io.BytesIO()
            new_wb.save(out_buf)
            return out_buf.getvalue(), out_filename, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        elif target_ext == "txt":
            txt_lines = ["\t".join(r) for r in rows]
            return "\n".join(txt_lines).encode("utf-8"), out_filename, "text/plain"

        elif target_ext == "html":
            html_parts = [f"<h1>{base_name}</h1><table border='1' cellpadding='6' style='border-collapse:collapse;width:100%;font-family:sans-serif;'>"]
            for r_idx, r in enumerate(rows):
                tag = "th" if r_idx == 0 else "td"
                bg = "style='background:#a6192e;color:white;'" if r_idx == 0 else ""
                html_parts.append("<tr>" + "".join([f"<{tag} {bg}>{c}</{tag}>" for c in r]) + "</tr>")
            html_parts.append("</table>")
            return f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>{base_name}</title></head><body>{''.join(html_parts)}</body></html>".encode("utf-8"), out_filename, "text/html"

        elif target_ext == "pdf":
            out_buf = io.BytesIO()
            doc_pdf = SimpleDocTemplate(out_buf, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
            story = []
            styles = getSampleStyleSheet()
            story.append(Paragraph(f"<b>{base_name}</b>", styles["Title"]))
            story.append(Spacer(1, 15))
            if rows:
                clean_table_data = [[Paragraph(str(c)[:50], styles["Normal"]) for c in r[:8]] for r in rows[:60]]
                t = Table(clean_table_data)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#A6192E")),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0,0), (-1,0), 6),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                ]))
                story.append(t)
            doc_pdf.build(story)
            return out_buf.getvalue(), out_filename, "application/pdf"

    # 5. PPTX CONVERSIONS
    if src_ext == "pptx":
        prs = Presentation(io.BytesIO(file_bytes))
        slides_text = []
        for idx, slide in enumerate(prs.slides):
            slide_content = []
            for shape in slide.shapes:
                if shape.has_text_frame:
                    for para in shape.text_frame.paragraphs:
                        text = para.text.strip()
                        if text:
                            slide_content.append(text)
            slides_text.append((idx + 1, slide_content))

        if target_ext == "txt":
            out_lines = []
            for s_num, s_lines in slides_text:
                out_lines.append(f"--- SLIDE {s_num} ---")
                out_lines.extend(s_lines)
                out_lines.append("")
            return "\n".join(out_lines).encode("utf-8"), out_filename, "text/plain"

        elif target_ext == "docx":
            new_doc = Document()
            new_doc.add_heading(base_name, 0)
            for s_num, s_lines in slides_text:
                new_doc.add_heading(f"Slide {s_num}", level=2)
                for line in s_lines:
                    new_doc.add_paragraph(line, style='List Bullet')
            out_buf = io.BytesIO()
            new_doc.save(out_buf)
            return out_buf.getvalue(), out_filename, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

        elif target_ext == "pdf":
            out_buf = io.BytesIO()
            doc_pdf = SimpleDocTemplate(out_buf, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
            styles = getSampleStyleSheet()
            story = [Paragraph(f"<b>{clean_xml_text(base_name)} (Presentation Summary)</b>", styles["Title"]), Spacer(1, 15)]
            for s_num, s_lines in slides_text:
                story.append(Paragraph(f"<b>Slide {s_num}</b>", styles["Heading2"]))
                for line in s_lines:
                    safe = clean_xml_text(line)
                    story.append(Paragraph(f"• {safe}", styles["Normal"]))
                story.append(Spacer(1, 10))
            doc_pdf.build(story)
            return out_buf.getvalue(), out_filename, "application/pdf"

        elif target_ext == "html":
            html_parts = [f"<h1>{base_name}</h1>"]
            for s_num, s_lines in slides_text:
                html_parts.append(f"<div style='border:1px solid #ddd;padding:12px;margin:10px 0;border-radius:8px;'><h3>Slide {s_num}</h3><ul>")
                for line in s_lines:
                    html_parts.append(f"<li>{line}</li>")
                html_parts.append("</ul></div>")
            return f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>{base_name}</title><style>body{{font-family:sans-serif;max-width:800px;margin:20px auto;}}</style></head><body>{''.join(html_parts)}</body></html>".encode("utf-8"), out_filename, "text/html"

    # 6. TXT & MD CONVERSIONS
    if src_ext in ["txt", "md"]:
        text_content = file_bytes.decode("utf-8", errors="replace")
        if target_ext == "docx":
            new_doc = Document()
            new_doc.add_heading(base_name, 0)
            for line in text_content.splitlines():
                if line.strip():
                    new_doc.add_paragraph(line.strip())
            out_buf = io.BytesIO()
            new_doc.save(out_buf)
            return out_buf.getvalue(), out_filename, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

        elif target_ext == "pdf":
            out_buf = io.BytesIO()
            doc_pdf = SimpleDocTemplate(out_buf, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
            styles = getSampleStyleSheet()
            story = [Paragraph(f"<b>{clean_xml_text(base_name)}</b>", styles["Title"]), Spacer(1, 15)]
            for line in text_content.splitlines():
                if line.strip():
                    safe = clean_xml_text(line)
                    story.append(Paragraph(safe, styles["Normal"]))
                    story.append(Spacer(1, 6))
            doc_pdf.build(story)
            return out_buf.getvalue(), out_filename, "application/pdf"

        elif target_ext == "html":
            html_p = "".join([f"<p>{p.strip()}</p>" for p in text_content.splitlines() if p.strip()])
            return f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>{base_name}</title><style>body{{font-family:sans-serif;max-width:800px;margin:20px auto;line-height:1.6;}}</style></head><body><h1>{base_name}</h1>{html_p}</body></html>".encode("utf-8"), out_filename, "text/html"

    raise ValueError(f"Dönüştürme desteklenmiyor: {src_ext} -> {target_ext}")
