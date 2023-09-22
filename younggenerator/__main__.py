"""Build static HTML site from directory of HTML templates and plain files."""
import pathlib
import json
import sys
import shutil
import click
import jinja2


@click.command()
@click.argument("input_dir", nargs=1, type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(exists=False),
              help="Output directory", metavar="PATH")
@click.option("-v", "--verbose", is_flag=True,
              help="Print more output.", metavar="")
def main(input_dir, output, verbose):
    """Templated static website generator."""
    input_dir = pathlib.Path(input_dir)
    if output:
        output_dir = input_dir/pathlib.Path(output)
    else:
        output_dir = input_dir / "html"
    print(f"DEBUG input_dir={input_dir}")
    config_filename = input_dir / "config.json"
    try:
        data = open_config(config_filename)
    except json.decoder.JSONDecodeError as err:
        sys.exit(f"Error: '{config_filename}'\n{err}")

    # COPY STATIC FILES TO OUTPUT DIRECTORy IF THEY EXIST
    try:
        static_dir = input_dir / "static"
        if static_dir.is_dir:
            shutil.copytree(static_dir, output_dir)
            if verbose:
                print(f"Copied {static_dir} -> {output_dir}")
    except FileNotFoundError:
        pass
    # MAKE OUTPUT DIRECTORY W/ERROR CHECKING IF ALREADY EXISTS
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except FileExistsError as err:
        sys.exit(f"Error: '{output_dir}'\n{err}")

    for item in data:
        url = item["url"].lstrip("/")
        template_name = item["template"]
        context = item["context"]
        # words = item['words']
        template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(input_dir / "templates"),
            autoescape=jinja2.select_autoescape(["html", "xml"]),
        )
        # url = url.lstrip('/')
        try:
            template = template_env.get_template(template_name)
            rendered_template = template.render(url=url, **context)
        except jinja2.exceptions.TemplateError as err:
            sys.exit(f"Error: '{template}'\n{err}")

        # Make output dir for specific Configuration

        output_path = output_dir / url

        try:
            output_path.mkdir(parents=True, exist_ok=True)
        except FileExistsError as err:
            pass

        output_path = output_dir / url / "index.html"
        with output_path.open("w") as output_file:
            output_file.write(rendered_template)
        if verbose:
            print(f"Rendered index.html -> {output_path}")


def open_config(config_filename):
    """Open the config file and returns the data."""
    with config_filename.open() as config_file:
        # config open
        return json.load(config_file)
    # config closed


if __name__ == "__main__":
    main()
