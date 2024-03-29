# Project "Comments"

## Running the Project

### Using Docker

1. **Clone the repository:**

    ```bash
    git clone https://github.com/kostomeister/py-spa-comments.git
    cd py-spa-comments
    ```

2. **Create a `.env` file:**

    Copy the `.env.sample` file to `.env` and fill it with your email details:

    ```ini
    SENDER_EMAIL=your_email@gmail.com
    SENDER_EMAIL_PASSWORD=your_password
    RECEIVER_EMAIL=recipient_email@gmail.com
    ```

    Please provide real data for your email.


3. **Choose the connection type:**
   ### In ```entrypoint.sh``` file
   - **For a regular Django server:**

      ```bash
      python manage.py runserver 0.0.0.0:8000
      ```

   - **For Daphne (with WebSockets):**

      ```bash
      daphne config.asgi:application
      ```

4. **Run the Docker container:**

    ```bash
    docker-compose up --build
    ```

5. **Interact with the application:**

   Now you can interact with the SPA application, add comments, and view them.

## API Endpoints

1. **Captcha API:**

    - Get a new CAPTCHA object:

        ```
        POST /api/captcha/
        ```

2. **Comments API:**

    - Get a list of comments:

        ```
        GET /api/comments/
        ```

    - Create a new comment:

        ```
        POST /api/comments/
        ```

## Additional Features

- When a user leaves a comment on another user's comment, the original user receives an email notification.
  
- Every day, an email is sent to the admin with the count of comments submitted on that day.

If you have any questions or issues, feel free to reach out.