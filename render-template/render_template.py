import jinja2
import os

def render_template(template_file, target_file, template_args):
    env_path = os.path.dirname(template_file)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(env_path), trim_blocks=True, block_start_string='@@',
                            block_end_string='@@', variable_start_string='@=', variable_end_string='=@')
    template = env.get_template(template_file)
    with open(target_file, 'w') as f:
        f.write(template.render(**template_args))
        f.write("\n")  # add a new line for pedantic warnings
