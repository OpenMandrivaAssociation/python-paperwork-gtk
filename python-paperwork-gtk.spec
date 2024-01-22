%global module paperwork-gtk

Summary:	Paperwork's GTK interface
Name:		python-paperwork-gtk
Version:	2.2.0
Release:	1
License:	GPL-3.0-or-later
Group:		Development/Python
URL:		https://pypi.org/project/paperwork-gtk/
Source0:	https://pypi.org/packages/source/p/%{module}/%{module}-%{version}.tar.gz
Patch0:		python-paperwork-gtk-2.2.0-fix_version_path.patch
BuildRequires:	/usr/bin/xvfb-run
BuildRequires:	python%{pyver}dist(distro)
BuildRequires:	python%{pyver}dist(openpaperwork-core)
BuildRequires:	python%{pyver}dist(openpaperwork-gtk)
BuildRequires:	python%{pyver}dist(paperwork-backend)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(pycountry)
BuildRequires:	python%{pyver}dist(pygobject)
BuildRequires:	python%{pyver}dist(pyocr)
BuildRequires:	python%{pyver}dist(python-levenshtein)
BuildRequires:	python%{pyver}dist(pyxdg)

Requires:	tesseract-osd
Requires:	typelib(Libinsane)

BuildArch:	noarch

Provides:	paperwork
Provides:	python-paperwork

%description
Paperwork is a personal document manager. It manages scanned documents 
and PDFs.

It's designed to be easy and fast to use. The idea behind Paperwork is
"scan & forget": You can just scan a new document and forget about it
until the day you need it again.

In other words, let the machine do most of the work for you.

This package provides the GTK frontend for paperwork.

%files
%doc README.markdown
%{_bindir}/paperwork-gtk
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_metainfodir}/*.appdata.xml
%{py_sitedir}/paperwork_gtk
%{py_sitedir}/paperwork_gtk-*.*-info

#-----------------------------------------------------------------------

%prep
%autosetup -p1 -n paperwork-gtk-%{version}

# relax version request for pyocr
sed -i -e 's,pyocr >= 0.3.0,pyocr,g' pyproject.toml

%build
%py_build

%install
%py_install

PYTHONPATH=%{buildroot}%{python_sitelib} \
	xvfb-run -a \
		%{__python} -m paperwork_gtk.main install \
			--data_base_dir %{buildroot}%{_datadir} \
			--icon_base_dir %{buildroot}%{_datadir}/icons

%check
export PATH=%{buildroot}%{_bindir}:$PATH
export PYTHONPATH=%{buildroot}%{python_sitelib}:$PYTHONPATH

xvfb-run -a paperwork-gtk chkdeps
#xvfb-run -a %{python} -m unittest discover --verbose -s tests

