from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="cjvt/GaMS-9B",
    cache_dir="./gams_9b_cache",  
    local_dir="./gams_9b_local",  
    local_dir_use_symlinks=False 
)
