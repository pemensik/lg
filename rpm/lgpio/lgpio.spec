%global common_make prefix=%{_prefix} libdir=%{_libdir} mandir=%{_mandir} STRIP=/bin/true
%global upstream_name lg
%global gittag v%{version}
#%%global gittag master

%bcond_without python

Name:           lgpio
Version:        0.1
Release:        1%{?dist}
Summary:        Linux Single Board Computer GPIO utilities

License:        Unlicense
URL:            http://abyz.me.uk/%{upstream_name}/
Source0:        https://github.com/joan2937/%{upstream_name}/archive/%{gittag}.tar.gz#/%{upstream_name}-%{version}.tar.gz

# https://github.com/joan2937/lg/pull/5
Patch1:         lg-0.1-python.patch
#Patch1:         0001-Make-python-version-overridable-by-PYTHON-variable.patch
Patch2:         0002-Make-python-lgpiod-buildable-without-install.patch
Patch3:         0003-Move-python-specific-into-PY-subdirectories.patch

BuildRequires:  gcc make
BuildRequires:  sed

%if %{with python}
BuildRequires:  python3-devel python3-setuptools
BuildRequires:  swig
%endif
Requires:       %{name}-libs = %{version}-%{release}

%description
lgpio is a library for Linux Single Board Computers (SBC)
which allows control of the General Purpose Input Outputs (GPIO).

Contains remote shell and daemon for remote host GPIO manipulation.

%package libs
Summary:        Linux Single Board Computer GPIO libraries

%description libs
lgpio is a library for Linux Single Board Computers (SBC)
which allows control of the General Purpose Input Outputs (GPIO).

Contains shared libraries.

%package devel
Summary:        Linux Single Board Computer GPIO development files
Requires:       %{name}-libs = %{version}-%{release}

%description devel
lgpio is a library for Linux Single Board Computers (SBC)
which allows control of the General Purpose Input Outputs (GPIO).

Contains development files for C language clients of the library.

%if %{with python}
%package -n python3-%{name}
Summary:        Linux Single Board Computer GPIO module
Requires:       %{name}-libs = %{version}-%{release}
# Borrowed from python-pigpio package
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}

Linux Single Board Computer Python module to access
the General Purpose Input Outputs (GPIO) on local machine.

%package -n python3-rgpio
Summary:        Linux Single Board Computer GPIO module
Requires:       %{name}-libs = %{version}-%{release}
BuildArch:      noarch
# Borrowed from python-pigpio package
%{?python_provide:%python_provide python3-rgpio}

%description -n python3-rgpio

Linux Single Board Computer Python module to access
the General Purpose Input Outputs (GPIO) via network.

%endif

%prep
%autosetup -n %{upstream_name}-%{version} -p1


%build
%set_build_flags
%make_build %{common_make}

%if %{with python}
# Make python build separate from makefile
for PYDIR in PY_{L,R}GPIO
do
	(cd $PYDIR && %py3_build)
done
%endif

%install

%make_install %{common_make} PYTHON=

%if %{with python}
for PYDIR in PY_{L,R}GPIO
do
	(cd $PYDIR && %py3_install)
done
%else

%endif

%files
%{_bindir}/rgpiod
%{_bindir}/rgs
%{_mandir}/man1/rg*.1*

%files libs
%doc README.md
%license UNLICENCE
%{_libdir}/liblgpio.so.1*
%{_libdir}/librgpio.so.1*

%files devel
%{_includedir}/?gpio*.h
%{_libdir}/lib?gpio.so
%{_mandir}/man3/*gpio.3*

%if %{with python}
%files -n python3-%{name}
%{python3_sitearch}/__pycache__/*
%{python3_sitearch}/%{name}.py
%{python3_sitearch}/_%{name}.*.so
%{python3_sitearch}/%{name}-*-py%{python3_version}.egg-info

%files -n python3-rgpio
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/rgpio.py
%{python3_sitelib}/rgpio-*-py%{python3_version}.egg-info
%endif

%changelog
* Sun Jan 31 2021 Petr Menšík <pemensik@redhat.com>
- initial build
