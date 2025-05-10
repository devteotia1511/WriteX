from flask import Flask, render_template, jsonify, request, send_file, url_for
import random
from fpdf import FPDF

app = Flask(__name__, static_url_path='/static')

app = Flask(__name__)
last_topic = None  # Store last generated topic to avoid repetition

def generate_auto_topic():
    """
    Dynamically generates unique, opinion-based topics for discussion.
    """
    keywords = [
        "Artificial Intelligence", "Remote Work", "Electric Vehicles", "Social Media", "Data Privacy",
        "Climate Change", "Cybersecurity", "Mental Health", "Education System", "Entrepreneurship",
        "Space Exploration", "Freelancing Culture", "Online Learning", "Blockchain", "Virtual Reality",
        "Internet Censorship", "Work-Life Balance", "5G Technology", "Digital Payments", "Gig Economy",
        "NFTs", "Electric Public Transport", "Youth Unemployment", "Career vs Passion", "Online Shopping",
        "Influencer Culture", "Job Automation", "Green Energy", "Recession Fears", "AI-generated Art",
        "Diversity in Tech", "Gaming Addiction", "Gender Equality at Work", "Skill-based Hiring",
        "Paper Degrees vs Practical Skills", "Moon Missions", "Remote Education", "Content Moderation",
        "Startup Ecosystem", "Short-form Content", "Coding in Schools", "ChatGPT and Productivity"
    ]

    question_formats = [
        "Do you think {k} is beneficial or harmful?",
        "What is your opinion on the rise of {k}?",
        "Is {k} changing the way we live and work?",
        "How does {k} impact our daily lives?",
        "Should governments regulate {k} more strictly?",
        "Can {k} solve modern-day problems effectively?",
        "Is society ready for the challenges posed by {k}?",
        "How important is {k} for the future of our country?",
        "Will {k} create more opportunities or more risks?",
        "Should {k} be promoted or restricted?",
        "Is {k} the need of the hour?",
        "Can India become a global leader in {k}?",
        "What challenges does {k} bring to our generation?",
        "Is {k} making humans smarter or lazier?",
        "Should students be educated about {k} early on?",
        "Is the impact of {k} more positive or negative?",
        "How should companies approach {k}?",
        "Will {k} reduce jobs or create new ones?",
        "Is the world overdependent on {k}?",
        "Should policies be updated to adapt to {k}?"
    ]

    max_retries = 10
    for _ in range(max_retries):
        keyword = random.choice(keywords)
        format_template = random.choice(question_formats)
        topic = format_template.format(k=keyword)
        if topic != last_topic:
            return topic
    return topic  # fallback even if repeated

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get-topic")
def get_topic():
    global last_topic
    topic = generate_auto_topic()
    last_topic = topic
    word_limit = random.randint(150, 400)
    return jsonify({"topic": f"{topic} Share your opinion on it.", "limit": word_limit})

@app.route("/download-pdf", methods=["POST"])
def download_pdf():
    content = request.form.get('content')  # Get the content written by the user
    
    # Create a PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    
    # Save the PDF in memory and send it as a response
    pdf_output = "/tmp/user_content.pdf"
    pdf.output(pdf_output)
    
    return send_file(pdf_output, as_attachment=True, download_name="writeX_content.pdf", mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True)