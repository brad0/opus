import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("config_name", type=str, help="name of config file (.yml will be appended)")
parser.add_argument("test_name", type=str, help="name for test result display")
parser.add_argument("checkpoint", type=str, help="checkpoint to test")
parser.add_argument("--lpcnet-demo", type=str, help="path to lpcnet_demo binary, default: /local/code/LPCNet/lpcnet_demo", default="/local/code/LPCNet/lpcnet_demo")
parser.add_argument("--lpcnext-path", type=str, help="path to lpcnext folder, defalut: dirname(__file__)", default=os.path.dirname(__file__))
parser.add_argument("--python-exe", type=str, help='python executable path, default: sys.executable', default=sys.executable)
parser.add_argument("--pad", type=str, help="left pad of output in seconds, default: 0.015", default="0.015")
parser.add_argument("--trim", type=str, help="left trim of output in seconds, default: 0", default="0")



template='''
test: "{NAME}"
processing:
  - "sox {{INPUT}} {{INPUT}}.raw"
  - "{LPCNET_DEMO} -features {{INPUT}}.raw {{INPUT}}.features.f32"
  - "{PYTHON} {WORKING}/test_lpcnet.py {{INPUT}}.features.f32 {CHECKPOINT} {{OUTPUT}}.ua.wav"
  - "sox {{OUTPUT}}.ua.wav {{OUTPUT}}.uap.wav pad {PAD}"
  - "sox {{OUTPUT}}.uap.wav {{OUTPUT}} trim {TRIM}"
  - "rm {{INPUT}}.raw {{OUTPUT}}.uap.wav {{OUTPUT}}.ua.wav {{INPUT}}.features.f32"
'''

if __name__ == "__main__":
    args = parser.parse_args()


    file_content = template.format(
        NAME=args.test_name,
        LPCNET_DEMO=os.path.abspath(args.lpcnet_demo),
        PYTHON=os.path.abspath(args.python_exe),
        PAD=args.pad,
        TRIM=args.trim,
        WORKING=os.path.abspath(args.lpcnext_path),
        CHECKPOINT=os.path.abspath(args.checkpoint)
    )

    print(file_content)

    filename = args.config_name
    if not filename.endswith(".yml"):
        filename += ".yml"

    with open(filename, "w") as f:
        f.write(file_content)
