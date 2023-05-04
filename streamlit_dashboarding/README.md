# README

## Streamlit Web App with OpenAI and Hugging Face Integration

This web app demonstrates various Streamlit components and features, and it also integrates OpenAI's GPT-3.5-turbo model and a Hugging Face pre-trained object detection model.

### Requirements

- Python 3.6 or higher
- Streamlit
- Pandas
- Plotly
- OpenAI
- Pillow
- Requests

### Setting up API keys

Before running the app, you might need to set up the API keys for OpenAI and Hugging Face.

1. Create an account or sign in to OpenAI (https://beta.openai.com/signup/) and obtain your API key from the API key section.
2. Create an account or sign in to Hugging Face (https://huggingface.co/join) and obtain your API key from the API key section.

To set up the API keys, you can either:

- Set the API keys as environment variables in your terminal or command prompt:

export OPENAI_AUTH=<your_openai_api_key>
export HF_AUTH=<your_huggingface_api_key>

- Or, replace the following lines in the code with your API keys:

os.environ["OPENAI_API_KEY"] = os.environ["OPENAI_AUTH"]
headers = {"Authorization": f"Bearer {os.environ['HF_AUTH']}"}

Replace with:

os.environ["OPENAI_API_KEY"] = "<your_openai_api_key>"
headers = {"Authorization": f"Bearer <your_huggingface_api_key>"}

You can start up the app in you VM with

```bash
docker compose up --build


