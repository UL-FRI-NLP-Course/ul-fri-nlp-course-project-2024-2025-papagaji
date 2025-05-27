from huggingface_hub import snapshot_download, login

snapshot_download(
    repo_id="cjvt/GaMS-9B",
    cache_dir="./gams_9b_cache",  # Optional: custom cache path
    local_dir="./gams_9b_local",  # Download a full local copy if you prefer
    local_dir_use_symlinks=False  # Copy files instead of symlinks (useful for portability)
)

# snapshot_download(
#     repo_id="mistralai/Mistral-7B-Instruct-v0.2",
#     cache_dir="./mistral_cache",       # Optional
#     local_dir="./mistral_7b_local",    # Your local path to use later
#     local_dir_use_symlinks=False,
#     allow_patterns=["*.safetensors", "*.json", "*.py", "*.txt", "*.model", "*.gitattributes", "*.md"]
# )