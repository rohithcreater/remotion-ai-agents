# Remotion AI Agent — 12K Motion Design Dataset

Build and tune your own AI motion designer for Remotion. This project pairs a local video studio and specialist agents with **12,081 chat-format motion-design examples** for training and evaluation. Use it to create polished product ads, explainers, 3D scenes, kinetic typography, social videos, and more.

Turn your motion skills into commercial video work: make assets for products, clients, and campaigns. The dataset is a strong starting point—not a promise of world-class output, customers, views, or income. Results depend on your model, training, creative direction, offer, and audience.

## What’s included

- **Local agent studio** — browser chat, project file browser, and MP4 preview.
- **Specialist team** — a Studio Director that chooses a fit, plus focused agents for product ads, explainers, kinetic typography, 3D and characters, social shorts, UI motion, music visualizers, and motion review.
- **Structured video brief** — assemble the product, audience, goal, duration, aspect ratio, supported claims, visual direction, and call to action before sending the prompt.
- **Project tools** — read and write text files, run recognized npm checks, and render a Remotion composition.
- **12K tuning dataset** — training, validation, and test archives, plus a training-only categorized archive for prompt retrieval. See [DATASET_CARD.md](DATASET_CARD.md) before tuning.
- **No app dependencies** — the agent server uses Node.js built-ins. The target Remotion project still needs its own dependencies installed.

## Start the agent

Requirements: Node.js 20 or newer, and an existing Remotion project.

1. Open a terminal in this folder.
2. Run `npm start`.
3. Open <http://127.0.0.1:4173>.
4. Select your Remotion project folder in the left panel.
5. Open **Settings** and enter an OpenAI-compatible chat-completions URL and model name. For a local Ollama model, use `http://localhost:11434/v1/chat/completions`. Hosted services may require an API key.
6. Ask the agent to inspect, create, or revise a composition. Request a render when you want an MP4 preview.

## Choose a specialist

Select **Studio Director** to have the agent identify the best-fit approach for each brief, or pick a specialist directly:

- **Product Ad Agent** — product launches, promotions, benefit-led stories, and calls to action.
- **Explainer Agent** — tutorials, educational videos, and clear visual storytelling.
- **Kinetic Type Agent** — titles, editorial motion, and typography-led sequences.
- **3D & Character Agent** — dimensional scenes and stylized character motion, based on the dependencies already in the project.
- **Social Shorts Agent** — vertical short-form videos with a fast hook and concise payoff.
- **UI Motion Agent** — app demos, product screens, and interface micro-interactions.
- **Music Visualizer Agent** — audio-led pacing and beat-aware motion using available audio assets.
- **Motion Review Agent** — reviews source code, timing implied by code, readability choices, and likely render blockers; it does not claim to have watched video when no visual evidence is available.

These are specialist playbooks that share the model configured in Settings; the app does not run separate model instances. For marketing work, give the agent the product, audience, supported benefits, desired length, and next step you want viewers to take. It can help make a polished, commercially focused video, but cannot guarantee views, sales, or income.

Use **Build a stronger video brief** to fill in those details and insert an editable brief into the chat. For feedback on an existing composition, select **Motion Review Agent** and ask for a prioritized code review. Add screenshots or frame exports to the prompt if you want feedback on the rendered image; a text-only source review cannot confirm what the video looks like.

The API key is kept in the browser tab’s memory. It is sent to the model endpoint you choose. The agent listens only on `127.0.0.1` by default.

## Dataset

The public release contains 12,081 chat-format examples across `data/remotion-curated.zip` (11,081 examples) and `data/motion-ui-remotion-1000.zip` (1,000 examples). `data/remotion-categories.zip` contains the 10,469 training examples split into 176 family-specific files for retrieval. See [DATASET_CARD.md](DATASET_CARD.md) for counts, source notes, license, and limitations. **User-reported render verification:** the curated set was rendered and everything appeared correct. The Motion UI archive reports stub type checks and mock Chromium checks, but no real Remotion render. Keep evaluation splits out of retrieval and training.

The agent ranks training examples in `data/remotion-categories.zip` by shared prompt, family, source, and palette terms, then supplies up to three examples to the model as references. Validation and test records are excluded from retrieval. The model is instructed to adapt relevant patterns to the current prompt instead of copying an unrelated example.

Before training, read the archive’s `README.md`, confirm the dataset license and source terms, preserve the supplied splits, and use a context length suitable for the long assistant outputs (the source reports a median around 11.5k characters). Keep the test split untouched for final evaluation. Do not train on validation or test records.

The app uses the categorized dataset for prompt-based example retrieval; it does not automatically fine-tune a model. The retrieval is lightweight keyword matching, not semantic embeddings, so very different wording may miss useful examples.

## Agent tools and boundaries

- `list_project_files` and `read_project_file` inspect the selected project.
- `write_project_file` edits files inside that project only.
- `run_project_check` can invoke existing `check`, `typecheck`, `lint`, or `build` scripts.
- `render_remotion` renders a named composition to an MP4 in the selected project.

The agent cannot run arbitrary shell commands. It does not delete files. Review generated changes before using them in production, and do not point it at folders containing secrets or unrelated work.

## Current limitations

- Model endpoints must support OpenAI-compatible chat completions and tool calls.
- Conversation history lives in the current browser tab; it is not a durable database.
- The included dataset is not automatically loaded into the model context.
- The app does not install Remotion into target projects or download browser binaries.
- No visual render QA is claimed until you render and inspect the result.

## Dataset archive layout

Inside `data/remotion-curated.zip` are `train.jsonl`, `validation.jsonl`, `test.jsonl`, `README.md`, and `scripts/`. The Motion UI archive has `dataset/train.jsonl`, `dataset/val.jsonl`, and `dataset/dataset.jsonl`. The separate `data/remotion-categories.zip` contains family-specific JSONL files under `categories/`, plus an index. Each category file contains training examples for one animation family. The dataset archives are distributed under the repository's MIT license as owner-provided material; source names are retained in the dataset metadata.
