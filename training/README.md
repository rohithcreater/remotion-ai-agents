# Kaggle QLoRA kit

This starter kit fine-tunes **Qwen2.5-Coder-1.5B-Instruct** with 4-bit QLoRA using one Kaggle GPU. It saves a small LoRA adapter; it does not rewrite or redistribute the base model. The model is a practical starting point for a Kaggle GPU, not a claim that it is the best model for every user. A T4 x2 session does not combine both cards into one 32 GB device; this script deliberately uses the first GPU.

## Run it in Kaggle

1. Open `kaggle_qlora.ipynb` on Kaggle and enable **Internet** plus a **GPU accelerator** in Notebook settings.
2. Run the cells from top to bottom. The notebook downloads this repository's two source data archives and the training script.
3. The first run uses 1,000 training rows and 200 validation rows so users can estimate time and memory use. The test split is never loaded.
4. The adapter is saved under `/kaggle/working/remotion-qlora`; download it from the notebook Output panel before the session ends.

To use every training row and all validation rows, change the command to pass `--max-train-samples 0 --max-eval-samples 0`. This may take much longer and consume substantial GPU quota. Kaggle's GPU types, availability, and quotas can change; see Kaggle's current [Notebook documentation](https://www.kaggle.com/docs/notebooks) and [GPU usage guide](https://www.kaggle.com/docs/efficient-gpu-usage).

## Customize

The reusable entry point is `train_qlora.py`. It accepts the two archive paths, model ID, maximum sequence length, sample caps, number of epochs, and optional maximum training steps. Start with a smaller model and a 4,096-token limit; raise `--max-length` to 8,192 only if the selected GPU has enough memory. Longer examples may be truncated at the configured limit.

The script uses Hugging Face TRL's conversational SFT trainer with assistant-only loss, PEFT LoRA, and bitsandbytes NF4 quantization. The dataset's test split is deliberately not read by the trainer. The validation result is training-time evaluation only; it is not proof of improved motion quality. Compare the adapter against the base model on the untouched test set and render representative Remotion projects before making quality claims.

Example command for the full training split, after downloading both ZIPs:

```bash
python training/train_qlora.py \
  --curated-zip data/remotion-curated.zip \
  --motion-ui-zip data/motion-ui-remotion-1000.zip \
  --max-train-samples 0 \
  --max-eval-samples 0 \
  --max-length 4096
```

The sample model is [Qwen2.5-Coder-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct), listed as Apache-2.0 on its model page. Check the base model's current license and usage conditions before distributing a merged model or adapter. The dataset itself is licensed under this repository's MIT license.
