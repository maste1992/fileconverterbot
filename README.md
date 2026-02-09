# File Converter Telegram Bot

A powerful Telegram bot that converts files between various formats. Now with OCR support!

## Features

- **PDF <-> Word**: Converts PDF to editable DOCX and vice versa.
- **Excel <-> PDF/Word**: Converts Excel spreadsheets to PDF or Word documents.
- **Image Conversion**:
  - Image to PDF
  - **OCR Support**: Extracts text from images and saves to Word or Excel.
- **Automatic Cleanup**: Temporary files are deleted after processing for privacy.

## Local Setup

1.  **Clone the repository.**
2.  **Install System Dependencies:**
    You need `libreoffice` for document conversion and `tesseract-ocr` for image text extraction.
    ```bash
    sudo apt update
    sudo apt install libreoffice tesseract-ocr poppler-utils -y
    ```
3.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configuration:**
    - Get your Bot Token from @BotFather on Telegram.
    - Create a `.env` file from `.env.example`:
      ```
      TELEGRAM_BOT_TOKEN=your_token_here
      ```
5.  **Run the bot:**
    ```bash
    ./run
    ```

## Deployment

Since this bot requires heavy system dependencies (LibreOffice, Tesseract), it cannot be deployed on standard serverless platforms like Vercel. Instead, used a Docker-based platform.

### Deploy on Railway (Recommended)

1.  Push this code to GitHub.
2.  Go to [Railway.app](https://railway.app/) and create a new project.
3.  Select "Deploy from GitHub repo" and choose this repository.
4.  Railway will automatically detect the `Dockerfile` and build it.
5.  Go to the "Variables" tab in Railway and add `TELEGRAM_BOT_TOKEN` with your bot token.
6.  Your bot will be live 24/7! 🚀

### Deploy on Render

1.  Push code to GitHub.
2.  Create a new **Web Service** on [Render.com](https://render.com/).
3.  Connect your repository.
4.  Select "Docker" as the Environment.
5.  Add your `TELEGRAM_BOT_TOKEN` in the Environment Variables section.
