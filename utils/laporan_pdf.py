"""
Helper untuk cetak laporan manifest penumpang ke PDF (ReportLab).
Dipakai oleh LaporanView.
"""

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer,
        Table, TableStyle, HRFlowable
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

from datetime import datetime


def cetak_laporan_pdf(
    data: list,
    judul: str,
    output_path: str
) -> bool:
    """
    Cetak laporan manifest ke PDF.

    data  : list of tuple (id_tiket, nama, golongan, nopol,
                           nama_kapal, asal, tujuan, total_bayar, ...)
    judul : string keterangan periode
    output_path : path file PDF tujuan
    """

    if not HAS_REPORTLAB:
        return False

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=15*mm,
        rightMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm
    )

    styles = getSampleStyleSheet()

    h1 = ParagraphStyle(
        'h1',
        fontSize=16,
        fontName='Helvetica-Bold',
        alignment=TA_CENTER,
        textColor=colors.HexColor('#003366')
    )

    sub = ParagraphStyle(
        'sub',
        fontSize=10,
        fontName='Helvetica',
        alignment=TA_CENTER,
        textColor=colors.grey
    )

    footer_style = ParagraphStyle(
        'footer',
        fontSize=9,
        fontName='Helvetica-Bold',
        alignment=TA_RIGHT,
        textColor=colors.HexColor('#003366')
    )

    ts_style = ParagraphStyle(
        'ts',
        fontSize=8,
        fontName='Helvetica',
        alignment=TA_RIGHT,
        textColor=colors.grey
    )

    story = []

    story.append(Paragraph("FERRYBOOK — LAPORAN MANIFEST PENUMPANG", h1))
    story.append(Paragraph(judul, sub))
    story.append(Spacer(1, 4*mm))
    story.append(HRFlowable(
        width="100%", thickness=2,
        color=colors.HexColor('#003366')
    ))
    story.append(Spacer(1, 3*mm))

    header = [
        "ID Tiket", "Nama", "Golongan", "No. Pol",
        "Kapal", "Asal", "Tujuan", "Total Bayar"
    ]

    rows = [header]
    total_pendapatan = 0

    for t in data:
        rows.append([
            str(t[0]),
            t[1],
            t[2],
            t[3] or "-",
            t[4],
            t[5],
            t[6],
            f"Rp {int(t[7]):,}".replace(",", ".")
        ])
        total_pendapatan += t[7]

    col_widths = [
        18*mm, 32*mm, 28*mm, 22*mm,
        28*mm, 18*mm, 18*mm, 26*mm
    ]

    tbl = Table(rows, colWidths=col_widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR',     (0, 0), (-1, 0), colors.white),
        ('FONTNAME',      (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1,-1), 7),
        ('FONTNAME',      (0, 1), (-1,-1), 'Helvetica'),
        ('ROWBACKGROUNDS',(0, 1), (-1,-1),
         [colors.HexColor('#EEF2FF'), colors.white]),
        ('GRID',          (0, 0), (-1,-1), 0.25, colors.HexColor('#AAAAAA')),
        ('TOPPADDING',    (0, 0), (-1,-1), 3),
        ('BOTTOMPADDING', (0, 0), (-1,-1), 3),
        ('ALIGN',         (0, 0), (-1,-1), 'LEFT'),
        ('ALIGN',         (-1, 0),(-1,-1), 'RIGHT'),
        ('VALIGN',        (0, 0), (-1,-1), 'MIDDLE'),
    ]))

    story.append(tbl)
    story.append(Spacer(1, 4*mm))
    story.append(HRFlowable(
        width="100%", thickness=1,
        color=colors.HexColor('#003366')
    ))
    story.append(Paragraph(
        f"Total Tiket: {len(data)}  |  "
        f"Total Pendapatan: Rp {int(total_pendapatan):,}".replace(",", "."),
        footer_style
    ))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        f"Dicetak: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        ts_style
    ))

    doc.build(story)
    return True
