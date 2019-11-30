import sys, subprocess, os, ujson
from pathlib import Path

for i in range(len(sys.argv), 3):
    sys.argv.append(None)

# for running specific dataset
ds_id = sys.argv[1] or ""
extra_args = sys.argv[2] or ""

datasets_dir = Path(os.path.abspath(__file__)).parent
for dpath in sorted(datasets_dir.iterdir()):
    if dpath.name.find(ds_id) == -1:
        continue

    with open(os.path.join(dpath, "drepr.json"), "r") as f:
        datasets = ujson.load(f)

    for i, dataset in enumerate(datasets):
        print(">>> convert dataset", dpath.name, "-", i)
        resources = " ".join([
            f"{rid}='{os.path.join(dpath, rfile)}'" for rid, rfile in dataset['resources'].items()
        ])
        ds_model = os.path.join(dpath, dataset['drepr'])
        output_file = os.path.join(dpath, dataset['output'])
        Path(output_file).parent.mkdir(exist_ok=True)
        try:
            if output_file.endswith(".gz"):
                # detect compression
                tmp_output_file = output_file.replace(".gz", "")
            else:
                tmp_output_file = output_file

            subprocess.check_call(
                f"python -m drepr.main -r {ds_model} -d {resources} -f ttl -o {tmp_output_file} {extra_args}",
                shell=True)

            if output_file.endswith(".gz"):
                # compress the file
                subprocess.check_call(
                    f"tar -czf {output_file} {tmp_output_file} && rm {tmp_output_file}", shell=True)
        except:
            print(">>> Terminate due to error")
            exit(1)

        print("\t+Generate tables for debugging")
        # generate table for debugging
        debug_file = str(Path(output_file).parent / 'tmp')
        subprocess.check_call(
            f"python -m drepr.main -r {ds_model} -d {resources} -f graph_json -o {debug_file} {extra_args} && python graph2csv.py {debug_file}",
            shell=True)
