%if 0%{?fedora}
%global with_python3 1
%endif

# disable debuginfo
%define debug_package %{nil}
%define pkgname anytemplate

Name:           python-%{pkgname}
Version:        0.1.3
Release:        1%{?dist}
Summary:        A python template abstraction layer module
Group:          Development/Tools
License:        MIT
URL:            https://github.com/ssato/%{name}
#Source0:        https://github.com/ssato/%%{name}/tarball/master/%%{name}-%%{version}.tar.gz
Source0:        %{pkgname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-setuptools
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-anyconfig
Requires:       PyYAML
%if 0%{?with_python3}
Requires:       python3-jinja2
Requires:       python3-anyconfig
Requires:       python3-PyYAML
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
A template abstraction layer module for python.

%if 0%{?with_python3}
%package -n python3-%{pkgname}
Summary:        A python template abstraction layer module
Group:          Development/Tools

%description -n python3-%{pkgname}
A template abstraction layer module for python.

This is a version for python-3.x.
%endif

%prep
%setup -q -n %{pkgname}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT%{_bindir}/anytemplate_cli $RPM_BUILD_ROOT%{_bindir}/py3anytemplate_cli
popd
%endif
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README.rst examples
%{_bindir}/anytemplate_cli
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n python3-%{pkgname}
%defattr(644,root,root,755)
%doc README.rst examples
%attr(755,root,root) %{_bindir}/py3anytemplate_cli
%{python3_sitelib}/*
%endif

%changelog
* Sat Nov 18 2017 Satoru SATOH <ssato@redhat.com> - 0.1.3-1
- fix: make it runnable even if locale is not set such like in docker env
- fix: some warnings such as deprecated-method, no-else-return and invalid-name

* Sun Oct 29 2017 Satoru SATOH <ssato@redhat.com> - 0.1.2-1
- fix: remove macro expansion in the comment line in this RPM SPEC
- fix: remove duplicated buildarch lines in this RPM SPEC

* Tue Apr 25 2017 Satoru SATOH <ssato@redhat.com> - 0.1.1-1
- fix: follow API changes in anyconfig; anyconfig.to_container was deprecated
  and removed, etc.
- change: move test cases under tests/
- various small bug fixes and refactorings

* Wed Nov  9 2016 Satoru SATOH <ssato@redhat.com> - 0.1.0-1
- add schema file support if anyconfig >=0.0.10 is installed
- add python 3.5 support
- fix: make cheetah (dummy) engine works for python 3.x even if it's not
  available
- enhancement: implement basic renders method to tenjin module
- fix: encode str to byte correctly (especially for python 3.x)
- fix: follow API changes in python-anyconfig >= 0.5.0
- fix: initialize ctx even if options.cotentxs was empty
- some more minor fixes, refactorings and enhancements
- jumped up the version as it may be in stable enough

* Tue Jun 16 2015 Satoru SATOH <ssato@redhat.com> - 0.0.5-1
- fix bugs that template engine specific keyword options are not correctly
  processed in jinja2 and cheetah modules
- fix a lot of potential issues found by pylint and flake8
- make pep8/flake8 ignoring 'module level import not at top of file' error"
- various small bug fixes and refactorings

* Wed Jun  3 2015 Satoru SATOH <ssato@redhat.com> - 0.0.4-1
- fix a bug that _render cannot render alternate template passed by user
- [engines.jinja2] fix a bug that jinja2's exception while fetching template
  but failed is not caught
- fix a few bugs around the code to compute template search paths
- fix a bug that _render cannot render alternate template passed by user
- various small bug fixes and refactorings

* Tue May 12 2015 Satoru SATOH <ssato@redhat.com> - 0.0.3-1
- Changed the license from BSD to MIT as it's easier to understand
- Added an API to list available template engines
- Added mako support which was accidentally not in the supported engines list
- Added pystache support
- Various fixes and enhancements for warnings/errors/comments from flake8,
  pylint and other code inspection tools

* Sun May 10 2015 Satoru SATOH <ssato@redhat.com> - 0.0.2-1
- Fix a bug that the CLI tool does not work

* Fri May  1 2015 Satoru SATOH <ssato@redhat.com> - 0.0.1-1
- Initial packaging
