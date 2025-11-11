# Assignment 2  
This is a guide to help you run my assignment.  

## Getting Started 

### Step 1: Add your API keys
1. On my branch, go under Settings > Secrets and Variables > Codespaces > Click on "New repository secret"
Name: TAVILY_API_KEY 
Secret: [add your api key here]
and click on "Add secret"

2. Now, create another secret: 
Name: OPENAI_API_KEY
Secret: [add your api key here]
and click on "Add secret"

### Step 2: Open the assignment on codespace
1. Click the green Code button and switch to the Codespaces tab.
2. Select Create Codespace.
3. Wait a few minutes for the environment to finish setting up.

### Step 3: Install requirements
1. Run the following in terminal: pip install -r requirements.txt

### Step 4: Run my assignment
1. Then run this command on terminal: streamlit run assign_2.py
2. On the popup that appears, click “Open in Browser” to view my assignment. If you miss the popup:
a. Press Ctrl + C in the terminal to stop the app.
b. Rerun the command from step 1 — the popup should appear again.
3. A new browser tab will open, showing the interface of my assignment.