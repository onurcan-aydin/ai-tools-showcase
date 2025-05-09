import requests
import json
import os
from typing import List, Dict, Union

class FeedbackAnalyzer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

    def analyze_feedback(self, feedback: Union[str, List[str]]) -> Dict:
        """
        Analyze customer feedback using Claude API and return structured insights.
        
        Args:
            feedback: Either a single feedback string or a list of feedback strings
            
        Returns:
            Dictionary containing top themes and action items
        """
        if isinstance(feedback, str):
            feedback = [feedback]
            
        # Prepare the prompt for Claude
        prompt = f"""Please analyze the following customer feedback and provide:
1. Top 3 themes that emerge from the feedback
2. 3-5 specific action items that should be taken based on the feedback

Customer Feedback:
{json.dumps(feedback, indent=2)}

Please format your response as a JSON object with the following structure:
{{
    "themes": [
        {{
            "theme": "theme name",
            "description": "brief description",
            "frequency": "how often this theme appears"
        }}
    ],
    "action_items": [
        {{
            "action": "specific action to take",
            "priority": "high/medium/low",
            "rationale": "why this action is important"
        }}
    ]
}}"""

        # Make the API call to Claude
        payload = {
            "model": "claude-3-opus-20240229",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            # Parse Claude's response
            response_data = response.json()
            if "content" in response_data and len(response_data["content"]) > 0:
                # Extract the JSON string from the response text
                response_text = response_data["content"][0]["text"]
                # Find the start of the JSON object
                json_start = response_text.find("{")
                if json_start != -1:
                    json_str = response_text[json_start:]
                    analysis = json.loads(json_str)
                    return analysis
                else:
                    print("Error: Could not find JSON object in response")
                    return None
            else:
                print("Error: Unexpected API response structure")
                print("Response:", response_data)
                return None
            
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"Response text: {e.response.text}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON Parsing Error: {str(e)}")
            print(f"Response text: {response.text}")
            return None
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
            return None

def main():
    # Use the API key directly
    api_key = "API KEY"
    
    # Initialize the analyzer
    analyzer = FeedbackAnalyzer(api_key)

    # Example feedback
    example_feedback = [
        "The app is great but it crashes sometimes when I try to upload photos. This is really frustrating when I'm trying to share important moments with friends.",
        "I love the new dark mode feature! It's much easier on my eyes at night. However, I wish there was a way to schedule when it automatically turns on and off.",
        "The customer service team was very helpful when I had an issue with my account. They responded quickly and solved my problem. Keep up the good work!",
        "The app takes too long to load on my older phone. I've had to wait up to 30 seconds sometimes. Please optimize the performance for older devices.",
        "The new update made the interface more confusing. I can't find some features that I used to use regularly. Please make the navigation more intuitive."
    ]

    # Analyze the feedback
    results = analyzer.analyze_feedback(example_feedback)
    
    if results:
        print("\n=== Feedback Analysis Results ===\n")
        
        print("Top Themes:")
        for theme in results["themes"]:
            print(f"\n- {theme['theme']}")
            print(f"  Description: {theme['description']}")
            print(f"  Frequency: {theme['frequency']}")
        
        print("\nSuggested Action Items:")
        for action in results["action_items"]:
            print(f"\n- {action['action']}")
            print(f"  Priority: {action['priority']}")
            print(f"  Rationale: {action['rationale']}")

if __name__ == "__main__":
    main() 
