# You-Know
### Created by Pierce Dreiling, Alan Sanchez, Caleb Schoenberg, Cade Stephens, and Khai Thieu

This app is a recreation of the classic card game Uno but with a learning twist. Users can also
access and study question sets they upload/create, similar to Quizlet study sets and flashcards.

## Installation
The only python package required to run our program is PyQT6.
`pip install pyqt6`

## Run
Run `app.py` to start the application.

## Specifications
- There needs to be at least 1 study set in the database at all times, or else
the main game will crash. There are already 4 study sets preloaded into the database.
- Users can upload a JSON file with a study set in the exact format of the sample files
in the `json/` directory. The file name is the name of the set, so use separate files to 
upload multiple sets.
- Users can select the study set to correspond with a card's color, i.e. red is Math. Set-color
mappings are randomly assigned when the app is first loaded.