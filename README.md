# HOTS PARSER
A tool to parse hots games. I made it to track scrims and games data. It then writes the data to a spreadsheet. Here is a sample [spreadsheet](https://docs.google.com/spreadsheets/d/1peqLDPnbXkSGZIvb6IB_JugES4hhzscq6X8SD2uTpyQ/edit?usp=sharing).

## Usage
1. Git clone
2. Make sure you are using Python3.11, since `hero protocol` uses the deprecated `imp` module.
3. `pip install gspread`
4. Git clone the [hero protocol](https://github.com/Blizzard/heroprotocol) repo, into this repo. (I couldn't get the pip install to work, it seems out of date. Janitor update it!!!)
5. Configure [`gspread`](https://docs.gspread.org/en/latest/oauth2.html).
6. Add the `service_account.json` file to a local `gspread` directory.
   So in the end you should have :
   ```
   hots-parser repo
     |- heroprotocol
     |- gspread
           |- service_account.json
   ```
7. Set the spreadsheet name in [sheet.py](https://github.com/LeoOuyang24/hots-parser/blob/361a094e0e7dd2ae0bb9f848cbee93447eb557be/sheets.py#L17).
8. Set the absolute path to heroprotocol's module in [collect.py](https://github.com/LeoOuyang24/hots-parser/blob/9f8621b8e4fca8ede5228904a177a4a0f1accb91/collect.py#L12).
9. Set the team member names you are interested in [collect.py](https://github.com/LeoOuyang24/hots-parser/blob/9f8621b8e4fca8ede5228904a177a4a0f1accb91/collect.py#L21).
   - Yes this should in fact all be command line arguments lalalala I CANT HEAR YOU!!!! (also like who tf else is running this repo? Is anyone even reading this? Am I truly alone here? Is there a god? If there was why would He allow such pain and suffering to exist?)
10. `python3 fensad_data.py`
   
