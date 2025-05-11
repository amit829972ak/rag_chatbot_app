def query_model(prompt, model_choice, api_key):
    if model_choice == "OpenAI GPT":
        import openai
        openai.api_key = api_key
        res = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Answer the question from the context."},
                      {"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content.strip()

    elif model_choice == "Google Gemini":
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro")
        return model.generate_content(prompt).text

    elif model_choice == "Claude":
        import requests
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        body = {
            "model": "claude-3-opus-20240229",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}]
        }
        res = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=body)
        return res.json()['content'][0]['text']
