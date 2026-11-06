# Remotion motion-design dataset

Chat-format examples for fine-tuning and evaluating models that generate Remotion motion-graphics projects.

## Contents and splits

| Archive | Records | Training | Validation | Test |
| --- | ---: | ---: | ---: | ---: |
| `data/remotion-curated.zip` | 11,081 | 9,519 | 787 | 775 |
| `data/motion-ui-remotion-1000.zip` | 1,000 | 950 | 50 | — |
| **Combined source records** | **12,081** | **10,469** | **837** | **775** |

`data/remotion-categories.zip` is a retrieval index containing the 10,469 training records split into 176 family-specific JSONL files. It is not an additional, independent set of examples.

## Use for fine-tuning

1. Download and extract the two source archives.
2. Use `train.jsonl` from `remotion-curated.zip` and `dataset/train.jsonl` from `motion-ui-remotion-1000.zip` for training.
3. Combine only the training files if your trainer expects one file. Keep both validation sets for model selection and the curated test set untouched for final evaluation.
4. Each row uses chat-style `messages` data. Confirm that your chosen fine-tuning service accepts the schema, token limits, and code content before uploading.

Do not train on validation or test rows. The split totals are shown separately so users can preserve evaluation boundaries.

## Data notes

- The curated archive combines the source groups `remotion-30s-3000`, `remotion-combined-9149`, and `toon3d_dataset`; the archive README describes filtering and static type-check details.
- The Motion UI archive contains 32 generated UI, motion-graphics, and WebGL families. Its README reports stub type checks and mock Chromium checks; it explicitly does not report renders with the real Remotion renderer.
- The categorized archive is for training-example retrieval, not an independent evaluation set.
- Generated code patterns and static checks do not guarantee visual quality, runtime correctness, or compatibility with every model/training provider. Render representative outputs with your target Remotion version before relying on them.
- The original archive READMEs and source labels are included in the ZIPs. Review them when citing or building on particular source groups.

## License

The dataset archives are released by the dataset owner under the repository's MIT License. The license permits use, modification, redistribution, and commercial use subject to preserving the copyright and license notice. The MIT license does not provide a warranty or guarantee that generated examples will work in a particular environment.

## Intended use

Training, evaluation, and research on code generation for Remotion motion graphics. Users are responsible for reviewing generated output, respecting platform policies, validating dependencies, and checking that their resulting videos and assets have the rights needed for their intended use.
