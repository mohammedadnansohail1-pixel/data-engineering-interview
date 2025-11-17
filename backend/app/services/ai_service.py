from anthropic import Anthropic
from app.core.config import settings
import json


class AIInterviewService:
    """Service for AI-powered interview coaching and code evaluation"""

    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def evaluate_code(
        self,
        code: str,
        question_title: str,
        question_description: str,
        test_results: dict
    ) -> dict:
        """Evaluate code submission and provide feedback"""

        prompt = f"""You are an expert technical interviewer for data engineering positions.

Question: {question_title}
Description: {question_description}

Candidate's Solution:
```
{code}
```

Test Results: {json.dumps(test_results, indent=2)}

Evaluate this solution on:
1. Correctness (does it solve the problem?)
2. Code quality (readability, style, best practices)
3. Efficiency (time/space complexity)
4. Data engineering best practices
5. Edge case handling

Provide your response in JSON format with the following structure:
{{
    "score": <0-100>,
    "strengths": ["point 1", "point 2"],
    "improvements": ["point 1", "point 2"],
    "optimization_suggestion": "specific suggestion",
    "would_pass_interview": true/false,
    "explanation": "brief explanation of pass/fail decision"
}}"""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            content = message.content[0].text

            # Try to parse JSON from response
            try:
                # Find JSON in the response
                json_start = content.find('{')
                json_end = content.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    feedback = json.loads(content[json_start:json_end])
                else:
                    # Fallback if no JSON found
                    feedback = {
                        "score": 70,
                        "strengths": ["Code is functional"],
                        "improvements": ["Could improve readability"],
                        "optimization_suggestion": "Consider edge cases",
                        "would_pass_interview": True,
                        "explanation": content
                    }
            except json.JSONDecodeError:
                # Fallback response
                feedback = {
                    "score": 70,
                    "strengths": ["Solution submitted"],
                    "improvements": ["Review feedback"],
                    "optimization_suggestion": "See detailed feedback",
                    "would_pass_interview": True,
                    "explanation": content
                }

            return feedback

        except Exception as e:
            return {
                "score": 0,
                "strengths": [],
                "improvements": ["Unable to evaluate code"],
                "optimization_suggestion": f"Error: {str(e)}",
                "would_pass_interview": False,
                "explanation": f"Evaluation error: {str(e)}"
            }

    async def generate_hint(
        self,
        question_title: str,
        question_description: str,
        user_code: str,
        hint_number: int
    ) -> str:
        """Generate progressive hints"""

        hint_level_descriptions = {
            1: "High-level approach/strategy without giving away the solution",
            2: "Specific technique or function to use",
            3: "Detailed step-by-step guidance"
        }

        prompt = f"""You are helping a candidate solve a data engineering interview question.

Question: {question_title}
{question_description}

Current code attempt:
```
{user_code if user_code else "No code written yet"}
```

Hint level: {hint_number}/3

Provide a progressive hint following this guideline:
{hint_level_descriptions.get(hint_number, "General guidance")}

Be encouraging but don't give away the complete solution. Keep the hint concise (2-3 sentences)."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=256,
                messages=[{"role": "user", "content": prompt}]
            )

            return message.content[0].text

        except Exception as e:
            return f"Unable to generate hint at this time: {str(e)}"

    async def suggest_improvements(self, code: str, feedback: dict) -> str:
        """Suggest specific code improvements"""

        prompt = f"""Based on this code and feedback, suggest 2-3 specific improvements:

Code:
```
{code}
```

Feedback: {json.dumps(feedback, indent=2)}

Provide concrete code suggestions."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}]
            )

            return message.content[0].text

        except Exception as e:
            return f"Unable to generate suggestions: {str(e)}"

    async def conduct_behavioral_interview(self, question: str, user_answer: str) -> dict:
        """Evaluate behavioral interview responses using STAR framework"""

        prompt = f"""You are conducting a behavioral interview for a data engineering role.

Question: {question}

Candidate's response:
{user_answer}

Evaluate using STAR framework:
- Situation: Was the context clear?
- Task: Did they explain their responsibility?
- Action: Were actions specific and detailed?
- Result: Were outcomes quantified?

Provide response in JSON format:
{{
    "score": <0-100>,
    "what_went_well": "feedback",
    "what_could_improve": "feedback",
    "follow_up_question": "a probing follow-up question"
}}"""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}]
            )

            content = message.content[0].text

            # Try to parse JSON
            try:
                json_start = content.find('{')
                json_end = content.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    return json.loads(content[json_start:json_end])
            except json.JSONDecodeError:
                pass

            return {
                "score": 70,
                "what_went_well": "Response provided",
                "what_could_improve": "Add more detail",
                "follow_up_question": "Can you elaborate further?"
            }

        except Exception as e:
            return {
                "score": 0,
                "what_went_well": "",
                "what_could_improve": f"Error: {str(e)}",
                "follow_up_question": ""
            }
