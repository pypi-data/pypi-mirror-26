# Get-Template
A simple tool use git repos as template for quick prototyping.

## Installation
```bash
pip install get-template
```

## Usage
Before your first usage, you need to set `get-template` to use a default remote source
```bash
template config set --default-source git@gitlab:your_acount
```

Then pull your templates:
```bash
template init your_template_repo your_dest_directory
```

A new git repository will be initialize in `your_dest_directory`.

Thats all.