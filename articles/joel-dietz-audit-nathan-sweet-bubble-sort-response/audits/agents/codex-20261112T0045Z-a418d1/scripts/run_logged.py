"""Capture an actual command; PRIVATE path is used only to route protected logs."""
import argparse, os
from pathlib import Path
import stage1
ap=argparse.ArgumentParser();ap.add_argument('--private',type=Path,required=True);ap.add_argument('--sensitive',action='store_true');ap.add_argument('label');ap.add_argument('command',nargs=argparse.REMAINDER);a=ap.parse_args()
stage1.PRIV=a.private.resolve()
r=stage1.command(a.label,a.command,Path.cwd(),private=a.sensitive,timeout=300)
print({'label':a.label,'exit_code':r['exit_code'],'stdout_sha256':r['stdout_sha256']})
raise SystemExit(r['exit_code'])
