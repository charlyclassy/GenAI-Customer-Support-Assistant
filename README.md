# SupportSense AI — GenAI in Business

An interactive responsible-AI evaluation exercise for a simulated customer-support drafting assistant. It includes **five fictional enquiries**, a reusable prompt, prepared sample draft replies, and human-led scoring for accuracy, bias/fairness, privacy, transparency, and human escalation.

> This is **not** a live generative AI model. No API key is needed; replies are written examples and no messages are sent.

## Run locally in VS Code (Python 3.12)

Open the project folder in VS Code, select **Terminal → New Terminal**, and enter:

```powershell
python -m pip install -r requirements.txt
python customer_support_exercise.py
python -m streamlit run app.py
```

The third command opens the Streamlit dashboard in your browser, usually at `http://localhost:8501`.

If you already ran the exercise and have both CSV files inside `outputs/`, you can skip the second command.

## How to use the dashboard

1. **Overview:** Read the five fictional enquiries.
2. **Review customer drafts:** Select a case, inspect its context and example reply, score each of the five criteria from 0 (not met) to 2 (fully met), and add reviewer notes.
3. **Scoring dashboard:** Review totals (maximum 10 per case, 50 overall) and download the checklist and summary as CSV files.
4. **Prompt & governance:** Review the reusable prompt and human-control rules.

**Important:** Evaluations are stored only within the Streamlit browser session. **Download your scored CSV before closing/restarting the app.** Empty scores are preserved as blanks rather than treated as zero.

## Repository structure

```text
GenAI_Customer_Support_Exercise/
├── app.py
├── customer_support_exercise.py
├── prompt_template.md
├── requirements.txt
├── README.md
└── outputs/
    ├── customer_support_cases_and_drafts.csv
    └── human_scoring_checklist.csv
```

## Deploy via Streamlit Community Cloud

1. Upload all project files, including the two CSV files in `outputs/`, to a new GitHub repository.
2. In Streamlit Community Cloud, choose **Create app**, select your repository, and set **Main file path** to `app.py`.
3. Choose Python 3.12 if prompted. Deploy.

The deployment will automatically install packages from `requirements.txt`.

## Safety and limitations

The cases are entirely fictional; no real customer data, authentication, refund, account access, or messaging service is involved. Any future use of AI-generated replies with real customers requires approved privacy protections, verified company policies, human escalation paths, and appropriate human review.
