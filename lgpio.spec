%global common_make prefix=%{_prefix} libdir=%{_libdir} mandir=%{_mandir} STRIP=/bin/true
%global upstream_name lg
%global gittag v%{version}

# Broken on v0.1
%bcond_with python

Name:           lgpio
Version:        0.1
Release:        1%{?dist}
Summary:        Linux Single Board Computer GPIO utilities

License:        Unlicense
URL:            http://abyz.me.uk/%{upstream_name}/
Source0:        https://github.com/joan2937/%{upstream_name}/archive/%{gittag}.tar.gz#/%{name}-%{version}.tar.gz

# https://github.com/joan2937/lg/pull/5
Patch1:         lg-0.1-python.patch

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
Requires:       %{name} = %{version}-%{release}

%description devel
lgpio is a library for Linux Single Board Computers (SBC)
which allows control of the General Purpose Input Outputs (GPIO).

Contains development files for C language clients of the library.

%if %{with python}
%package -n python3-%{name}
Summary:        Linux Single Board Computer GPIO module
Requires:       %{name} = %{version}-%{release}
# Borrowed from python-pigpio package
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}

Linux Single Board Computer Python module to access
the General Purpose Input Outputs (GPIO).

%endif

%prep
%autosetup -n %{upstream_name}-%{version} -p1


%build
%set_build_flags
%make_build %{common_make}

%if %{with python}
pushd PY_LGPIO
%py3_build
popd

pushd PY_RGPIO
%py3_build
popd
%endif

%install

%if %{with python}
%make_install %{common_make} PYTHON=%{__python3}
pushd PY_LGPIO
%py3_install
popd
pushd PY_RGPIO
%py3_install
popd
%else

%make_install %{common_make} PYTHON=
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
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/%{name}.py
%{python3_sitelib}/%{name}-%{?pyver_prefix}%{version}-py%{python3_version}.egg-info
%endif

%changelog
* Sun Jan 31 2021 Petr Menšík <pemensik@redhat.com>
- initial build
