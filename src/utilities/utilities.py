import base64
import datetime
import io
import os
import sqlite3

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Flowable
from reportlab.platypus.para import Paragraph

from src import logger, app
from src.constants import sql_object


def image_to_byte_array(image_uri):
    if os.path.exists(image_uri):
        with open(image_uri, "rb") as image_object:
            image_bytes = image_object.read()
            image_bytes_string = base64.b64encode(image_bytes)
            return str(image_bytes_string).replace("b\'", "data:image/jpeg;base64,").replace("\'", "")
    return ''


def save_pdf(item, image_byte):
    pdf_elements = []
    # List of Lists
    data = [
        ['Code', ':', item['code']],
        ['Model No', ':', item['modelno']],
        ['Manufacturer', ':', item['manufacturer']],
        ['Make', ':', item['make']],
        ['Dimensions', ':', item['dimensions']],
        ['Color', ':', item['color']],
        ['Price', ':', '$'+item['price']]
    ]

    from reportlab.platypus import SimpleDocTemplate

    buff = io.BytesIO()
    pdf = SimpleDocTemplate(
        buff,
        title=item['code'],
        pagesize=(4.55*inch, 5.15*inch),
        leftMargin=.2*inch,
        rightMargin=.2*inch,
        topMargin=.2*inch,
        bottomMargin=.2*inch,
    )

    from reportlab.platypus import Table
    table = Table(data)

    # add style
    from reportlab.platypus import TableStyle

    style = TableStyle([
        ('TOPPADDING', (0, 0), (-1, 0), 20),
        ('FONTNAME', (0, 0), (0, -1), 'Courier-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 14),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
    ])
    table.setStyle(style)

    pic = flowable_fig(image_byte)
    pdf_elements.append(pic)

    style = getSampleStyleSheet()['Normal']
    pdf_elements.append(Paragraph('<b></b>', style))

    sp = ParagraphStyle(name='Center',
                        spaceBefore=150,
                        textColor=colors.blue,
                        alignment=TA_CENTER,
                        fontSize=16,
                        fontName="Times-Roman")
    pdf_elements.append(Paragraph(item['display_name'], sp))

    pdf_elements.append(table)

    pdf.build(pdf_elements)
    pdf_bytes = buff.getvalue()
    buff.close()
    return pdf_bytes


class flowable_fig(Flowable):
    def __init__(self, imgdata):
        Flowable.__init__(self)
        self.img = ImageReader(imgdata)

    def draw(self):
        self.canv.drawImage(self.img, 0, 0, height=-2.2 * inch, width=4 * inch)


def has_user_expired(username):
    # Check if user is expired or not
    logger.info("Check if user is expired or not")
    now = datetime.datetime.now()

    # Create database connection with sqlite database
    conn = sqlite3.connect(app.config['SQLALCHEMY_DATABASE_FILE'])
    cursor = conn.cursor()
    updated_query = sql_object.UPDATE_LAST_ACTIVE_USER_BY_NAME.format(now, username, now)
    logger.info("UPDATE_LAST_ACTIVE_USER_BY_NAME query %s", updated_query)

    # Execute query and fetch result
    rows_affected = cursor.execute(updated_query)
    conn.commit()
    return rows_affected.rowcount == 0 if True else False