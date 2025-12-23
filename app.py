import gradio as gr
from transformers import pipeline

# Load a public model for general text classification (no auth required)
classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

def detect_phishing(email_text):
    try:
        result = classifier(email_text[:512])[0]
        label = result["label"]
        score = result["score"]

        # Simple logic to flag phishing-like emails
        phishing_keywords = ["account", "bank", "verify", "password", "login", "update", "click", "urgent", "confirm"]
        email_lower = email_text.lower()

        if any(word in email_lower for word in phishing_keywords) or score < 0.6:
            return f"⚠️ Phishing Detected (Confidence: {score:.2f}) — Reason: Suspicious keywords found"
        else:
            return f"✅ Safe Email (Confidence: {score:.2f})"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Gradio Interface
demo = gr.Interface(
    fn=detect_phishing,
    inputs=gr.Textbox(lines=10, label="Paste Email Content Here"),
    outputs=gr.Textbox(label="Prediction Result"),
    title="🧠 AI-Powered Phishing Email Detector",
    description="Detects phishing emails based on text classification and keyword intelligence."
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
