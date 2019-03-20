set output=Z:\DocumentsAndStuff\DownloadedStuff\GitHub\EyeTrackerAnalysis
robocopy /S core %output%\core
robocopy /S outputs %output%\outputs
robocopy /S sample_data %output%\sample_data
robocopy /S test %output%\test
robocopy . %output% .gitattributes .gitignore *.ipynb *.py *.json *.md requirements.txt
pause
