from typing import Optional
import jinja2 as jj2
import pydantic


class Mail_Template:

    def __init__(self, template_folder: pydantic.DirectoryPath = None) -> None:
        self.template_folder = template_folder
        self.env: jj2.Environment = jj2.Environment(
            loader=jj2.FileSystemLoader(self.template_folder),
            autoescape=jj2.select_autoescape())

    def render(self, template_name: str, context: Optional[dict] = {}) -> str:
        self.template = self.env.get_template(template_name)
        return self.template.render(**context)
