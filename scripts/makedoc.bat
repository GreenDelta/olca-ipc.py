@echo off
rem we use pdoc3 to generate our documentation
rem see https://github.com/pdoc3/pdoc

cd ..

del /s /q doc\*.html
pdoc --html --force --config latex_math=True --output-dir doc olca
cd scripts
