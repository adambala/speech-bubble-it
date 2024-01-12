# Speech Bubble It
Speech Bubble It is a Python script that puts a speech bubble on an image

## About
Online communication is accompanied by various jokes in the form of images (mostly memes). These also include speech bubbles.

The point of such images is that the sender presents the user in a chat as a character or a thing that speaks its message in a speech bubble.

## Instructions
This script does not require large resources to create an image with a speech bubble. It requires `Python 3.10` or above and these dependencies:
- Pillow

You can install them by running `pip install -r requirements.txt` 

Speech Bubble It can be used from the command line:
```sh
python speech_bubble_it.py <image path> <output path>
```

where
- `<image path>` is the path of an image you want to put speech bubble on;
- `<output path>` is the path to the file where the result will be written to.

The script supports such image formats as `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.webp` and `.tiff`.

## Optional arguments
You can transform your speech bubble by these flags:
- `-h`, `--help` — help information;
- `-m`, `--mirror` — flips speech bubble horizontally;
- `-o`, `--orientation` — changes speech bubble orientation (1: on the top; 2: on the left; 3: on the bottom; 4: on the right).

## Example

```sh
python speech_bubble_it.py .\input\input.jpg .\output\output.png
```

.\input\input.jpg          |  .\output\output.png
:-------------------------:|:-------------------------:
![](N/A)                   |  ![](N/A)

## Contributions
This repository is open for contributing. So feel free to open issues and make pull requests.

## TODO
- [ ] Implement the support of images from web
- [ ] Use vector image of the speech bubble instead of `.png`