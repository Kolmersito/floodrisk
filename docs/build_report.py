"""Genera el informe PDF desde su fuente Markdown; requiere reportlab."""
from pathlib import Path
from xml.sax.saxutils import escape
import argparse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parent

def build(target, source=None, label='Informe v3', date='17 de octubre de 2026'):
    font_dir = Path('C:/Windows/Fonts')
    regular, bold = 'Helvetica', 'Helvetica-Bold'
    if (font_dir/'arial.ttf').exists():
        pdfmetrics.registerFont(TTFont('Report',str(font_dir/'arial.ttf')))
        pdfmetrics.registerFont(TTFont('ReportBold',str(font_dir/'arialbd.ttf')))
        regular,bold='Report','ReportBold'
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='TextReport',fontName=regular,fontSize=9.3,leading=12.5,spaceAfter=8))
    styles.add(ParagraphStyle(name='TitleReport',fontName=bold,fontSize=23,leading=28,spaceAfter=20,textColor=HexColor('#17324D')))
    styles.add(ParagraphStyle(name='HeadingReport',fontName=bold,fontSize=16,leading=20,spaceBefore=16,spaceAfter=15,keepWithNext=True,textColor=HexColor('#17324D')))
    styles.add(ParagraphStyle(name='SmallHeadingReport',fontName=bold,fontSize=11,leading=15,spaceAfter=9,keepWithNext=True))
    styles.add(ParagraphStyle(name='CellReport',fontName=regular,fontSize=8.6,leading=11.5))
    styles.add(ParagraphStyle(name='HeaderReport',fontName=bold,fontSize=8.6,leading=11.5,textColor=white))
    story=[]
    lines=(source or ROOT/'informe_v3.md').read_text(encoding='utf-8').splitlines()
    i=0
    while i<len(lines):
        line=lines[i].strip();i+=1
        if not line:continue
        if line.startswith('## '):
            if source is None:
                story.append(PageBreak())
            story.append(Paragraph(escape(line[3:]),styles['HeadingReport']))
        elif line.startswith('# '):story.append(Paragraph(escape(line[2:]),styles['TitleReport']))
        elif line.startswith('### '):story.append(Paragraph(escape(line[4:]),styles['SmallHeadingReport']))
        elif line.startswith('|'):
            raw=[line]
            while i<len(lines) and lines[i].startswith('|'):raw.append(lines[i]);i+=1
            rows=[[c.strip() for c in r.strip('|').split('|')] for r in raw]
            rows=[r for r in rows if not all(set(c)<=set('-: ') for c in r)]
            n=len(rows[0]);widths={3:[158,84,262],4:[130,110,130,134],5:[135,75,90,90,114]}.get(n,[504/n]*n)
            if rows[0][0]=='Código':widths=[48,180,276]
            if rows[0][0]=='Riesgo' and n==3:widths=[120,200,184]
            if rows[0][0]=='ID' and n==3:widths=[58,190,256]
            if n==2:widths=[150,354]
            cells=[[Paragraph(escape(c),styles['HeaderReport' if j==0 else 'CellReport']) for c in row] for j,row in enumerate(rows)]
            t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT')
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#17324D')),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#F0F5F9')]),('GRID',(0,0),(-1,-1),.4,HexColor('#D4DFE7')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
            story.extend([t,Spacer(1,12)])
        else:story.append(Paragraph(escape(line),styles['TextReport']))
    def footer(c,doc):
        c.setFont(regular,8);c.setFillColor(HexColor('#64748B'))
        c.drawString(54,28,f'FloodRisk | {label} | {date}')
        c.drawRightString(558,28,str(doc.page))
    target.parent.mkdir(parents=True,exist_ok=True)
    SimpleDocTemplate(str(target),pagesize=letter,leftMargin=54,rightMargin=54,topMargin=46,bottomMargin=47,title=f'FloodRisk - {label}',author='Equipo FloodRisk').build(story,onFirstPage=footer,onLaterPages=footer)
    print(target)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=ROOT/'FloodRisk_Informe_v3.pdf')
    parser.add_argument('--source',type=Path)
    parser.add_argument('--label',default='Informe v3')
    parser.add_argument('--date',default='17 de octubre de 2026')
    args=parser.parse_args()
    build(args.output,args.source,args.label,args.date)
