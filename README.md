# File Converter Telegram Bot

A Telegram bot that allows users to convert files between different formats (PDF to Word, Word to PDF, Image to PDF).

## Setup

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Install LibreOffice (required for Word to PDF conversion on Linux):
    ```bash
    sudo apt update
    sudo apt install libreoffice
    ```
4.  Create a `.env` file from `.env.example` and add your Telegram Bot Token.
5.  Run the bot:
    ```bash
    python bot.py
    ```

## Features

- **PDF to Word**: Converts PDF documents to editable DOCX files.
- **Word to PDF**: Converts DOCX files to PDF documents.
- **Image to PDF**: Converts JPG/PNG images to PDF documents.
- **Automatic Cleanup**: Temporary files are deleted after conversion.
