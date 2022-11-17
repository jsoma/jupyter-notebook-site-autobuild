import frontmatter
from pathlib import Path
import logging
import markdown
import jinja2
import shutil

logging.basicConfig(level=logging.INFO)

template_loader = jinja2.FileSystemLoader(searchpath="templates")
template_env = jinja2.Environment(loader=template_loader)

class Page:

    def __init__(self, path):
        logging.info(f"Loading page at {path}")
        self.path = path
        self.data = frontmatter.load(path)
        self.slug = self.data.get('slug', self.path.stem.lower().replace(" ", "-"))
        self.title = self.data.get('title', self.path.stem)

    def render(self, render_base, nav_links=[]):
        content = markdown.markdown(self.data.content)

        template = template_env.get_template("template.html")
        rendered = template.render(
            title=self.title,
            content=content,
            nav_links=nav_links
        )

        target_path = render_base.joinpath(self.slug).joinpath("index.html")
        target_path.parent.mkdir(parents=True, exist_ok=True)

        logging.info(f"Rendering page to {target_path}")
        target_path.write_text(rendered)

class Site:

    def __init__(self, base_path):
        self.base = Path(base_path)
        logging.info(f"Processing site at {self.base.resolve()}")

        page_files = list(self.base.glob("**/*.md"))
        logging.info(f"Found {len(page_files)} page files")
        self.pages = [Page(path) for path in page_files]

    def render(self, output_path="docs"):
        output_path = Path(output_path)

        # Initialize the site's pages
        self.pages.sort(key=lambda page: page.data.get("position", 999)) 
        nav_links = [{"title": page.title, "slug": page.slug} for page in self.pages]
        for page in self.pages:
            page.render(output_path, nav_links=nav_links)

    def move_statics(self):
        logging.info("Copying statics")
        shutil.rmtree("docs/static", ignore_errors=True)
        shutil.copytree("statics", "docs/statics", dirs_exist_ok=True)

site = Site("content")
site.render()
site.move_statics()