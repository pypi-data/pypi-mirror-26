from __future__ import print_function, division


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    from numpy.distutils.system_info import get_info
    from os.path import join as osp_join

    config = Configuration('siesta', parent_package, top_path)

    all_info = get_info('ALL')
    sources = [
        'free_unit.f90',
        'write_hsx.f90',
        'read_hsx.f90',
        'read_hs.f90',
        'read_tshs.f90',
        'write_tshs.f90',
        'read_grid.f90',
        'write_grid.f90',
        'write_gf.f90',
    ]
    config.add_extension('_siesta',
                         sources = [osp_join('src', s) for s in sources],
                         extra_info = all_info)
    config.make_config_py()  # installs __config__.py
    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
