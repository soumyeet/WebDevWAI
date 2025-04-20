

# Generate prompt
def generate_prompt_hiring(hiring_text):
    prompt = (
        "You are an expert job description evaluator. Given the following job description text, analyze it thoroughly, google the company's name and do a background search to get the answer to most of these:\n"
        "\n"
        "1. Score the following skill requirements on a scale of 1 to 100:\n"
        "    - Communication\n"
        "    - Technical Skills\n"
        "    - Creativity\n"
        "    - Leadership\n"
        "    - Problem Solving\n"
        "2. Determine the top strengths focused on based on these scores.\n"
        "3. Identify areas that are not required.\n"
        "4. Provide a 3-4 sentence summary of the job description.\n"
        "\n"
        f"JD:\n\"\"\"{hiring_text}\"\"\"\n"
        "\n"
        "Return your answer as a JSON object with these keys: skills, strengths, weaknesses, action_items, summary."
    )
    return textwrap.dedent(prompt)

# Resume analysis logic
def analyze_hiring_with_gemini(text):
    try:
        logger.info("Generating prompt for Gemini")
        prompt = generate_prompt_hiring(text)

        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content(prompt)

        # Clean up extra markdown formatting if present
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = re.sub(r"```json|```", "", response_text).strip()

        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            logger.warning("Gemini returned non-JSON output. Returning raw text as summary.")
            return {
                "skills": {},
                "strengths": [],
                "weaknesses": [],
                "summary": response_text
            }

    except Exception as e:
        logger.error(f"Error during Gemini analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")

# Endpoint
@app.post("/api/calculate-match")
async def calculate_match_endpoint(request: MatchRequest):
    logger.info("Received resume for analysis")
    result = analyze_hiring_with_gemini(hiring.text)
    return {
        "status": "success",
        "data": result
    }
