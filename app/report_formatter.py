from jinja2 import Template
from datetime import datetime, timezone
import io
from xhtml2pdf import pisa

def format_report_html(data):
    """
    Formats the raw JSON data into a premium, modern dashboard.
    """
    if not data or data.get("status") != "success":
        return None
        
    candidates = data.get("candidates", [])
    summary = data.get("summary", {})
    now_str = datetime.now(timezone.utc).strftime('%B %d, %Y')
    
    # Final Comprehensive Template (Full Detail)
    template_html = """
    <html>
    <head>
        <style>
            table { border-collapse: collapse; width: 100%; border: 1px solid #e2e8f0; }
            th { border: 1px solid #ffffff; padding: 10px; font-size: 10px; text-transform: uppercase; background-color: #3b5998; color: #ffffff; }
            td { border: 1px solid #e2e8f0; padding: 10px; font-size: 10px; text-align: center; }
        </style>
    </head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f3f4f6; margin: 0; padding: 40px 10px;">
        <div style="max-width: 1100px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); overflow: hidden;">
            
            <div style="background-color: #1f2937; color: #ffffff; padding: 30px; text-align: center;">
                <h1 style="margin: 0; font-size: 24px; font-weight: 600; letter-spacing: 0.5px;">Weekly Marketing Report</h1>
                <p style="margin: 10px 0 0 0; font-size: 14px; color: #9ca3af;">{{ summary.start_date }}{% if summary.end_date %} &mdash; {{ summary.end_date }}{% endif %}</p>
                {% if not is_pdf %}
                <div style="margin-top: 15px;">
                    <a href="https://api.whitebox-learning.com/api/report-pdf?key=wbl_marketing_secret_2024" style="display: inline-block; background-color: #3b82f6; color: #ffffff; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: 600;">Download PDF Report</a>
                </div>
                {% endif %}
            </div>
            
            <div style="padding: 20px;">
                <table width="100%" cellpadding="0" cellspacing="5" style="margin-bottom: 25px; border: none;">
                    <tr>
                        <td width="25%" style="background-color: #f9fafb; padding: 15px; text-align: center; border-radius: 6px; border: 1px solid #e5e7eb;">
                            <div style="font-size: 24px; font-weight: bold; color: #3b82f6;">{{ summary.total_candidates }}</div>
                            <div style="font-size: 10px; color: #6b7280; text-transform: uppercase;">Candidates</div>
                        </td>
                        <td width="25%" style="background-color: #f9fafb; padding: 15px; text-align: center; border-radius: 6px; border: 1px solid #e5e7eb;">
                            <div style="font-size: 24px; font-weight: bold; color: #10b981;">{{ summary.total_interviews }}</div>
                            <div style="font-size: 10px; color: #6b7280; text-transform: uppercase;">Interviews</div>
                        </td>
                        <td width="25%" style="background-color: #f9fafb; padding: 15px; text-align: center; border-radius: 6px; border: 1px solid #e5e7eb;">
                            <div style="font-size: 24px; font-weight: bold; color: #f59e0b;">{{ summary.total_clicks }}</div>
                            <div style="font-size: 10px; color: #6b7280; text-transform: uppercase;">Job Clicks</div>
                        </td>
                    </tr>
                </table>

                <div style="overflow-x: auto;">
                    <table width="100%" cellpadding="0" cellspacing="0" style="border: 1px solid #e2e8f0;">
                        <thead>
                            <tr>
                                <th rowspan="2" style="background-color: #3b5998;">Candidate</th>
                                <th colspan="4" style="background-color: #4d71bb;">APPLICATIONS</th>
                                <th colspan="4" style="background-color: #6d8acb;">INTERVIEWS</th>
                                <th rowspan="2" style="background-color: #38ada9;">Total</th>
                                <th colspan="3" style="background-color: #8da3dc;">FEEDBACK</th>
                            </tr>
                            <tr style="background-color: #f0f4f8; color: #334e81; font-size: 8px;">
                                <th style="color: #334e81; background-color: #f0f4f8;">EMAIL OUTREACH</th>
                                <th style="color: #334e81; background-color: #f0f4f8;">LINKEDIN EA</th>
                                <th style="color: #334e81; background-color: #f0f4f8;">PORTAL AUTO</th>
                                <th style="color: #334e81; background-color: #f0f4f8;">CLICKS</th>
                                <th style="color: #334e81; background-color: #f0f4f8;">ASSESS</th>
                                <th style="color: #334e81; background-color: #f0f4f8;">RECRUIT</th>
                                <th style="color: #334e81; background-color: #f0f4f8;">TECH</th>
                                <th style="color: #334e81; background-color: #f0f4f8;">ONSITE</th>
                                <th style="color: #16a34a; background-color: #f0f4f8;">POS</th>
                                <th style="color: #ef4444; background-color: #f0f4f8;">NEG</th>
                                <th style="color: #d97706; background-color: #f0f4f8;">PEND</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for c in candidates %}
                            <tr style="background-color: {{ '#ffffff' if loop.index0 % 2 == 0 else '#f8fafc' }};">
                                <td style="text-align: left; font-weight: 600; padding-left: 10px;">{{ c.full_name }}</td>
                                <td>{{ c.outreach_count or '0' }}</td>
                                <td>{{ c.linkedin_easy_apply_count or '0' }}</td>
                                <td>{{ c.job_portal_automation_count or '0' }}</td>
                                <td style="color: #ea580c; font-weight: bold;">{{ c.job_clicks or '0' }}</td>
                                <td>{{ c.assessment_count or '0' }}</td>
                                <td>{{ c.recruiter_call_count or '0' }}</td>
                                <td>{{ c.technical_count or '0' }}</td>
                                <td>{{ c.onsite_count or '0' }}</td>
                                <td style="background-color: #ecfdf5; font-weight: 800;">{{ c.total_interviews or '0' }}</td>
                                <td style="color: #16a34a; font-weight: bold;">{{ c.feedback_positive or '0' }}</td>
                                <td style="color: #ef4444; font-weight: bold;">{{ c.feedback_negative or '0' }}</td>
                                <td style="color: #d97706; font-weight: bold;">{{ c.feedback_pending or '0' }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div style="background-color: #f9fafb; padding: 20px; text-align: center; border-top: 1px solid #e5e7eb;">
                <p style="margin: 0; font-size: 11px; color: #9ca3af;">Whitebox Learning Audit System • Generated on {{ now_str }}</p>
            </div>
            
        </div>
    </body>
    </html>
    """
    
    template = Template(template_html)
    return template.render(
        candidates=candidates, 
        summary=summary,
        now_str=now_str
    )
    
    template = Template(template_html)
    return template.render(
        candidates=candidates, 
        summary=summary,
        now_str=now_str,
        is_pdf=False
    )

def create_report_pdf(data):
    """
    Converts the report data into a PDF using fpdf2 (Zero-dependency).
    """
    from fpdf import FPDF
    summary = data.get("summary", {})
    candidates = data.get("candidates", [])
    now_str = datetime.now(timezone.utc).strftime('%B %d, %Y')
    
    # Initialize PDF in Landscape mode
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    
    # 1. Header Section
    pdf.set_fill_color(31, 41, 55) # Dark Gray
    pdf.rect(0, 0, 297, 40, 'F')
    
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_y(10)
    pdf.cell(0, 10, "Weekly Marketing Report", 0, 1, 'C')
    
    pdf.set_font("Helvetica", "", 10)
    date_label = summary.get('start_date', '')
    if summary.get('end_date'):
        date_label += f" - {summary.get('end_date')}"
    pdf.cell(0, 10, date_label, 0, 1, 'C')
    
    # 2. Summary Boxes
    pdf.set_y(45)
    pdf.set_text_color(31, 41, 55)
    
    # Box styles
    box_w = 90
    box_h = 20
    startX = (297 - (box_w * 3)) / 2
    
    def draw_box(x, y, value, label, color):
        pdf.set_draw_color(229, 231, 235)
        pdf.set_fill_color(249, 250, 251)
        pdf.rect(x, y, box_w, box_h, 'DF')
        
        pdf.set_xy(x, y + 4)
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(color[0], color[1], color[2])
        pdf.cell(box_w, 7, str(value), 0, 1, 'C')
        
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(107, 114, 128)
        pdf.cell(box_w, 5, label, 0, 0, 'C')

    draw_box(startX, 45, summary.get('total_candidates', 0), "CANDIDATES", (59, 130, 246))
    draw_box(startX + box_w, 45, summary.get('total_interviews', 0), "INTERVIEWS", (16, 185, 129))
    draw_box(startX + (box_w*2), 45, summary.get('total_clicks', 0), "JOB CLICKS", (245, 158, 11))

    # 3. Table Header
    pdf.set_y(75)
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_text_color(255, 255, 255)
    pdf.set_fill_color(59, 89, 152) # Dark Blue
    
    cols = [
        ("Candidate", 35),
        ("EMAIL", 18), ("LINKEDIN", 18), ("PORTAL", 18), ("CLICKS", 18),
        ("ASSESS", 18), ("RECRUIT", 18), ("TECH", 18), ("ONSITE", 18),
        ("Total", 18),
        ("POS", 18), ("NEG", 18), ("PEND", 18)
    ]
    
    # Primary Header Row
    startX_table = 10
    pdf.set_x(startX_table)
    
    # Draw Headers
    for label, width in cols:
        pdf.cell(width, 10, label, 1, 0, 'C', True)
    pdf.ln()

    # 4. Table Body
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(31, 41, 55)
    
    for i, c in enumerate(candidates):
        pdf.set_x(startX_table)
        
        # Zebra striping
        if i % 2 == 1:
            pdf.set_fill_color(248, 250, 252)
        else:
            pdf.set_fill_color(255, 255, 255)
            
        # Draw cells
        pdf.cell(35, 8, str(c.get('full_name', '')), 1, 0, 'L', True)
        pdf.cell(18, 8, str(c.get('outreach_count', 0)), 1, 0, 'C', True)
        pdf.cell(18, 8, str(c.get('linkedin_easy_apply_count', 0)), 1, 0, 'C', True)
        pdf.cell(18, 8, str(c.get('job_portal_automation_count', 0)), 1, 0, 'C', True)
        
        pdf.set_text_color(234, 88, 12) # Orange for clicks
        pdf.cell(18, 8, str(c.get('job_clicks', 0)), 1, 0, 'C', True)
        pdf.set_text_color(31, 41, 55)
        
        pdf.cell(18, 8, str(c.get('assessment_count', 0)), 1, 0, 'C', True)
        pdf.cell(18, 8, str(c.get('recruiter_call_count', 0)), 1, 0, 'C', True)
        pdf.cell(18, 8, str(c.get('technical_count', 0)), 1, 0, 'C', True)
        pdf.cell(18, 8, str(c.get('onsite_count', 0)), 1, 0, 'C', True)
        
        pdf.set_font("Helvetica", "B", 7)
        pdf.set_fill_color(236, 253, 245)
        pdf.cell(18, 8, str(c.get('total_interviews', 0)), 1, 0, 'C', True)
        
        pdf.set_font("Helvetica", "", 7)
        pdf.set_text_color(22, 163, 74) # Green
        pdf.cell(18, 8, str(c.get('feedback_positive', 0)), 1, 0, 'C', True)
        pdf.set_text_color(239, 68, 68) # Red
        pdf.cell(18, 8, str(c.get('feedback_negative', 0)), 1, 0, 'C', True)
        pdf.set_text_color(217, 119, 6) # Amber
        pdf.cell(18, 8, str(c.get('feedback_pending', 0)), 1, 0, 'C', True)
        pdf.set_text_color(31, 41, 55)
        pdf.ln()

    # Footer
    pdf.set_y(-20)
    pdf.set_font("Helvetica", "I", 7)
    pdf.set_text_color(156, 163, 175)
    pdf.cell(0, 10, f"Whitebox Learning Audit System - Generated on {now_str}", 0, 0, 'C')

    return pdf.output()
