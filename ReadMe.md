# Gemini Pro AI

Gemini Pro AI is a Streamlit-based application that utilizes the Gemini Pro and Gemini Pro Vision models from the Google Generative AI API to provide text and image-based conversational responses.

## Overview

Gemini Pro AI allows users to engage in a chat with the Gemini Pro AI models, enabling conversations with both text and image inputs. The application utilizes Streamlit for the user interface and Google Generative AI API for generating responses.

## Getting Started

To run the application, make sure you have the required dependencies installed. You can install them using the following command:

```bash
    pip install streamlit pillow python-dotenv google-generativeai
```

Additionally, you need to set up your Gemini API key. You can either set it as an environment variable named `GENAI_API_KEY` or enter it when prompted.

```bash
    export GENAI_API_KEY=your_api_key
```

## Usage

Run the application using the following command:

```bash
    streamlit run your_app_file.py
```

Once the application is running, you can interact with Gemini Pro AI:

1. Enter text in the input box.
2. Optionally, upload an image using the file uploader.
3. Click the "Send" button to initiate the conversation.

Gemini Pro AI will process your input and generate responses based on the configured models. Conversations will be displayed in the chat container.

## Configuration

Gemini Pro AI is configured with the following settings:

- **Text Chat Model:**
  - Model Name: gemini-pro
  - Generation Configuration:
    - Temperature: 0.9
    - Top-p: 1
    - Top-k: 32
    - Max Output Tokens: 8192
  - Safety Settings:
    - HARM_CATEGORY_HARASSMENT: BLOCK_MEDIUM_AND_ABOVE
    - HARM_CATEGORY_HATE_SPEECH: BLOCK_MEDIUM_AND_ABOVE
    - HARM_CATEGORY_SEXUALLY_EXPLICIT: BLOCK_MEDIUM_AND_ABOVE
    - HARM_CATEGORY_DANGEROUS_CONTENT: BLOCK_MEDIUM_AND_ABOVE

- **Image Chat Model:**
  - Model Name: gemini-pro-vision
  - Generation Configuration: (Same as Text Chat Model)
  - Safety Settings: (Same as Text Chat Model)

## Example

```python
    python your_app_file.py
```

Visit [http://localhost:8501](http://localhost:8501) in your web browser to interact with Gemini Pro AI.

## Contributions

Contributions are welcome! Feel free to open issues or pull requests to enhance the functionality or fix any issues.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.