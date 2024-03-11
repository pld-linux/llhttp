#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Node.js llhttp Library
Summary(pl.UTF-8):	Biblioteka llhttp z Node.js
Name:		llhttp
Version:	9.2.0
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/nodejs/llhttp/releases
# source archives: need preparation with "make release" using npm
#   $ install --no-optional --ignore-scripts
#   $ node_modules/.bin/ts-node bin/generate.ts
#   $ make release
#Source0:	https://github.com/nodejs/llhttp/archive/v%{version}/%{name}-%{version}.tar.gz
# already prepared release tarballs, with pregenerated C sources:
Source0:	https://github.com/nodejs/llhttp/archive/release/v%{version}/%{name}-release-v%{version}.tar.gz
# Source0-md5:	50f5549bbf5871aa8ad76eab1f4267ca
URL:		https://llhttp.org/
BuildRequires:	cmake >= 3.5.1
BuildRequires:	gcc >= 5:3.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Node.js llhttp Library - port of http_parser to llparse.

%description -l pl.UTF-8
Biblioteka llhttp z Node.js - port biblioteki http_parser do llparse.

%package devel
Summary:	Header file for llhttp library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki llhttp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header file for llhttp library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki llhttp.

%package static
Summary:	Static llhttp library
Summary(pl.UTF-8):	Statyczna biblioteka llhttp
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static llhttp library.

%description static -l pl.UTF-8
Statyczna biblioteka llhttp.

%prep
%setup -q -n %{name}-release-v%{version}

%build
install -d build
cd build
%cmake .. \
	%{?with_static_libs:-DBUILD_STATIC_LIBS=ON} \
	-DCMAKE_CONFIGURATION_TYPES=fake_to_allow_PLD_build_type \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE-MIT README.md
%attr(755,root,root) %{_libdir}/libllhttp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libllhttp.so.9.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libllhttp.so
%{_includedir}/llhttp.h
%{_libdir}/cmake/llhttp
%{_pkgconfigdir}/libllhttp.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libllhttp.a
%endif
