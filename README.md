# projector_pbl4

A pipeline for multi-projector edge blending: it crops a source image for each projector (left / right), applies a blend mask to the overlapping region, and displays the result.

## Requirements

- Python **3.14** (pinned in `.python-version`)
- Dependencies (defined in `pyproject.toml`, locked in `uv.lock`)
  - Runtime: `numpy`, `opencv-python`
  - Development: `pytest`

---

## Option A: Using uv (recommended)

[uv](https://docs.astral.sh/uv/) manages the Python version, the virtual environment, and dependencies in one tool.

### 1. Install uv

**macOS / Linux**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell)**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Alternatives**

```bash
brew install uv      # Homebrew
pipx install uv      # pipx
pip install uv       # pip
```

Restart your terminal, then check the installation:

```bash
uv --version
```

See the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/) for more options.

### 2. Set up the project

```bash
git clone git@github.com:maksym-syd/projector_pbl4.git
cd projector_pbl4
uv sync
```

`uv sync` downloads Python 3.14 if needed, creates `.venv/`, and installs the exact versions from `uv.lock`.

### 3. Run the code

```bash
uv run python <script>.py
uv run pytest
```

`uv run` always uses the project's virtual environment, so you don't need to activate it.

### Managing dependencies

| Task | Command |
|---|---|
| Add a runtime dependency | `uv add <package>` |
| Add a development dependency | `uv add --dev <package>` |
| Remove a dependency | `uv remove <package>` |
| Upgrade locked versions | `uv lock --upgrade` |
| Sync after pulling changes | `uv sync` |

> [!IMPORTANT]
> After you change dependencies, regenerate the requirements files (see [Option B](#option-b-without-uv-pip--venv)) and commit `pyproject.toml`, `uv.lock`, `requirements.txt`, and `requirements-dev.txt` together.

---

## Option B: Without uv (pip + venv)

If you can't install uv, you can use the standard `venv` and `pip` tools.

### 1. Install Python 3.14

Download it from [python.org](https://www.python.org/downloads/) and check the version:

```bash
python3 --version   # Windows: py -3.14 --version
```

### 2. Create and activate a virtual environment

**macOS / Linux**

```bash
git clone git@github.com:maksym-syd/projector_pbl4.git
cd projector_pbl4
python3.14 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
git clone git@github.com:maksym-syd/projector_pbl4.git
cd projector_pbl4
py -3.14 -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

The requirements files are exported from `uv.lock`, so pip installs the same versions as uv:

```bash
pip install --upgrade pip
pip install -r requirements-dev.txt   # runtime + development (pytest)
# or, runtime only:
pip install -r requirements.txt
```

### 4. Run the code

With the virtual environment activated:

```bash
python <script>.py
pytest
```

Run `deactivate` to leave the virtual environment.

> [!NOTE]
> `requirements.txt` and `requirements-dev.txt` are generated files. Don't edit them by hand. After you change dependencies with uv, regenerate them:
>
> ```bash
> uv export --no-hashes --no-dev --format requirements-txt -o requirements.txt
> uv export --no-hashes --format requirements-txt -o requirements-dev.txt
> ```

---

## Project structure

| File | Description |
|---|---|
| `pipeline_class.py` | Main pipeline: load → scale → crop → apply mask → display |
| `setup_class.py` | Loads and validates the configuration (resolution, image width, projector spacing, gamma, source path, side) |
| `math_class.py` | Calculations for overlap, pixels per cm, crop region, and blend mask |
| `region.py` | Crop region (x start and width in pixels) |
| `mask.py` | Blend mask (alpha values) |
| `side.py` | `Side` enum (`LEFT` / `RIGHT`) |
| `image.py`, `display.py` | Image and display classes |

> [!NOTE]
> The modules are generated from a UML model. Keep the `# ˅` / `# ˄` markers and write your code between them so it is kept when the code is regenerated.

## Smoke test: full-screen on a chosen screen

`display.py` has a manual smoke test at the bottom of the file. It writes a
generated test picture to `images/sample.jpg`, loads it back through
`Image.load`, and shows it full-screen:

```bash
uv run python display.py
```

Press `q` or `ESC` to quit; the window also closes by itself after 30 s, so the
run can never hang unattended.

Edit the `screens` list inside the smoke test to match your desk layout — each
entry is `(x, y, width, height)` in **logical** pixels, and index 0 is the
monitor to show on.

## License

See [LICENSE](LICENSE).
