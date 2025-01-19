from flask import Blueprint, request, jsonify
from langchain_huggingface import HuggingFaceEndpoint
from tavily import TavilyClient
import os

# Set up Flask Blueprint
pitch_bp = Blueprint('pitch', __name__)

# Set your Hugging Face API token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"  # Replace if necessary

# Initialize Tavily Client
client = TavilyClient(api_key="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")  # Replace if necessary

# Hugging Face model setup
llm = HuggingFaceEndpoint(repo_id="meta-llama/Llama-3.2-3B-Instruct", task="text-generation")

def generate_prompt(company_url):
    """
    Generate the Hugging Face model prompt to create a professional email pitch.
    """
    return (
        f'Information: """\n'
        f'Analyze from {company_url} and provide insights.\n'
        f'Target: Input company\n\n'
        f'Objective: Propose a solution to address the company’s recruitment challenges and improve their hiring processes.\n\n'
        f'Requirements:\n'
        f'1. Introduction:\n'
        f'   - Open with a polite and professional greeting.\n'
        f'   - Express appreciation for the company’s recent hiring efforts and acknowledge their industry contributions.\n\n'
        f'2. Highlight the recipient’s needs:\n'
        f'   - Recognize the company’s ongoing recruitment initiatives.\n'
        f'   - Demonstrate understanding of the challenges and opportunities in their industry.\n\n'
        f'3. Propose a solution:\n'
        f'   - Present the system as a solution to enhance their recruitment process.\n'
        f'   - Explain its ability to extract relevant information about companies and key contacts.\n'
        f'   - Highlight its capability to generate tailored sales pitches to engage potential clients more effectively.\n'
        f'   - Emphasize time-saving and efficiency benefits.\n\n'
        f'4. Maintain a professional tone:\n'
        f'   - Use polite, formal language with a persuasive and helpful tone.\n'
        f'   - Avoid overly technical jargon, ensuring clarity and professionalism.\n\n'
        f'5. Call to action:\n'
        f'   - Conclude with a clear and concise invitation to discuss the proposal further.\n'
        f'   - Offer to schedule a meeting or call at the recipient’s convenience, expressing flexibility in timing.\n'
        f'"""\n\n'
        f'Generate a professional email pitch based on the above details, ensuring all points are covered clearly and concisely. '
        f'Use polite and formal language, structured into sections with a professional tone. Format the email using markdown syntax for easy readability.'
    )

@pitch_bp.route('/generate-report', methods=['POST'])
def generate_report():
    """
    Generate a professional email pitch based on the company URL and other inputs.
    """
    # Get the company URL from the incoming request
    try:
        company_url = request.json.get("company_url")
        if not company_url:
            return jsonify({"error": "No company URL provided"}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to parse input JSON: {str(e)}"}), 400

    # Fetch content based on the company URL using Tavily client
    try:
        content = client.search(company_url, search_depth="advanced", topic="news", time_range="day")["results"]
    except Exception as e:
        return jsonify({"error": f"Failed to fetch content from Tavily: {str(e)}"}), 500

    # Prepare the Hugging Face prompt
    prompt = generate_prompt(company_url)

    # Run Hugging Face model to generate the report
    try:
        report = llm.invoke(prompt)  # Get the response directly
        if not report:
            return jsonify({"error": "Failed to generate pitch using Hugging Face."}), 500
    except Exception as e:
        return jsonify({"error": f"Failed to generate report using Hugging Face: {str(e)}"}), 500

    # Return the generated report
    return jsonify({"report": report})
