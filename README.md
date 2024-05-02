# Let Me Interview.ai

This is an AI interview system that supports two user types: HR and candidates. Organizations can conduct interviews with candidates based on the provided descriptions and required experience without any human interference. It sends invites to candidates through emails, sends reminders for them to appear for the test, administers the test, and evaluates a set of suitable candidates from all the interviews conducted.

## Main Features

* Register as HR and set up an interview.
* Send invites to one/many candidates for an interview.
* Send reminders to candidates who didn't appear for the interview.
* Take interviews as candidates.
* No human interference, no bias.
* Get evaluation of a particular test or a candidate.

## Setting Up the Project Locally

Follow the steps to set up the project locally on your machine!

1. First clone the repository from GitHub:
    ```
    git clone git@github.com:anuragshuklajec/lmi.ai.git
    ```

2. Create and activate a virtual environment:

   On Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   On macOS/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies from requirements.txt:

    ```
    pip install -r requirements.txt
    ```

4. Set up environment variables:

    There is a file called `.env.example`. Rename this to `.env` and add your OpenAI API key and Email app password inside the placeholders given in this file.

5. Apply the migrations:

    ```
    python manage.py migrate
    ```

6. Run the development server:

    ```
    python manage.py runserver
    ```
7. Load the `lmi_app.postman_collection.json` file in postman or your preferred API testing tool and various routes
