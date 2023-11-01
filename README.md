# Press Ganey Survey Submitter

Handle parsing of spreadsheet reports to a format acceptable to Press Ganey then upload the spreadsheet to Press Ganey to initiate patient survey distribution.

## Setup

* Install Python 3.12 or higher.
* Open a terminal window and navigate to the desired parent directory on your computer.
* Run `git clone https://github.com/ManzellaTech/PressGaneySurveySubmitter.git` to get the project files.
* In the terminal window, navigate into the "PressGaneySurveySubmitter" directory.
* Optional: create and activate a virtual environment.
* Run `python3 -m pip install -r requirements.txt` (on Windows replace "python3" with "py").
* Edit "config.json" in the same directory as "main.py" to handle column renaming, sanitizing input, etc.  The output spreadsheet's column order is determined the order of the "columns" array in "config.json".  Add the Survey Designator and Client ID (obtained from Press Ganey) to the "config.json" file.  

## Usage

Run `python3 main.py`.  CLI options can be provided.  If no CLI options are provided, the script will prompt for user input.  SFTP credentials are stored as Environment Variables.  

CLI Options:

  -h, --help &emsp; Show this help message and exit

  -c CONFIG_PATH, --config CONFIG_PATH &emsp; Path to the config JSON file (default is "config.json").

  -f INPUT_FILE, --file INPUT_FILE &emsp; Path to the input .xlsx spreadsheet.

  -n, --no-transmit &emsp; Do not transmit the output spreadsheet to Press Ganey.

  -s, --sftp-transmit &emsp; Transmit the output spreadsheet to Press Ganey via SFTP.
