from pathlib import Path

out_path = Path('output/pdf/app_summary_vk_deeplearning_models.pdf')
out_path.parent.mkdir(parents=True, exist_ok=True)

lines = [
    (16, 50, 760, 'vk_deeplearning_models - One-Page App Summary'),
    (12, 50, 736, 'What it is'),
    (11, 50, 720, 'A compact Python app that trains a feedforward neural network on MNIST digits.'),
    (11, 50, 706, 'It uses stochastic gradient descent with backpropagation and sigmoid activations.'),
    (12, 50, 684, 'Who it\'s for'),
    (11, 50, 668, 'Primary persona: ML learners who want a minimal, readable neural-net training example.'),
    (12, 50, 646, 'What it does'),
    (11, 50, 630, '- Loads MNIST data from ../data/mnist.pkl.gz using gzip + pickle.'),
    (11, 50, 616, '- Reshapes each image into a 784x1 input vector.'),
    (11, 50, 602, '- One-hot encodes training labels into 10x1 target vectors.'),
    (11, 50, 588, '- Builds a dense network from a layer-size list (example: [784, 20, 10]).'),
    (11, 50, 574, '- Initializes biases and weights with Gaussian random values.'),
    (11, 50, 560, '- Trains with mini-batch SGD, backprop, and configurable epochs/batch size/eta.'),
    (11, 50, 546, '- Evaluates test predictions each epoch and prints accuracy counts.'),
    (12, 50, 524, 'How it works (repo-evidence architecture)'),
    (11, 50, 508, '- run_network1.py orchestrates: load data, build Network, call SGD.'),
    (11, 50, 494, '- mnist_loader.py handles data IO and preprocessing for train/val/test splits.'),
    (11, 50, 480, '- network1.py contains model state, feedforward, SGD loop, backprop, evaluate.'),
    (11, 50, 466, '- Data flow: MNIST file -> wrapper transforms -> SGD mini-batches -> epoch metrics.'),
    (12, 50, 444, 'How to run (minimal steps)'),
    (11, 50, 428, '1. Create Python env and install numpy (dependency files: Not found in repo).'),
    (11, 50, 414, '2. Place dataset at ../data/mnist.pkl.gz relative to this repo root.'),
    (11, 50, 400, '3. Run: python3 run_network1.py'),
    (12, 50, 378, 'Not found in repo'),
    (11, 50, 362, '- README, packaged data file, and dataset download/source instructions.'),
    (11, 50, 348, '- CLI/config system, tests, and model checkpoint export path.'),
]


def pdf_escape(text: str) -> str:
    return text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

content_parts = []
for size, x, y, text in lines:
    content_parts.append('BT')
    content_parts.append(f'/F1 {size} Tf')
    content_parts.append(f'1 0 0 1 {x} {y} Tm')
    content_parts.append(f'({pdf_escape(text)}) Tj')
    content_parts.append('ET')
content = ('\n'.join(content_parts) + '\n').encode('latin-1')

objs = []
objs.append('<< /Type /Catalog /Pages 2 0 R >>'.encode('ascii'))
objs.append('<< /Type /Pages /Kids [3 0 R] /Count 1 >>'.encode('ascii'))
objs.append(
    (
        '<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] '
        '/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>'
    ).encode('ascii')
)
objs.append((f'<< /Length {len(content)} >>\nstream\n').encode('ascii') + content + b'endstream')
objs.append('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>'.encode('ascii'))

pdf = bytearray()
pdf.extend(b'%PDF-1.4\n')
offsets = [0]
for i, obj in enumerate(objs, start=1):
    offsets.append(len(pdf))
    pdf.extend(f'{i} 0 obj\n'.encode('ascii'))
    pdf.extend(obj)
    pdf.extend(b'\nendobj\n')

xref_start = len(pdf)
pdf.extend(f'xref\n0 {len(objs) + 1}\n'.encode('ascii'))
pdf.extend(b'0000000000 65535 f \n')
for off in offsets[1:]:
    pdf.extend(f'{off:010d} 00000 n \n'.encode('ascii'))
pdf.extend(
    (
        f'trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\n'
        f'startxref\n{xref_start}\n%%EOF\n'
    ).encode('ascii')
)

out_path.write_bytes(pdf)
print(out_path)
