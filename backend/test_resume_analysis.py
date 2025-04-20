import requests
from resume_data import RESUME_TEXT

def test_resume_analysis():
    # API endpoint
    url = "http://localhost:8000/api/analyze-resume"
    
    # Prepare the request payload
    payload = {
        "text": RESUME_TEXT
    }
    
    try:
        # Send POST request
        response = requests.post(url, json=payload)
        
        # Check if request was successful
        if response.status_code == 200:
            print("Analysis successful!")
            print("\nResponse:")
            print(response.json())
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_resume_analysis()