from __future__ import print_function, division


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('io', parent_package, top_path)
    for sub in ['bigdft', 'gulp', 'scaleup',
                'siesta', 'tbtrans',
                'vasp', 'wannier90']:
        config.add_subpackage(sub)
    config.make_config_py()  # installs __config__.py
    config.add_data_dir('tests')
    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
