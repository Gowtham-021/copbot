from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import os
import re
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Configuration
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

BOT_NAME = "TN Police Cop Bot"
USERS = {"admin": "password123"}  # Simple user database

# LLM backend configuration: default to Ollama (local Ollama server)
MODEL_BACKEND = os.environ.get("MODEL_BACKEND", "ollama").lower()
# MODEL_PATH for Ollama should be the Ollama model name (e.g. 'mistral')
MODEL_SPEC = os.environ.get("MODEL_PATH")


def call_ollama(model, prompt, max_tokens=256):
    """Call local Ollama HTTP API and return text result or error string."""
    try:
        import requests
    except Exception:
        return "Server error: 'requests' package not installed."

    url = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
    payload = {"model": model, "prompt": prompt, "max_tokens": max_tokens}
    try:
        r = requests.post(url, json=payload, timeout=15)
        try:
            data = r.json()
        except Exception:
            return f"Ollama returned non-JSON response: {r.text}"

        # Common response shapes: {'text': '...'} or {'choices':[{'text':...}]}
        if isinstance(data, dict):
            if "text" in data and data["text"]:
                return data["text"]
            if "choices" in data and isinstance(data["choices"], list) and data["choices"]:
                choice = data["choices"][0]
                return choice.get("text") or choice.get("message") or str(choice)
        return str(data)
    except Exception as e:
        return f"Ollama request failed: {e}"

# FIR Procedure Data
FIR_PROCEDURES = {
    'en': {
        'title': "FIR Procedure (English)",
        'steps': [
            "Visit the nearest police station under whose jurisdiction the crime occurred",
            "Provide complete details of the incident (date, time, location, people involved)",
            "Submit a written complaint or give verbal statement which will be recorded",
            "Police will register the FIR and provide you a free copy",
            "Get the investigating officer's contact details for follow-up"
        ],
        'note': "Note: FIR registration is your legal right under Section 154 of CrPC."
    },
    'ta': {
        'title': "FIR செயல்முறை (தமிழ்)",
        'steps': [
            "குற்றம் நடந்த இடத்தின் அதிகார வரம்புக்குட்பட்ட காவல் நிலையத்திற்குச் செல்லவும்",
            "சம்பவத்தின் முழு விவரங்களை வழங்கவும் (தேதி, நேரம், இடம், சம்பந்தப்பட்ட நபர்கள்)",
            "எழுத்துப்பூர்வ புகாரை சமர்ப்பிக்கவும் அல்லது பதிவு செய்யப்படும் வாய்மொழி அறிக்கையை வழங்கவும்",
            "காவல் துறை FIR ஐ பதிவு செய்து உங்களுக்கு இலவச நகலை வழங்கும்",
            "பின்தொடர்வுக்காக விசாரணை அதிகாரியின் தொடர்பு விவரங்களைப் பெறவும்"
        ],
        'note': "குறிப்பு: CrPC இன் பிரிவு 154 இன் கீழ் FIR பதிவு செய்வது உங்கள் சட்டப்பூர்வ உரிமை."
    }
}

# Emergency Contacts Data
EMERGENCY_CONTACTS = {
    'ta': [
        {"priority": 1, "icon": "👮", "name": "பொது அவசர எண்", "number": "100", "description": "காவல் உதவிக்கு"},
        {"priority": 2, "icon": "🚑", "name": "மருத்துவ அவசர எண்", "number": "108", "description": "ஆம்புலன்ஸ் சேவைகள்"},
        {"priority": 3, "icon": "🚒", "name": "தீயணைப்பு பணியகம்", "number": "101", "description": "தீயணைப்பு வண்டி"},
        {"priority": 4, "icon": "👩", "name": "மகளிர் உதவி எண்", "number": "1091", "description": "பெண்கள் பாதுகாப்பு"},
        {"priority": 5, "icon": "🧒", "name": "குழந்தை உதவி எண்", "number": "1098", "description": "குழந்தைகள் பாதுகாப்பு"}
    ],
    'en': [
        {"priority": 1, "icon": "👮", "name": "Police Emergency", "number": "100", "description": "For police assistance"},
        {"priority": 2, "icon": "🚑", "name": "Medical Emergency", "number": "108", "description": "Ambulance services"},
        {"priority": 3, "icon": "🚒", "name": "Fire Department", "number": "101", "description": "Fire brigade"},
        {"priority": 4, "icon": "👩", "name": "Women's Helpline", "number": "1091", "description": "Women's safety"},
        {"priority": 5, "icon": "🧒", "name": "Child Helpline", "number": "1098", "description": "Child protection"}
    ]
}

# Crime Types Data
CRIME_TYPES = {
    'en': {
        'title': "Types of Crimes",
        'categories': [
            {
                'name': "Violent Crimes",
                'examples': ["Murder", "Assault", "Rape", "Robbery", "Kidnapping"]
            },
            {
                'name': "Property Crimes", 
                'examples': ["Theft", "Burglary", "Arson", "Vandalism", "Fraud"]
            },
            {
                'name': "White-Collar Crimes",
                'examples': ["Embezzlement", "Money Laundering", "Cybercrime", "Tax Evasion"]
            },
            {
                'name': "Drug-Related Crimes",
                'examples': ["Drug Possession", "Drug Trafficking", "Manufacturing of Drugs"]
            },
            {
                'name': "Public Order Crimes",
                'examples': ["Rioting", "Disorderly Conduct", "Public Intoxication"]
            }
        ],
        'note': "Note: This is not an exhaustive list. Contact police for specific cases."
    },
    'ta': {
        'title': "குற்றங்களின் வகைகள்",
        'categories': [
            {
                'name': "வன்முறை குற்றங்கள்",
                'examples': ["கொலை", "தாக்குதல்", "கற்பழிப்பு", "கொள்ளையடித்தல்", "கடத்தல்"]
            },
            {
                'name': "சொத்து குற்றங்கள்",
                'examples': ["திருட்டு", "கொள்ளையடித்தல்", "தீ வைத்தல்", "சேதப்படுத்துதல்", "மோசடி"]
            },
            {
                'name': "வெள்ளைக்காலர் குற்றங்கள்",
                'examples': ["உள்நாட்டு கையாடல்", "பணம் கறைபடிந்தது", "இணைய குற்றம்", "வரி தவிர்ப்பு"]
            },
            {
                'name': "மருந்து தொடர்பான குற்றங்கள்",
                'examples': ["மருந்து உடைமை", "மருந்து கடத்தல்", "மருந்து உற்பத்தி"]
            },
            {
                'name': "பொது ஒழுங்கு குற்றங்கள்",
                'examples': ["கலகம்", "குழப்பமான நடத்தை", "பொது போதை"]
            }
        ],
        'note': "குறிப்பு: இது ஒரு முழுமையான பட்டியல் அல்ல. குறிப்பிட்ட வழக்குகளுக்கு காவல்துறையை அணுகவும்."
    }
}

# Bail Procedure Data
BAIL_PROCEDURE = {
    'en': {
        'title': 'Bail Procedure (English)',
        'steps': [
            'Apply for bail through a magistrate or court with the help of your lawyer.',
            'Produce necessary documents: identity proof, address proof, bail bond if required.',
            'Surety may be required; a surety provides assurance to the court.',
            'Court may impose conditions; comply with any orders and attend hearings.',
            'If bail is rejected at lower court, file an appeal to a higher court through legal counsel.'
        ],
        'note': 'This is a summary. Consult a lawyer for jurisdiction-specific advice.'
    },
    'ta': {
        'title': 'Bail செயல்முறை (தமிழ்)',
        'steps': [
            'உங்கள் வழக்கறிஞரின் உதவியுடன் மகிஸ்ட்ரேட் அல்லது நீதிமன்றத்தில் ஜாமீன் கோரிக்கை செய்யவும்.',
            'தேவையான ஆவணங்களை முன்வைக்கவும்: அடையாள சான்று, முகவரி சான்று, தேவையெனில் ஜாமீன் பத்திரம்.',
            'உறுதி (surety) தேவைப்படலாம்; இது நீதிமன்றத்திற்கு உத்தரவாதம் வழங்குகிறது.',
            'நீதிமன்றம் விதிகளையும் நிபந்தனைகளையும் அமல்படுத்தலாம்; அதனை பின்பற்றவும் மற்றும் விவாதங்களில் வரவும்.',
            'கீழ்நீதிமன்றத்தில் ஜாமீன் நிராகரிக்கப்பட்டால், மேல்நீதிமன்றத்தில் வழக்கினை மறு விசாரணை செய்யவும்.'
        ],
        'note': 'இது ஒரு சுருக்கம். பகுதி-சார்ந்த ஆலோசனைகளுக்கு வழக்கறிஞரைக் consulte செய்க.'
    }
}


def generate_bail_response(language):
    """Generate bail procedure response"""
    bail_data = BAIL_PROCEDURE.get(language, BAIL_PROCEDURE['en'])
    response = f"""
    <div class="bail-procedure">
        <h4><i class="fas fa-gavel"></i> {bail_data['title']}</h4>
        <div class="procedure-steps">
            <ol>
    """
    for step in bail_data['steps']:
        response += f"<li>{step}</li>"
    response += f"""
            </ol>
        </div>
        <div class="procedure-note">
            <i class="fas fa-info-circle"></i> {bail_data['note']}
        </div>
    </div>
    """
    return response

def detect_query_language(text):
    """Enhanced language detection with explicit language requests"""
    try:
        text = text.lower().strip()
        if any(word in text for word in ["tamil", "தமிழில்", "ta", "tamil version"]):
            return 'ta'
        if any(word in text for word in ["english", "ஆங்கிலத்தில்", "en", "english version"]):
            return 'en'
        if re.search(r'[\u0B80-\u0BFF]', text):
            return 'ta'
        return 'en'
    except:
        return 'en'

def generate_fir_response(language):
    """Generate FIR procedure response"""
    fir_data = FIR_PROCEDURES.get(language, FIR_PROCEDURES['en'])
    response = f"""
    <div class="fir-procedure">
        <h4><i class="fas fa-file-alt"></i> {fir_data['title']}</h4>
        <div class="procedure-steps">
            <ol>
    """
    for step in fir_data['steps']:
        response += f"<li>{step}</li>"
    response += f"""
            </ol>
        </div>
        <div class="procedure-note">
            <i class="fas fa-info-circle"></i> {fir_data['note']}
        </div>
    </div>
    """
    return response

def generate_emergency_response(language):
    """Generate emergency contacts response"""
    contacts = EMERGENCY_CONTACTS.get(language, EMERGENCY_CONTACTS['en'])
    response = f"""
    <div class="emergency-contacts">
        <h4><i class="fas fa-phone-alt"></i> {'அவசரத் தொடர்புகள்' if language == 'ta' else 'Emergency Contacts'}</h4>
        <div class="alert alert-danger">🚨 {'அவசர சூழ்நிலைகளில் மட்டும்' if language == 'ta' else 'For real emergencies only'}</div>
        <div class="contact-list">
    """
    for contact in sorted(contacts, key=lambda x: x['priority']):
        response += f"""
        <div class="contact-item">
            <span class="contact-icon">{contact['icon']}</span>
            <div class="contact-info">
                <strong>{contact['name']}</strong>
                <a href="tel:{contact['number']}" class="contact-number">{contact['number']}</a>
                <p class="contact-desc">{contact['description']}</p>
            </div>
        </div>
        """
    response += f"""
        </div>
        <div class="contact-footer">
            <i class="fas fa-exclamation-circle"></i> {'அவசர சூழ்நிலைகளில் மட்டும் அழைக்கவும்' if language == 'ta' else 'Call only in real emergencies'}
        </div>
    </div>
    """
    return response

def generate_crime_types_response(language):
    """Generate crime types response"""
    crime_data = CRIME_TYPES.get(language, CRIME_TYPES['en'])
    response = f"""
    <div class="crime-types">
        <h4><i class="fas fa-gavel"></i> {crime_data['title']}</h4>
        <div class="crime-categories">
    """
    for category in crime_data['categories']:
        response += f"""
        <div class="crime-category">
            <h5>{category['name']}</h5>
            <ul>
        """
        for example in category['examples']:
            response += f"<li>{example}</li>"
        response += """
            </ul>
        </div>
        """
    response += f"""
        </div>
        <div class="crime-note">
            <i class="fas fa-info-circle"></i> {crime_data['note']}
        </div>
    </div>
    """
    return response

@app.route('/static/<path:filename>')
def serve_static(filename):
    # Removed: rely on Flask's built-in static file handling
    return redirect(url_for('static', filename=filename))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if username in USERS and USERS[username] == password:
            session["user"] = username
            return redirect(url_for("chat"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if "user" not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        # Handle file upload logic here
        pass
    
    return render_template("upload.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "user" not in session:
        return redirect(url_for("login"))
    
    if "chat_history" not in session:
        session["chat_history"] = []
        
    if request.method == "POST":
        user_query = request.form.get("query", "").strip()
        if user_query:
            language = detect_query_language(user_query)
            query_lower = user_query.lower()
            
            if any(keyword in query_lower for keyword in ['emergency', 'அவசர', 'helpline', 'உதவி எண்']):
                response = generate_emergency_response(language)
            elif any(keyword in query_lower for keyword in ['fir', 'first information report', 'முதல் தகவல் அறிக்கை']):
                response = generate_fir_response(language)
            elif any(keyword in query_lower for keyword in ['crime', 'offense', 'குற்றம்', 'வழக்கு', 'types of crime', 'குற்ற வகைகள்']):
                response = generate_crime_types_response(language)
            elif any(keyword in query_lower for keyword in ['bail', 'ஜாமீன்', 'bail procedure', 'how to get bail', 'how to obtain bail']):
                response = generate_bail_response(language)
            else:
                # For general queries, prefer the configured LLM backend (Ollama by default)
                if MODEL_BACKEND == 'ollama' and MODEL_SPEC:
                    llm_text = call_ollama(MODEL_SPEC, user_query, max_tokens=256)
                    # If Ollama returned an error string, fall back to static help text
                    if llm_text.startswith('Ollama request failed:') or llm_text.startswith("Server error:"):
                        response = "I can help with FIR procedures, crime types, and emergency contacts. Please specify what you need help with."
                    else:
                        # Wrap LLM text for HTML rendering
                        response = f"<div class='llm-response'>{llm_text}</div>"
                else:
                    response = "I can help with FIR procedures, crime types, and emergency contacts. Please specify what you need help with."
            
            formatted_response = {
                'query': user_query,
                'response': response,
                'language': language,
                'timestamp': datetime.now().strftime("%H:%M"),
                'bot_name': BOT_NAME
            }
            
            session["chat_history"].append(formatted_response)
            session.modified = True
    
    return render_template("chat.html", chat_history=session.get("chat_history", []))

@app.route("/clear_chat", methods=["POST"])
def clear_chat():
    if "user" not in session:
        return redirect(url_for("login"))
    session["chat_history"] = []
    return redirect(url_for("chat"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)