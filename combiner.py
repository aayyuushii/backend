from flask import Blueprint, jsonify
from langchain_huggingface import HuggingFaceEndpoint
import os
import shared_data

# Set your Hugging Face API token if needed
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"  # Replace if necessary

combiner_bp = Blueprint('combiner', __name__)

@combiner_bp.route('/combine', methods=['GET'])
def get_combined_data():
    company_url = shared_data.shared_input.get("company_url")
    if not company_url:
        return jsonify({"error": "No company URL provided"}), 400

    services_app = ['AI Integration', 'Designing', 'Enterprise solutions', 'App Development']

    # Set up Hugging Face prompt using the company URL
    prompt = (
        f'Compare the services of {services_app} and give results that provide facts of how apptware company can help.\n'
        f'Information: """\n'
        f'1. Company-specific software -> Domains/Projects\n'
        f'2. Input company -> Domains/Projects\n'
        f'3. Compare keywords from both fields and generate a detailed summarized analysis.\n'
        f'4. Upon comparison, generate the following insights:\n'
        f'   - Key features of the software and its alignment with the domains/projects.\n'
        f'   - Facts that highlight unique strengths, overlaps, or gaps between the software and domains/projects.\n'
        f'   - Actionable suggestions to enhance the alignment or address challenges identified during the analysis.\n'
        f'   - Insights derived from the comparison to uncover potential opportunities.\n'
        f'   - Solutions or recommendations that can improve or optimize the company’s offerings.\n'
        f'5. Ensure all points are concisely and professionally written in grammatically correct language.\n'
        f'6. The final output must be formatted in a way that can be easily converted into a polished pitch for an email.\n'
        f'7. Use MLA format and markdown syntax for clarity and readability.\n'
        f'"""\n\n'
        f'Analyze the provided data, compare keywords effectively, and ensure the output includes the following elements:\n'
        f'- Clear, structured insights organized with bullet points.\n'
        f'- A professional tone suitable for business communication.\n'
        f'- High-level summaries that maintain focus on actionable takeaways.\n\n'
        f'Please ensure that all suggestions, facts, and solutions are user-friendly and adaptable for crafting an email pitch.'
    )

    # Running Hugging Face model for text generation
    llm = HuggingFaceEndpoint(repo_id="meta-llama/Llama-3.2-3B-Instruct", task="text-generation")
    report = llm.invoke(prompt)  # Get the response directly
    
    # Return the result as a JSON response
    return jsonify({"combined_report": report})
