STEP 9 — Print 'I am filling in the metadata form', then download the reference files via bash:
   mkdir -p /data/tmp_form
   wget -q -O /data/tmp_form/metadata.json https://raw.githubusercontent.com/pegi3s/dockerfiles/master/metadata/metadata.json
   wget -q -O /data/tmp_form/dio.diaf https://raw.githubusercontent.com/pegi3s/dockerfiles/master/metadata/dio.diaf

Then identify analogous tools — tools in metadata.json whose domain/function matches pegi3s/<program_name> — by running via bash (replace <keyword> with 1–3 words that describe the tool's function, e.g. "alignment", "assembly", "annotation", "phylogenetics"):
   jq -r '.[] | select(.description | test("<keyword>"; "i")) | {name,description,input_data_type,usual_invocation_specific,test_invocation_specific,custom_searches,auto_tests}' /data/tmp_form/metadata.json | head -400

Then find the DIO classification codes for those analogous tools via bash:
   grep -E "<analogous_tool_1>|<analogous_tool_2>|<analogous_tool_3>" /data/tmp_form/dio.diaf

Use the analogous entries as templates to fill in all fields for pegi3s/<program_name> as described below, then write the two output files via bash. Do NOT print their contents as text in your reply — ALL file writes MUST go through your bash tool.

==============================================================
HOW TO FILL IN EACH FIELD (use analogous tools as models)
==============================================================

name
  The repository / program name (e.g. "clustalomega"). Already known from the GitHub URL.

description
  A concise lowercase phrase of 2–5 words describing what the tool does (e.g. "Sequence alignment",
  "Phylogenetics inferences", "de novo sequence assembler"). Copy the style from analogous entries.
  Never use the tool's own name in the description.

project_active
  Boolean. Check the GitHub repository (archive banner, README notes, last commit/release activity)
  for any indication that the project is discontinued or no longer maintained (e.g. the repo is
  archived, or the README states it is deprecated/unmaintained/no longer developed). Set to false
  if such an indication is found, otherwise set to true.

status
  Always "Usable" (the build and test succeeded).

recommended / latest
  Use the image version tag established in STEP 5. For recommended[0].date use today's date in
  DD/MM/YYYY format (e.g. "11/05/2026"). Set latest to the same version string.

bug_found / not_working / no_longer_tested
  Always [] for a newly built image.

manual_url
  The documentation URL found in the README (STEP 3). Use "" if none.

source_url
  The GitHub URL provided by the user.

comments
  An array of strings. Include any important usage notes found in the README (e.g. GUI notes,
  special invocation requirements). Use [] if none.

gui / gui_command
  Set gui to true only if the tool is a graphical application (inferred from README). If gui is
  true, set gui_command to the command that launches the GUI (from the README); otherwise "".

podman / singularity
  Always "untested".

invocation_general
  Always exactly: "docker run --rm -v /your/data/dir:/data pegi3s/<program_name>"
  Exception: if the tool requires additional flags (e.g. -v /var/run/docker.sock:/var/run/docker.sock),
  include them — infer from the README and from analogous tool entries.

usual_invocation_specific
  The typical command arguments after the image name. Derive from the README (STEP 3) and the test
  run performed in STEP 8. Use generic placeholder names for files (e.g. /data/fastaFile,
  /data/output/out_name). Follow the exact style of analogous entries. Always use canonical
  extensions in placeholder filenames — e.g. /data/output.fas not /data/output.afa.

usual_invocation_specific_comments
  Array of strings explaining the parameters. Copy the style from analogous entries. Use [] if none.

test_invocation_specific
  The command arguments used in STEP 8, but rewritten with conventional paths:
    - Replace /data/dockeragent_results/test_data/<file>  →  /data/test/data/<file>
    - Replace /data/dockeragent_results/<program_name>/test/<result>  →  /data/test/results/<result>
  Use "" if no suitable test data was found in STEP 8.

test_data_url
  "http://evolution6.i3s.up.pt/static/pegi3s/dockerfiles/input_test_data/<test_file>"
  where <test_file> is the actual input file used in STEP 8 (e.g. "SRR3143588_1.fastq",
  "small_not_aligned.fas"). Use "" if no suitable test data was found.

test_results_url
  Always "" for a newly built image.

icon
  The URL to an icon/logo image found in the README or the GitHub repository (e.g. a raw
  githubusercontent.com URL to a .png or .svg). Use "" if none is found.

input_data_type
  An array of short lowercase tokens describing the required input file types. Use exactly the
  same tokens as analogous tools that accept the same formats (e.g. ["fasta"], ["fastq"],
  ["newick", "fasta"]). Infer from the README and STEP 8 test files.

auto_tests
  A single-element array. Fill using the information from STEP 8:
    docker_image:  "pegi3s/<program_name>:<version>" (include the version tag)
    input_files:   array of input filenames (just the basenames from /data/dockeragent_results/test_data/; use the canonical extension — e.g. .fas/.fasta for FASTA, never .afa or other non-standard variants)
    output_dir:    the output subdirectory name used in STEP 8 (e.g. "clustalomega_output")
    output_file:   the primary output filename (use the canonical extension — e.g. .fas/.fasta for aligned FASTA output, never .afa or other non-standard variants)
    add_config:    "" (unless the tool requires extra docker flags — use those from STEP 8)
    commands:      the full command after the image name, rewritten with conventional paths:
                     - input files:  /data/input_data/<file>
                     - output files: /data/output_folder/<output_dir>/<output_file>
                   Append " > /dev/null 2>&1" at the end.
  If no suitable test data was found in STEP 8, use:
    [{"docker_image": "pegi3s/<program_name>", "input_files": [], "output_dir": "", "output_file": "", "add_config": "", "commands": ""}]

custom_searches
  Four search query strings for literature discovery. Derive the keywords from the tool name and
  the key authors / paper title found in the README. Follow the exact key/format of analogous
  entries:
    "pubmed":             "term=<keywords>"
    "scholar":            "q=<keywords>"
    "bioprotocol":        "content=<keywords>"
    "bioprotocol_exchange": "content=<keywords>"
  If no paper is referenced, use the tool name alone as the keyword in all four fields.

==============================================================
DIO CLASSIFICATION
==============================================================

The file /data/tmp_form/dio.diaf maps DIO ontology codes to tool names using tab-separated lines:
  DIO:XXXXXXX\t<tool_name>

Apply the same DIO code(s) to pegi3s/<program_name> that were assigned to the analogous tools
identified above. A single tool may receive multiple DIO codes (one line per code).

==============================================================
OUTPUT FILES — replicate pegi3s/contribute's for_submission folder
==============================================================

Write all files via bash — do NOT print their contents as plain text.

--- Step A: write the metadata files into the project directory ---

1. /data/dockeragent_results/<program_name>/metadata.json
   A single JSON object (not wrapped in an array) containing all fields listed above, in this order:
   name, description, project_active, status, recommended, latest, bug_found, not_working, no_longer_tested,
   manual_url, source_url, comments, gui, gui_command, podman, singularity, invocation_general,
   usual_invocation_specific, usual_invocation_specific_comments, test_invocation_specific,
   test_data_url, test_results_url, icon, input_data_type, auto_tests, custom_searches
   Write with Python: json.dump(obj, f, indent=4, ensure_ascii=False)

2. /data/dockeragent_results/<program_name>/ontology.diaf
   Plain text, one DIO ID per line, with a header comment. Exact format:
     # Ontology terms
     DIO:XXXXXXX
     DIO:YYYYYYY
   Do NOT append a tab or the tool name after the DIO ID.

3. /data/dockeragent_results/<program_name>/README.md
   The README for the pegi3s/<program_name> Docker image, following the standard pegi3s format.
   Write it via bash using Python — do NOT print its contents as text in your reply.
   Derive all values from the information gathered in previous steps (STEP 3 README and STEP 8
   test run). The README must contain exactly the following five sections in order:

   SECTION 1 — Copyright header (copy verbatim):
     # This image belongs to a larger project called Bioinformatics Docker Images Project (http://pegi3s.github.io/dockerfiles)
     ## (Please note that the original software licenses still apply)

   SECTION 2 — Short description sentence (one line):
     This image facilitates the usage of [<Program Name>](<source_url>), a <description>.
     • <Program Name> : the human-readable name of the tool (capitalised as appropriate)
     • <source_url>   : the GitHub URL provided by the user (same as source_url in metadata.json)
     • <description>  : the brief lowercase phrase from the description field of metadata.json,
                        NOT starting with the tool's own name (e.g. "a multiple sequence alignment
                        tool", "a de novo sequence assembler")

   SECTION 3 — Linux usage section:
     # Using the <Program Name> image in Linux

     You should adapt and run the following command: `docker run --rm -v /your/data/dir:/data pegi3s/<program_name> <typical_args>`

     In this command, you should replace:
     - `/your/data/dir` to point to the directory that contains the input file(s).
     - `<placeholder1>` to the actual name of your <file type> file.
     - `<placeholder2>` to the actual name of your output file.
     (Add or remove bullet points to match the actual parameters of the tool; use the
     usual_invocation_specific value from metadata.json as the source for <typical_args>
     and placeholder names. Always use canonical extensions in placeholder filenames —
     e.g. output.fas not output.afa.)

     To see the [<Program Name>](<manual_url if non-empty, otherwise source_url>) help, just run `docker run --rm pegi3s/<program_name> --help`.
     (Use the actual help flag if different from --help; omit this sentence only if the tool
     has no help option at all.)

   Write with Python:
     python3 << 'EOF'
     content = """<assembled README text>"""
     with open('/data/dockeragent_results/<program_name>/README.md', 'w') as f:
         f.write(content)
     EOF

--- Step B: assemble the for_submission folder ---

Create the folder skeleton:
   mkdir -p /data/dockeragent_results/<program_name>/for_submission/test_data/input_test_data
   mkdir -p /data/dockeragent_results/<program_name>/for_submission/test_data/output_test_data

Move every flat file at the top level of the project directory (Dockerfile, README.md,
metadata.json, ontology.diaf, and any other non-directory items) into for_submission/,
skipping subdirectories — exactly as pegi3s/contribute does:
   for f in /data/dockeragent_results/<program_name>/*; do
     [ -f "$f" ] && mv "$f" /data/dockeragent_results/<program_name>/for_submission/
   done

Package input test data (only the file(s) listed in auto_tests[0].input_files — i.e. the actual
input files used in STEP 8 — not all files that may be present in test_data/):
   INPUT_COUNT=<number of files in auto_tests[0].input_files>
   if [ "$INPUT_COUNT" -eq 1 ]; then
     # single file — copy directly, preserving the filename
     cp /data/dockeragent_results/test_data/<input_file> \
        /data/dockeragent_results/<program_name>/for_submission/test_data/input_test_data/
   elif [ "$INPUT_COUNT" -gt 1 ]; then
     # multiple files — zip only the files used in the test into one archive
     cd /data/dockeragent_results/test_data && \
     zip /data/dockeragent_results/<program_name>/for_submission/test_data/input_test_data/<program_name>.zip <input_file_1> <input_file_2> ...
   fi

Package output test data (always zipped, even if there is only one file). Exclude the `run`
script and any input data files (i.e. the files listed in auto_tests[0].input_files) — zip only
the actual result files produced by the tool:
   OUTPUT_COUNT=$(ls /data/dockeragent_results/<program_name>/test/ 2>/dev/null | wc -l)
   if [ "$OUTPUT_COUNT" -gt 0 ]; then
     cd /data/dockeragent_results/<program_name>/test && \
     zip /data/dockeragent_results/<program_name>/for_submission/test_data/output_test_data/<program_name>_output.zip * --exclude run --exclude <input_file_1> --exclude <input_file_2> ...
   fi

The final for_submission layout must be:
   for_submission/
   ├── Dockerfile
   ├── README.md
   ├── metadata.json
   ├── ontology.diaf
   └── test_data/
       ├── input_test_data/
       │   └── <file>               ← single input file copied directly, OR
       │   └── <program_name>.zip   ← all input files zipped if more than one
       └── output_test_data/
           └── <program_name>_output.zip

After assembling, print the tree so the user can verify:
   find /data/dockeragent_results/<program_name>/for_submission/ -type f | sort

==============================================================
Additional rules:
==============================================================
- If jq is not available, install it first: apt-get install -y jq
- Always validate the metadata.json with: python3 -c "import json; json.load(open('/data/dockeragent_results/<program_name>/metadata.json'))" and fix any JSON errors before finishing.
- Do NOT invent DIO codes that do not exist in /data/tmp_form/dio.diaf. Only assign codes already present in that file.
- If no analogous tool can be found with the initial keyword, try broader or alternative keywords.
- The two output files and the for_submission folder structure of this step MUST match exactly what https://github.com/pegi3s/contribute produces:
  * metadata.json  — a single JSON object, pretty-printed with indent=4, written with json.dump(obj, f, indent=4, ensure_ascii=False)
  * ontology.diaf  — plain text: first line is "# Ontology terms", then one DIO ID per line (e.g. "DIO:0000042"), NO tab, NO tool name appended to the ID.
