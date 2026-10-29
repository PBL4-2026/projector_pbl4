# Software usage {#software_usage}

Once the projectors are in place (see @ref hardware_setup "Hardware setup"),
install the program on the computer that drives them. It needs Python 3.14,
`numpy` and `opencv-python`. `pytest` is only for development.

## Install

We use [uv](https://docs.astral.sh/uv/) because it fetches the right Python
version by itself.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone git@github.com:maksym-syd/projector_pbl4.git
cd projector_pbl4
uv sync
```

That first line is for macOS and Linux. On Windows run
`powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
instead. `uv sync` creates `.venv/` and installs the versions in `uv.lock`.

If uv is not an option, make a Python 3.14 virtual environment and use pip:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate it with `.venv\Scripts\Activate.ps1`.

## Settings

`SetupClass` reads the settings and rejects values that do not make sense.

| Setting | Value |
|---------|-------|
| Projector resolution | native resolution of the projectors |
| Image width | TODO: is this the `w` measured earlier? |
| Projector spacing | `d` from the hardware setup |
| Blending gamma | how fast the brightness fades in the overlap |
| Source path | image to project |
| Side | `LEFT` or `RIGHT` |

TODO: where these are set (file, arguments or constants).

## Run

Start one instance per projector and give each its own side.

```bash
uv run python <script>.py
```

TODO: name of the script that starts the pipeline.

## Check the displays first

Before running the pipeline, make sure each projector shows up as its own
screen. `display.py` ends with a smoke test for this. It draws a test
picture, saves it as `images/sample.jpg`, loads it back and shows it
full-screen.

```bash
uv run python display.py
```

Press `q` or `ESC` to close it. It also closes on its own after 30 seconds.
To pick the screen, edit the `screens` list in the smoke test. Each entry is
`(x, y, width, height)` in logical pixels, and the picture appears on index
0.

Tests run with `uv run pytest`.

@note Most modules are generated from a UML model. Keep the `# ˅` and `# ˄`
markers and write your code between them, otherwise it is overwritten the
next time the code is generated.

Back to the @ref index "main page".
