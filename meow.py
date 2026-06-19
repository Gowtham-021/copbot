import pandas as pd

# Define file paths
file_paths = {
    "police_faqs": "/home/bray/hari/data/police_faqs.csv",
    "law_sections": "/home/bray/hari/data/law_sections.xlsx",
    "emergency_contacts": "/home/bray/hari/data/emergency_contacts.xlsx",
    "crimes": "/home/bray/hari/data/crimes.xlsx",
    "case_types": "/home/bray/hari/data/case_types.xlsx",
    "fir_procedure": "/home/bray/hari/data/fir_procedure.txt",
    "bail_procedure": "/home/bray/hari/data/bail_procedure.txt",
    "investigation_steps": "/home/bray/hari/data/investigation_steps.txt"
}

# Create CSV: police_faqs.csv
df_faqs = pd.DataFrame({
    "Question": [
        "How can I file an FIR?",
        "What documents are needed to file an FIR?",
        "How do I track my FIR status?",
        "How to approach police for non-cognizable offenses?"
    ],
    "Answer": [
        "Visit the nearest police station with a written complaint. If the offense is cognizable, police must register the FIR under Section 154 CrPC.",
        "Identity proof (Aadhaar, Passport, PAN), any supporting evidence (photos, videos, documents), and a written complaint.",
        "Check online via the state police department’s website or visit the police station.",
        "Non-cognizable offenses require a complaint to be registered differently. Consult your local police station for details."
    ]
})
df_faqs.to_csv(file_paths["police_faqs"], index=False)

# Create Excel: law_sections.xlsx
df_law = pd.DataFrame({
    "Section": ["154 CrPC", "161 CrPC", "173 CrPC", "437 CrPC", "438 CrPC"],
    "Law Name": ["FIR Registration", "Police Powers to Examine", "Charge Sheet Filing", "Bail in Non-Cognizable Offenses", "Anticipatory Bail"],
    "Description": [
        "Mandates that police register an FIR for cognizable offenses upon receiving a complaint.",
        "Empowers police to record statements from victims, witnesses, and suspects during an inquiry.",
        "Requires police to submit a charge sheet after completing an investigation.",
        "Allows courts to grant bail in certain non-cognizable offenses.",
        "A person fearing arrest may apply for anticipatory bail."
    ]
})
df_law.to_excel(file_paths["law_sections"], index=False)

# Create Excel: emergency_contacts.xlsx
df_contacts = pd.DataFrame({
    "Service": ["National Emergency Number", "Police", "Fire Brigade", "Ambulance"],
    "Contact Number": ["112", "100", "101", "102"],
    "Availability": ["24/7", "24/7", "24/7", "24/7"],
    "Description": [
        "Single emergency number for police, fire, and ambulance.",
        "Local police emergency services.",
        "Immediate fire and rescue services.",
        "Medical emergency services."
    ]
})
df_contacts.to_excel(file_paths["emergency_contacts"], index=False)

# Create Excel: crimes.xlsx
df_crimes = pd.DataFrame({
    "Crime Type": ["Theft", "Murder", "Cyber Crime", "Assault", "Fraud"],
    "Description": [
        "Unauthorized taking of someone’s property with intent to deprive them permanently.",
        "Unlawful killing of another human with intent.",
        "Illegal activities carried out using computers or the internet.",
        "Physical attack or threat of violence against an individual.",
        "Wrongful or criminal deception intended to result in financial or personal gain."
    ]
})
df_crimes.to_excel(file_paths["crimes"], index=False)

# Create Excel: case_types.xlsx
df_cases = pd.DataFrame({
    "Case Type": ["Civil Case", "Criminal Case", "Family Case", "Labour Case"],
    "Description": [
        "Disputes between private parties such as contractual disagreements, property disputes, or tort claims.",
        "Cases involving alleged offenses against the state or public order, prosecuted under criminal law.",
        "Legal disputes concerning marriage, divorce, child custody, and related issues.",
        "Disputes between employers and employees regarding working conditions, wages, or dismissals."
    ]
})
df_cases.to_excel(file_paths["case_types"], index=False)

# Create TXT: fir_procedure.txt
fir_text = """Steps to File an FIR:

1. Visit the police station with jurisdiction over the incident area.
2. Approach the duty officer or Station House Officer (SHO) and clearly state your full name, address, and contact details.
3. Provide a detailed written complaint including the exact date, time, location, and description of the incident along with any available evidence.
4. Ensure that the FIR is registered under Section 154 CrPC for cognizable offenses, and obtain a free copy of the FIR.
5. If the police refuse to register your complaint, seek legal counsel or escalate to the Superintendent of Police.
"""
with open(file_paths["fir_procedure"], "w", encoding="utf-8") as f:
    f.write(fir_text)

# Create TXT: bail_procedure.txt
bail_text = """Steps to Apply for Bail:

1. Legal Consultation:
   - Consult a lawyer to assess the case and determine if bail is applicable.
2. Document Preparation:
   - Collect necessary documents such as identity proof, incident details, and previous court records.
3. Filing the Bail Application:
   - Submit a bail application in the appropriate court (Judicial Magistrate or Sessions Court).
4. Court Hearing:
   - The court reviews the application, considering factors such as the nature of the offense, flight risk, and possibility of tampering with evidence.
5. Conditions:
   - If granted, the court may impose conditions like surrendering travel documents or periodic reporting to the police.
6. Final Decision:
   - Obtain a copy of the bail order and comply with all court conditions.
"""
with open(file_paths["bail_procedure"], "w", encoding="utf-8") as f:
    f.write(bail_text)

# Create TXT: investigation_steps.txt
investigation_text = """Steps of Police Investigation:

1. Registration of Complaint:
   - The investigation begins with the registration of an FIR upon receiving a complaint.
2. Preliminary Inquiry:
   - Officers secure the crime scene and gather initial information.
3. Evidence Collection:
   - Forensic, digital, and physical evidence is collected, documented, and preserved.
4. Witness Examination:
   - Statements are recorded from the victim, witnesses, and involved parties (as per Section 161 CrPC).
5. Arrest and Interrogation:
   - Suspects are arrested and interrogated if sufficient evidence is found.
6. Charge Sheet Preparation:
   - A detailed charge sheet is prepared under Section 173 CrPC and submitted to the court.
7. Judicial Review and Trial:
   - The charge sheet is reviewed by a Magistrate, and the case proceeds to trial.
"""
with open(file_paths["investigation_steps"], "w", encoding="utf-8") as f:
    f.write(investigation_text)

# Provide file paths for download
file_paths
