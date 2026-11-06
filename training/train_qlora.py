"""QLoRA fine-tuning entry point for the Remotion chat-format dataset."""

import argparse
import json
import random
import zipfile
from pathlib import Path


def read_jsonl_from_zip(archive_path: Path, member_suffix: str, limit: int = 0):
    with zipfile.ZipFile(archive_path) as archive:
        matches = [name for name in archive.namelist() if name.endswith(member_suffix)]
        if len(matches) != 1:
            raise ValueError(f"Expected one {member_suffix!r} in {archive_path}, found {len(matches)}")
        rows = []
        with archive.open(matches[0]) as source:
            for raw in source:
                if not raw.strip():
                    continue
                row = json.loads(raw)
                messages = row.get("messages")
                if not isinstance(messages, list) or not any(m.get("role") == "assistant" for m in messages):
                    raise ValueError(f"Invalid chat example in {archive_path}: expected messages with assistant output")
                rows.append({"messages": messages})
                if limit and len(rows) >= limit:
                    break
        return rows


def select_rows(rows, limit: int, seed: int):
    if not limit or limit >= len(rows):
        return rows
    indices = list(range(len(rows)))
    random.Random(seed).shuffle(indices)
    return [rows[i] for i in indices[:limit]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--curated-zip", type=Path, required=True)
    parser.add_argument("--motion-ui-zip", type=Path, required=True)
    parser.add_argument("--model", default="Qwen/Qwen2.5-Coder-1.5B-Instruct")
    parser.add_argument("--output-dir", type=Path, default=Path("training/output/remotion-qlora"))
    parser.add_argument("--max-length", type=int, default=4096)
    parser.add_argument("--max-train-samples", type=int, default=1000, help="0 uses all 10,469 training rows")
    parser.add_argument("--max-eval-samples", type=int, default=200, help="0 uses all 837 validation rows")
    parser.add_argument("--max-steps", type=int, default=-1, help="-1 trains for the configured epoch count")
    parser.add_argument("--epochs", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    from datasets import Dataset
    import torch
    from peft import LoraConfig
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    from trl import SFTConfig, SFTTrainer

    curated_train = read_jsonl_from_zip(args.curated_zip, "train.jsonl")
    motion_train = read_jsonl_from_zip(args.motion_ui_zip, "dataset/train.jsonl")
    curated_eval = read_jsonl_from_zip(args.curated_zip, "validation.jsonl")
    motion_eval = read_jsonl_from_zip(args.motion_ui_zip, "dataset/val.jsonl")
    train_rows = select_rows(curated_train + motion_train, args.max_train_samples, args.seed)
    eval_rows = select_rows(curated_eval + motion_eval, args.max_eval_samples, args.seed)
    print(f"Training rows: {len(train_rows)}; validation rows: {len(eval_rows)}; test rows are not loaded.")

    if not torch.cuda.is_available():
        raise RuntimeError("A CUDA GPU is required. In Kaggle, enable a GPU accelerator in Notebook settings.")
    quantization = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.float16,
    )
    tokenizer = AutoTokenizer.from_pretrained(args.model, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        quantization_config=quantization,
        torch_dtype=torch.float16,
        device_map={"": 0},
    )
    model.config.use_cache = False

    training_args = SFTConfig(
        output_dir=str(args.output_dir),
        max_length=args.max_length,
        num_train_epochs=args.epochs,
        max_steps=args.max_steps,
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=8,
        gradient_checkpointing=True,
        learning_rate=2e-4,
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,
        logging_steps=10,
        eval_strategy="steps",
        eval_steps=100,
        save_strategy="steps",
        save_steps=100,
        save_total_limit=2,
        optim="paged_adamw_8bit",
        fp16=True,
        bf16=False,
        assistant_only_loss=True,
        eos_token=tokenizer.eos_token,
        report_to="none",
        seed=args.seed,
        data_seed=args.seed,
    )
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=Dataset.from_list(train_rows),
        eval_dataset=Dataset.from_list(eval_rows),
        processing_class=tokenizer,
        peft_config=LoraConfig(
            r=16,
            lora_alpha=32,
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM",
            target_modules="all-linear",
        ),
    )
    trainer.train()
    print("Validation metrics:", trainer.evaluate())
    trainer.save_model(str(args.output_dir))
    tokenizer.save_pretrained(str(args.output_dir))
    print(f"LoRA adapter and tokenizer saved to {args.output_dir}")


if __name__ == "__main__":
    main()
