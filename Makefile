
PYUIC=pyuic5
PFLAGS=

all: ui/main_design.py ui/grid_design.py ui/output_design.py

ui/%_design.py: ui/%.ui
	$(PYUIC) $(PFLAGS) $< -o $@

clean:
	rm ui/*.py
