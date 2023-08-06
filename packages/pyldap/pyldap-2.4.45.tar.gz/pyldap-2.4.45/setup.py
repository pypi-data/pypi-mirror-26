"""
setup.py - Setup package with the help Python's DistUtils

See https://www.python-ldap.org/ for details.
"""

import sys,os,string,time

has_setuptools = False
try:
  from setuptools import setup, Extension
  has_setuptools = True
except ImportError:
  from distutils.core import setup, Extension

if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    raise Warning('This software is not tested on your version of Python.  Be careful!')
if sys.version_info[0] >= 3 and sys.version_info < (3, 3):
    raise RuntimeError('The C API from Python 3.3+ is required.')

if sys.version_info[0] >= 3:
    from configparser import ConfigParser
    from functools import reduce as reduce_fun
    def string_strip(s):
        return s.strip()
    def string_split(s, *args):
        return s.split(*args)
else:
    from ConfigParser import ConfigParser
    reduce_fun = reduce
    def string_strip(s):
        return string.strip(s)
    def string_split(s, *args):
        return string.split(s, *args)

##################################################################
# Weird Hack to grab release version of python-ldap from local dir
##################################################################
exec_startdir = os.path.dirname(os.path.abspath(sys.argv[0]))
package_init_file_name = reduce_fun(os.path.join,[exec_startdir,'Lib','ldap','__init__.py'])
f = open(package_init_file_name,'r')
s = f.readline()
while s:
  s = string_strip(s)
  if s[0:11]=='__version__':
    version = eval(string_split(s,'=')[1])
    break
  s = f.readline()
f.close()

#-- A class describing the features and requirements of OpenLDAP 2.0
class OpenLDAP2:
  library_dirs = []
  include_dirs = []
  extra_compile_args = []
  extra_link_args = []
  extra_objects = []
  libs = ['ldap', 'lber']
  defines = [ ]
  extra_files = []

LDAP_CLASS = OpenLDAP2

#-- Read the [_ldap] section of setup.cfg
cfg = ConfigParser()
cfg.read('setup.cfg')
if cfg.has_section('_ldap'):
  for name in dir(LDAP_CLASS):
    if cfg.has_option('_ldap', name):
      print(name + ': ' + cfg.get('_ldap', name))
      setattr(LDAP_CLASS, name, string_split(cfg.get('_ldap', name)))

for i in range(len(LDAP_CLASS.defines)):
  LDAP_CLASS.defines[i]=((LDAP_CLASS.defines[i],None))

for i in range(len(LDAP_CLASS.extra_files)):
  destdir, origfiles = string_split(LDAP_CLASS.extra_files[i], ':')
  origfileslist = string_split(origfiles, ',')
  LDAP_CLASS.extra_files[i]=(destdir, origfileslist)

#-- Let distutils/setuptools do the rest
name = 'pyldap'

# Python 2.3.6+ and setuptools are needed to build eggs, so
# let's handle setuptools' additional  keyword arguments to
# setup() in a fashion that doesn't break compatibility  to
# distutils. This still allows 'normal' builds where either
# Python > 2.3.5 or setuptools (or both ;o) are not available.
kwargs = dict()
if has_setuptools:
  kwargs = dict(
    include_package_data = True,
    install_requires = ['setuptools'],
    zip_safe = False,
    python_requires = '>=2.7,!=3.0.*,!=3.1.*,!=3.2.*',
  )

setup(
  #-- Package description
  name = name,
  version = version,
  description = 'Python modules for implementing LDAP clients',
  long_description = """pyldap:
  pyldap is a fork of python-ldap, and provides an object-oriented API to access LDAP
  directory servers from Python programs. Mainly it wraps the OpenLDAP 2.x libs for that purpose.
  Additionally the package contains modules for other LDAP-related stuff
  (e.g. processing LDIF, LDAPURLs, LDAPv3 schema, LDAPv3 extended operations
  and controls, etc.). 
  """,
  author = 'pyldap project',
  url = 'https://github.com/pyldap/pyldap/',
  download_url = 'https://pypi.python.org/pypi/pyldap/',
  classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Operating System :: OS Independent',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Programming Language :: C',

    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    # Note: when updating Python versions, also change .travis.yml and tox.ini

    'Topic :: Database',
    'Topic :: Internet',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: System :: Systems Administration :: Authentication/Directory :: LDAP',
    'License :: OSI Approved :: Python Software Foundation License',
  ],
  license = 'Python style',
  #-- C extension modules
  ext_modules = [
    Extension(
      '_ldap',
      [
        'Modules/LDAPObject.c',
        'Modules/ldapcontrol.c',
        'Modules/common.c',
        'Modules/constants.c',
        'Modules/errors.c',
        'Modules/functions.c',
        'Modules/schema.c',
        'Modules/ldapmodule.c',
        'Modules/message.c',
        'Modules/version.c',
        'Modules/options.c',
        'Modules/berval.c',
      ],
      libraries = LDAP_CLASS.libs,
      include_dirs = ['Modules'] + LDAP_CLASS.include_dirs,
      library_dirs = LDAP_CLASS.library_dirs,
      extra_compile_args = LDAP_CLASS.extra_compile_args,
      extra_link_args = LDAP_CLASS.extra_link_args,
      extra_objects = LDAP_CLASS.extra_objects,
      runtime_library_dirs = (not sys.platform.startswith("win"))*LDAP_CLASS.library_dirs,
      define_macros = LDAP_CLASS.defines + \
        ('ldap_r' in LDAP_CLASS.libs or 'oldap_r' in LDAP_CLASS.libs)*[('HAVE_LIBLDAP_R',None)] + \
        ('sasl' in LDAP_CLASS.libs or 'sasl2' in LDAP_CLASS.libs or 'libsasl' in LDAP_CLASS.libs)*[('HAVE_SASL',None)] + \
        ('ssl' in LDAP_CLASS.libs and 'crypto' in LDAP_CLASS.libs)*[('HAVE_TLS',None)] + \
        [('LDAPMODULE_VERSION', version)]
    ),
  ],
  #-- Python "stand alone" modules
  py_modules = [
    'ldapurl',
    'ldif',
    'dsml',
    'ldap',
    'slapdtest',
    'ldap.async',
    'ldap.compat',
    'ldap.controls',
    'ldap.controls.deref',
    'ldap.controls.libldap',
    'ldap.controls.openldap',
    'ldap.controls.ppolicy',
    'ldap.controls.psearch',
    'ldap.controls.pwdpolicy',
    'ldap.controls.readentry',
    'ldap.controls.sessiontrack',
    'ldap.controls.simple',
    'ldap.controls.sss',
    'ldap.cidict',
    'ldap.dn',
    'ldap.extop',
    'ldap.extop.dds',
    'ldap.filter',
    'ldap.functions',
    'ldap.ldapobject',
    'ldap.logger',
    'ldap.modlist',
    'ldap.resiter',
    'ldap.sasl',
    'ldap.schema',
    'ldap.schema.models',
    'ldap.schema.subentry',
    'ldap.schema.tokenizer',
    'ldap.syncrepl',
  ],
  package_dir = {'': 'Lib',},
  data_files = LDAP_CLASS.extra_files,
  test_suite = 'Tests',
  **kwargs
)
