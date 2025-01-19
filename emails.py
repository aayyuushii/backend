from flask import Blueprint, jsonify
import requests
import shared_data

# Your Hunter.io API key
API_KEY = "12d1263c5cb4a171f83bc03ffef0123fc6135224"

# Define the Blueprint for emails
emails_bp = Blueprint('emails', __name__)

def get_employees(domain):
    """
    Fetches a list of employees, their emails, and positions from a company's domain using Hunter.io Domain Search API.

    Parameters:
    - domain: The company's domain (e.g., "example.com").

    Returns:
    - A list of dictionaries containing employee name, email, and position.
    """
    url = "https://api.hunter.io/v2/domain-search"
    params = {
        "api_key": API_KEY,
        "domain": domain,
        "type": "personal"  # Restrict to personal (employee) email addresses
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get("data") and data["data"].get("emails"):
            employees = []
            for email_entry in data["data"]["emails"]:
                first_name = email_entry.get("first_name", "")
                last_name = email_entry.get("last_name", "")
                
                # Safely concatenate first and last name, handling None values
                employees.append({
                    "name": f"{first_name or ''} {last_name or ''}".strip(),  # Safely concatenate
                    "email": email_entry.get("value", ""),
                    "position": email_entry.get("position", ""),
                    "confidence_score": email_entry.get("confidence", 0)
                })
            return employees
        else:
            return {"error": "No employee data found for the provided domain."}
    else:
        return {"error": f"API call failed with status code {response.status_code}."}

# Define the Flask route to get employee details
@emails_bp.route('/get-employees', methods=['GET'])
def get_employees_data():
    company_url = shared_data.shared_input.get("company_url")
    if not company_url:
        return jsonify({"error": "No company URL provided"}), 400
    
    # Fetch employees from Hunter.io using the domain
    employee_list = get_employees(company_url)

    if isinstance(employee_list, list):
        return jsonify({"employees": employee_list})
    else:
        return jsonify({"error": employee_list.get("error")}), 400
