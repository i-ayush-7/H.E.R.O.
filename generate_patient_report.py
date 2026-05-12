"""
Generate a professional clinical report PDF for patient Priya Sharma.
Used for PromptOpinion hackathon demo.
"""
from fpdf import FPDF
from datetime import datetime, timedelta
import os

class ClinicalReportPDF(FPDF):
    
    NAVY = (10, 36, 99)
    DARK_GRAY = (51, 51, 51)
    MED_GRAY = (100, 100, 100)
    LIGHT_BG = (245, 247, 250)
    ACCENT = (0, 102, 178)
    BORDER_LINE = (180, 195, 220)
    WHITE = (255, 255, 255)
    RED_ALERT = (180, 30, 30)

    def header(self):
        # Top accent bar
        self.set_fill_color(*self.NAVY)
        self.rect(0, 0, 210, 3, 'F')
        
        # Hospital name block
        self.set_y(8)
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(*self.NAVY)
        self.cell(0, 8, 'Apollo Multispecialty Hospital', ln=True, align='C')
        
        self.set_font('Helvetica', '', 8)
        self.set_text_color(*self.MED_GRAY)
        self.cell(0, 4, '154/11, Bannerghatta Road, Opposite IIM, Bengaluru, Karnataka 560076', ln=True, align='C')
        self.cell(0, 4, 'Ph: +91-80-2630-4050  |  NABH Accredited  |  Reg. No: KA/BLR/MH-2019/04872', ln=True, align='C')
        
        # Separator
        self.set_y(28)
        self.set_draw_color(*self.BORDER_LINE)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)
    
    def footer(self):
        self.set_y(-22)
        self.set_draw_color(*self.BORDER_LINE)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)
        self.set_font('Helvetica', 'I', 7)
        self.set_text_color(*self.MED_GRAY)
        self.cell(0, 3, 'This is a computer-generated document. Authentication is verified via digital signature.', ln=True, align='C')
        self.cell(0, 3, f'Report ID: APL-BLR-{datetime.now().strftime("%Y%m%d")}-07284  |  Printed: {datetime.now().strftime("%d-%b-%Y %H:%M IST")}', ln=True, align='C')
        self.cell(0, 3, f'Page {self.page_no()}/{{nb}}', align='C')

    def section_title(self, title):
        self.ln(3)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*self.WHITE)
        self.set_fill_color(*self.NAVY)
        self.cell(0, 7, f'  {title}', ln=True, fill=True)
        self.ln(1)
    
    def info_row(self, label, value, bold_value=False):
        self.set_font('Helvetica', '', 9)
        self.set_text_color(*self.MED_GRAY)
        x = self.get_x()
        self.cell(42, 5.5, label, border=0)
        self.set_text_color(*self.DARK_GRAY)
        if bold_value:
            self.set_font('Helvetica', 'B', 9)
        self.cell(0, 5.5, value, ln=True, border=0)
    
    def vital_row(self, parameter, value, unit, ref_range, flag=""):
        self.set_font('Helvetica', '', 9)
        self.set_text_color(*self.DARK_GRAY)
        self.cell(55, 5.5, parameter)
        
        if flag == "H" or flag == "L":
            self.set_font('Helvetica', 'B', 9)
            self.set_text_color(*self.RED_ALERT)
        self.cell(30, 5.5, str(value))
        
        self.set_font('Helvetica', '', 9)
        self.set_text_color(*self.DARK_GRAY)
        self.cell(25, 5.5, unit)
        self.set_text_color(*self.MED_GRAY)
        self.cell(35, 5.5, ref_range)
        
        if flag:
            self.set_font('Helvetica', 'B', 8)
            self.set_text_color(*self.RED_ALERT)
            self.cell(10, 5.5, flag)
        self.ln()
    
    def table_header(self, cols):
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(*self.NAVY)
        self.set_fill_color(*self.LIGHT_BG)
        for text, width in cols:
            self.cell(width, 6, text, border=0, fill=True)
        self.ln()


def generate_report():
    pdf = ClinicalReportPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=25)
    pdf.add_page()
    
    admit_date = datetime.now() - timedelta(days=3)
    discharge_date = datetime.now() - timedelta(days=1)
    report_date = datetime.now()
    dob = datetime(2002, 3, 15)
    
    # ─── DOCUMENT TITLE ───
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(*ClinicalReportPDF.NAVY)
    pdf.cell(0, 8, 'DISCHARGE SUMMARY & CLINICAL REPORT', ln=True, align='C')
    pdf.ln(1)

    # ─── PATIENT DEMOGRAPHICS ───
    pdf.section_title('PATIENT INFORMATION')
    
    col1_x = 10
    col2_x = 105
    y_start = pdf.get_y()
    
    pdf.set_x(col1_x)
    pdf.info_row('Patient Name:', 'PRIYA SHARMA', bold_value=True)
    pdf.set_x(col1_x)
    pdf.info_row('Date of Birth:', dob.strftime('%d-%b-%Y'))
    pdf.set_x(col1_x)
    pdf.info_row('Age / Gender:', '24 Years / Female')
    pdf.set_x(col1_x)
    pdf.info_row('Blood Group:', 'B+ (Positive)')
    pdf.set_x(col1_x)
    pdf.info_row('Aadhaar (last 4):', 'XXXX-XXXX-7842')
    
    y_after_col1 = pdf.get_y()
    pdf.set_y(y_start)
    
    pdf.set_x(col2_x)
    pdf.info_row('MRN:', 'APL-2026-048271')
    pdf.set_x(col2_x)
    pdf.info_row('UHID:', 'UH-0948-2026-BLR')
    pdf.set_x(col2_x)
    pdf.info_row('Admission Date:', admit_date.strftime('%d-%b-%Y, %I:%M %p'))
    pdf.set_x(col2_x)
    pdf.info_row('Discharge Date:', discharge_date.strftime('%d-%b-%Y, %I:%M %p'))
    pdf.set_x(col2_x)
    pdf.info_row('Attending Doctor:', 'Dr. Meera Krishnan, MD (Pulm.)')
    
    pdf.set_y(max(y_after_col1, pdf.get_y()) + 2)
    
    # ─── CHIEF COMPLAINTS ───
    pdf.section_title('CHIEF COMPLAINTS & PRESENTING ILLNESS')
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(*ClinicalReportPDF.DARK_GRAY)
    pdf.multi_cell(0, 5, 
        'The patient presented to the Emergency Department with acute onset shortness of breath (dyspnea) '
        'and audible wheezing for the past 6 hours. She reported worsening symptoms triggered by exposure to '
        'construction dust near her workplace. She also complained of persistent chest tightness and mild '
        'palpitations. She has a known history of bronchial asthma since childhood with intermittent '
        'exacerbations. She denied fever, hemoptysis, or recent upper respiratory infection.\n\n'
        'On further questioning, the patient also reported occasional headaches and dizziness over the past '
        '2 months. She was found to have elevated blood pressure readings during triage (148/94 mmHg).'
    )
    
    # ─── MEDICAL HISTORY ───
    pdf.section_title('PAST MEDICAL HISTORY & COMORBIDITIES')
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(*ClinicalReportPDF.DARK_GRAY)
    
    conditions = [
        ('Mild Persistent Asthma (J45.30)', 'Diagnosed at age 8. Uses Salbutamol MDI PRN. Last exacerbation 4 months ago.'),
        ('Essential Hypertension, Stage 1 (I10)', 'Newly diagnosed during this admission. No prior antihypertensive therapy.'),
        ('Allergic Rhinitis (J30.1)', 'Seasonal. Managed with intranasal corticosteroids intermittently.'),
        ('Iron Deficiency Anemia - Resolved (D50.9)', 'Treated and resolved in 2024. Hb normalized.')
    ]
    
    for code, desc in conditions:
        pdf.set_font('Helvetica', 'B', 9)
        pdf.set_text_color(*ClinicalReportPDF.ACCENT)
        pdf.cell(5, 5, '>')  # bullet
        pdf.set_text_color(*ClinicalReportPDF.DARK_GRAY)
        pdf.cell(85, 5, code)
        pdf.set_font('Helvetica', '', 8)
        pdf.set_text_color(*ClinicalReportPDF.MED_GRAY)
        pdf.cell(0, 5, desc, ln=True)

    # ─── VITALS AT ADMISSION ───
    pdf.section_title('VITAL SIGNS (Recorded at Admission)')
    
    pdf.table_header([
        ('Parameter', 55), ('Value', 30), ('Unit', 25), ('Reference', 35), ('Flag', 10)
    ])
    
    pdf.vital_row('Heart Rate (Pulse)', '112', 'beats/min', '60 - 100', 'H')
    pdf.vital_row('Blood Pressure (Systolic)', '148', 'mmHg', '90 - 120', 'H')
    pdf.vital_row('Blood Pressure (Diastolic)', '94', 'mmHg', '60 - 80', 'H')
    pdf.vital_row('Oxygen Saturation (SpO2)', '91', '%', '95 - 100', 'L')
    pdf.vital_row('Respiratory Rate', '26', 'breaths/min', '12 - 20', 'H')
    pdf.vital_row('Body Temperature', '37.1', 'deg C', '36.1 - 37.2', '')
    pdf.vital_row('BMI', '22.4', 'kg/m' + '2', '18.5 - 24.9', '')

    # ─── VITALS AT DISCHARGE ───
    pdf.section_title('VITAL SIGNS (Recorded at Discharge)')
    
    pdf.table_header([
        ('Parameter', 55), ('Value', 30), ('Unit', 25), ('Reference', 35), ('Flag', 10)
    ])
    
    pdf.vital_row('Heart Rate (Pulse)', '78', 'beats/min', '60 - 100', '')
    pdf.vital_row('Blood Pressure (Systolic)', '126', 'mmHg', '90 - 120', 'H')
    pdf.vital_row('Blood Pressure (Diastolic)', '82', 'mmHg', '60 - 80', 'H')
    pdf.vital_row('Oxygen Saturation (SpO2)', '97', '%', '95 - 100', '')
    pdf.vital_row('Respiratory Rate', '16', 'breaths/min', '12 - 20', '')
    pdf.vital_row('Body Temperature', '36.8', 'deg C', '36.1 - 37.2', '')

    # ─── LAB RESULTS ───
    pdf.section_title('LABORATORY INVESTIGATIONS')
    
    pdf.table_header([
        ('Test', 55), ('Result', 30), ('Unit', 25), ('Reference', 35), ('Flag', 10)
    ])
    
    pdf.vital_row('Hemoglobin', '12.8', 'g/dL', '12.0 - 15.5', '')
    pdf.vital_row('Total WBC Count', '9,200', '/cumm', '4,000 - 11,000', '')
    pdf.vital_row('Platelet Count', '2.4', 'Lakh/cumm', '1.5 - 4.0', '')
    pdf.vital_row('ESR', '18', 'mm/hr', '0 - 20', '')
    pdf.vital_row('Serum IgE (Total)', '485', 'IU/mL', '< 100', 'H')
    pdf.vital_row('Serum Creatinine', '0.8', 'mg/dL', '0.6 - 1.2', '')
    pdf.vital_row('Fasting Blood Glucose', '92', 'mg/dL', '70 - 100', '')
    pdf.vital_row('HbA1c', '5.2', '%', '< 5.7', '')
    pdf.vital_row('Total Cholesterol', '195', 'mg/dL', '< 200', '')
    pdf.vital_row('Serum Sodium', '140', 'mEq/L', '136 - 145', '')
    pdf.vital_row('Serum Potassium', '4.1', 'mEq/L', '3.5 - 5.0', '')

    # ─── PULMONARY FUNCTION ───
    pdf.section_title('PULMONARY FUNCTION TEST (SPIROMETRY)')
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(*ClinicalReportPDF.DARK_GRAY)
    
    pdf.table_header([
        ('Parameter', 55), ('Pre-BD', 30), ('Post-BD', 25), ('Predicted', 35), ('', 10)
    ])
    pdf.vital_row('FEV1', '2.1 L (72%)', '2.6 L (89%)', '2.92 L', '')
    pdf.vital_row('FVC', '3.0 L (85%)', '3.2 L (91%)', '3.52 L', '')
    pdf.vital_row('FEV1/FVC Ratio', '70%', '81%', '> 75%', '')
    
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(*ClinicalReportPDF.MED_GRAY)
    pdf.cell(0, 5, 'Interpretation: Mild obstructive pattern with significant bronchodilator reversibility (> 12%). Consistent with asthma.', ln=True)

    # ─── TREATMENT GIVEN ───
    pdf.section_title('TREATMENT ADMINISTERED DURING HOSPITALIZATION')
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(*ClinicalReportPDF.DARK_GRAY)
    
    treatments = [
        'Nebulization with Salbutamol 2.5mg + Ipratropium 0.5mg Q6H for 48 hours',
        'IV Hydrocortisone 100mg STAT, followed by oral Prednisolone 40mg OD x 5 days (tapering)',
        'Oxygen supplementation via nasal cannula at 2L/min for 12 hours',
        'Tab. Montelukast 10mg OD (added for long-term asthma control)',
        'Tab. Amlodipine 5mg OD (initiated for newly diagnosed hypertension)',
        'Fluticasone/Salmeterol MDI 250/50mcg 1 puff BD (step-up controller therapy)',
        'IV Normal Saline 0.9% for hydration during first 24 hours'
    ]
    
    for t in treatments:
        pdf.set_font('Helvetica', '', 8)
        pdf.set_text_color(*ClinicalReportPDF.ACCENT)
        pdf.cell(5, 4.5, '>')
        pdf.set_text_color(*ClinicalReportPDF.DARK_GRAY)
        pdf.cell(0, 4.5, t, ln=True)
    
    # ─── DISCHARGE MEDICATIONS ───
    pdf.section_title('DISCHARGE PRESCRIPTION')
    
    pdf.table_header([
        ('Medication', 65), ('Dosage', 30), ('Frequency', 35), ('Duration', 25)
    ])
    
    meds = [
        ('Tab. Amlodipine', '5 mg', 'Once daily (AM)', '30 days'),
        ('Tab. Montelukast', '10 mg', 'Once daily (HS)', '30 days'),
        ('Tab. Prednisolone', '20 mg', 'OD (tapering)', '5 days'),
        ('Fluticasone/Salmeterol MDI', '250/50 mcg', '1 puff BD', 'Long-term'),
        ('Salbutamol MDI (Rescue)', '100 mcg', '2 puffs PRN', 'As needed'),
        ('Tab. Cetirizine', '10 mg', 'Once daily', '14 days'),
    ]
    
    for med, dose, freq, dur in meds:
        pdf.set_font('Helvetica', '', 8)
        pdf.set_text_color(*ClinicalReportPDF.DARK_GRAY)
        pdf.cell(65, 5, med)
        pdf.cell(30, 5, dose)
        pdf.cell(35, 5, freq)
        pdf.cell(25, 5, dur, ln=True)
    
    # ─── DIAGNOSIS ───
    pdf.section_title('FINAL DIAGNOSIS (ICD-10 CODED)')
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(*ClinicalReportPDF.DARK_GRAY)
    
    diagnoses = [
        ('1.', 'Acute Exacerbation of Mild Persistent Bronchial Asthma', 'J45.31', 'Active'),
        ('2.', 'Essential (Primary) Hypertension, Stage 1 - Newly Diagnosed', 'I10', 'Active'),
        ('3.', 'Allergic Rhinitis, Perennial', 'J30.1', 'Active'),
    ]
    
    for num, name, icd, status in diagnoses:
        pdf.set_font('Helvetica', 'B', 9)
        pdf.cell(8, 5.5, num)
        pdf.set_font('Helvetica', '', 9)
        pdf.cell(95, 5.5, name)
        pdf.set_font('Helvetica', 'B', 8)
        pdf.set_text_color(*ClinicalReportPDF.ACCENT)
        pdf.cell(20, 5.5, icd)
        pdf.set_text_color(0, 140, 60)
        pdf.cell(0, 5.5, status, ln=True)
        pdf.set_text_color(*ClinicalReportPDF.DARK_GRAY)

    # ─── FOLLOW UP ───
    pdf.section_title('FOLLOW-UP & RECOMMENDATIONS')
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(*ClinicalReportPDF.DARK_GRAY)
    
    followups = [
        'Follow-up with Pulmonology OPD in 2 weeks (Dr. Meera Krishnan)',
        'BP monitoring at home twice daily. Maintain a log for review',
        'Follow-up with Internal Medicine in 4 weeks for BP reassessment',
        'Avoid known allergens (dust, pollen, strong perfumes)',
        'Carry Salbutamol rescue inhaler at all times',
        'Repeat spirometry in 6 weeks',
        'Diet: Low sodium (< 5g/day), adequate hydration',
        'If SpO2 drops below 92% or severe breathlessness - visit ER immediately'
    ]
    
    for f in followups:
        pdf.set_font('Helvetica', '', 8)
        pdf.set_text_color(*ClinicalReportPDF.ACCENT)
        pdf.cell(5, 4.5, '>')
        pdf.set_text_color(*ClinicalReportPDF.DARK_GRAY)
        pdf.cell(0, 4.5, f, ln=True)
    
    # ─── SIGNATURES ───
    pdf.ln(10)
    pdf.set_draw_color(*ClinicalReportPDF.BORDER_LINE)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)
    
    sig_y = pdf.get_y()
    
    pdf.set_x(15)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(*ClinicalReportPDF.DARK_GRAY)
    pdf.cell(60, 5, 'Dr. Meera Krishnan', ln=True)
    pdf.set_x(15)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(*ClinicalReportPDF.MED_GRAY)
    pdf.cell(60, 4, 'MD (Pulmonary Medicine)', ln=True)
    pdf.set_x(15)
    pdf.cell(60, 4, 'Consultant Pulmonologist', ln=True)
    pdf.set_x(15)
    pdf.cell(60, 4, 'KMC Reg: 78452-KA', ln=True)
    
    pdf.set_y(sig_y)
    pdf.set_x(130)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(*ClinicalReportPDF.DARK_GRAY)
    pdf.cell(60, 5, 'Dr. Arjun Patel', ln=True)
    pdf.set_x(130)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(*ClinicalReportPDF.MED_GRAY)
    pdf.cell(60, 4, 'MBBS, DNB (Internal Medicine)', ln=True)
    pdf.set_x(130)
    pdf.cell(60, 4, 'Resident, Internal Medicine', ln=True)
    pdf.set_x(130)
    pdf.cell(60, 4, 'KMC Reg: 94201-KA', ln=True)

    # ─── SAVE ───
    output_path = os.path.join(
        r'c:\Users\Ayush Shukla\Desktop\Agents Assemble',
        'Priya_Sharma_Clinical_Report.pdf'
    )
    pdf.output(output_path)
    print(f"Report generated: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_report()
