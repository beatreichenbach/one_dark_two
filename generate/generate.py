import os
from functools import partial

import toml
from jinja2 import Environment, FileSystemLoader


def opacity(color: str, weight: float) -> str:
    values = color.replace('#', '')
    rgb = tuple(int(values[i:i+2], 16) for i in (0, 2, 4))
    updated_color = '#{:02X}{:02X}{:02X}{:02X}'.format(
        rgb[0], rgb[1], rgb[2], int(weight * 255)
    )
    return updated_color


def mix(color1: str, color2: str, weight: float) -> str:
    values1 = color1.replace('#', '')
    values2 = color2.replace('#', '')
    rgb1 = tuple(int(values1[i:i+2], 16) for i in (0, 2, 4))
    rgb2 = tuple(int(values2[i:i+2], 16) for i in (0, 2, 4))
    mixed_rgb = tuple(
        int((1 - weight) * c1 + weight * c2) for c1, c2 in zip(rgb1, rgb2)
    )
    mixed_color = '#{:02X}{:02X}{:02X}'.format(*mixed_rgb)
    return mixed_color


def render_template(template_path, output_path, variables):
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
    template = env.get_template(template_path)
    rendered_template = template.render(**variables)
    with open(output_path, 'w') as output_file:
        output_file.write(rendered_template)


def main() -> None:
    generate_dir = os.path.dirname(__file__)
    themes_dir = os.path.join(generate_dir, '..', 'src', 'main', 'resources', 'themes')
    palettes_path = os.path.join(generate_dir, 'palettes.toml')

    with open(palettes_path, 'r') as f:
        palettes = toml.load(f)

    for variant, values in palettes.items():
        variables = {
            'name': f'One Dark Two - {variant.title()}',
            'editorScheme': f'/themes/{variant}.xml',
            'parent_scheme': 'Darcula',
            'opacity': partial(mix, values['base']),
            'mix': mix,
            'italics': False,

            'accentColor': values['primary'],
            'secondaryAccentColor': values['secondary'],
            'primaryForeground': values['subtext0'],
            'disabledForeground': values['overlay0'],
            'primaryBackground': values['base'],
            'secondaryBackground': values['surface0'],
            'panelBackground': values['base'],
            'secondaryPanelBackground': values['mantle'],
            'hoverBackground': values['surface0'],
            'selectionForeground': values['subtext1'],
            'selectionBackground': values['surface0'],
            'selectionInactiveBackground': values['base'],
            'borderColor': values['base'],
            'separatorColor': values['base'],
        }
        variables.update(values)

        if not os.path.exists(themes_dir):
            os.makedirs(themes_dir)

        template_path = 'ui.theme.json'
        output_path = os.path.join(themes_dir, f'{variant}.theme.json')
        render_template(template_path, output_path, variables)

        template_path = 'editor.xml'
        output_path = os.path.join(themes_dir, f'{variant}.xml')
        render_template(template_path, output_path, variables)


if __name__ == '__main__':
    main()
