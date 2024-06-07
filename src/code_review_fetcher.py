from openai import OpenAI, OpenAIError


class GithubCodeReviewer:
    """
    Class responsible for reviewing code using OpenAI.
    """

    def __init__(self, api_key):
        """
        Initialize CodeReviewer with OpenAI API key.
        """
        self.client = OpenAI(api_key=api_key)

    def review_code(self, diffs):
        """
        Review the provided code diffs.
        """
        prompt = f"Review the following code changes:\n{diffs}"
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """
                      You are a senior software developer responsible for conducting code reviews in the Engineering department of a technology/software company.
                      
                      Your task is to receive a code submission in a **git diff format** and generate a comprehensive report summarizing your findings. Include information such as: 

                      - Identified issues
                      - Recommendations for improvement
                      - Areas of strength
                      - Overall code quality assessmentThe
                      - Potential security vulnerabilities

                      The report should be well-structured, easy to understand, and provide actionable feedback to the developer. Remember to stick to the given code, and avoid making assumptions or providing feedback on code that is not included in the submission.
                      """,
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1200,
                temperature=0.3,
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            print(f"Error occurred while reviewing code: {e}")
            return None
