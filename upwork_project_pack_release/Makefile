DIST=release

all: clean pdf zip

clean:
	rm -rf $(DIST) && mkdir -p $(DIST)

pdf:
	# Build HTML then convert to PDF (no LaTeX needed)
	pandoc base/*.md    -t html -o $(DIST)/base.html
	pandoc sales/*.md   -t html -o $(DIST)/sales.html
	pandoc content/*.md -t html -o $(DIST)/content.html
	-wkhtmltopdf $(DIST)/base.html    $(DIST)/base.pdf
	-wkhtmltopdf $(DIST)/sales.html   $(DIST)/sales.pdf
	-wkhtmltopdf $(DIST)/content.html $(DIST)/content.pdf

zip:
	zip -r $(DIST)/upwork_project_pack_release.zip base sales content portfolio .vscode Makefile README.md CHANGELOG.md || true
