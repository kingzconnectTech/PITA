import ollama
import sys

try:
    print("Checking Ollama models...", flush=True)
    models = ollama.list()
    print("Available models:", flush=True)
    for model in models.get('models', []):
        print(f"- {model['name']}", flush=True)
    if not models.get('models'):
        print("No models found.", flush=True)
except Exception as e:
    print(f"Error connecting to Ollama: {e}", flush=True)
    import traceback
    traceback.print_exc()
