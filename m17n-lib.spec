#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
#
Summary:	A multilingual text processing library
#Summary(pl.UTF-8):	-
Name:		m17n-lib
Version:	1.6.2
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://www.m17n.org/m17n-lib-download/%{name}-%{version}.tar.gz
# Source0-md5:	ad889ed85d4c24928e52f9865bc224ce
Source1:	http://www.m17n.org/m17n-lib-download/m17n-docs-%{version}.tar.gz
# Source1-md5:	5b9652fb714772fc7c7946e282ebedb3
Source2:	http://www.m17n.org/m17n-lib-download/m17n-db-%{version}.tar.gz
# Source2-md5:	47a1db5107865a3aed7cd267faf86280
Patch0:		DESTDIR.patch
URL:		http://www.m17n.org/
BuildRequires:	automake
BuildRequires:	localedb-src
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXaw-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	fribidi-devel
BuildRequires:	libotf-devel >= 0.9.4
BuildRequires:	freetype-devel
BuildRequires:	xorg-lib-libXft-devel >= 2.0.0
BuildRequires:	fontconfig-devel
BuildRequires:	gd-devel
BuildRequires:	libxml2-devel
BuildRequires:	anthy-devel
BuildRequires:	ispell
BuildRequires:	libthai-devel
Requires:	ispell
Requires:	m17n-db = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The m17n library is a multilingual text processing library for the C
language.  This library has following features:
  - The m17n library is an open source software.
  - The m17n library for any Linux/Unix applications.
  - The m17n library realizes multilingualization of many aspects of
    applications.
  - The m17n library represents multilingual text as an object named
    M-text.  M-text is a string with attributes called text
    properties, and designed to substitute for string in C.
    Text properties carry any information required to input,
    display and edit the text.
  - The m17n library  supports functions to handle M-texts.
 
m17n is an abbreviation of Multilingualization.

#%description -l pl.UTF-8

%package -n m17n-db
Summary:	Database files for m17n library
Summary(pl.UTF-8):	Baza danych biblioteki m17n
Group:		Development/Libraries

%description -n m17n-db
Database files for m17n library.

%description -n m17n-db -l pl.UTF-8
Baza danych biblioteki m17n.


%package devel
Summary:	Header files for m17n library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki m17n
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for m17n library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki m17n.

%package static
Summary:	Static m17n library
Summary(pl.UTF-8):	Statyczna biblioteka m17n
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static m17n library.

%description static -l pl.UTF-8
Statyczna biblioteka m17n.

%package apidocs
Summary:	m17n API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki m17n
Group:		Documentation

%description apidocs
API and internal documentation for m17n library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki m17n.

%prep
%setup -q -T -c -a0 -a1 -a2

cd m17n-docs-%{version}
%patch0 -p1

%build
cd %{name}-%{version}
%configure \
	--enable-gui \
	%{!?with_static_libs:--disable-static}
%{__make} -j1

cd ../m17n-docs-%{version}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make} -j1

cd ../m17n-db-%{version}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 -C %{name}-%{version} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -j1 -C m17n-docs-%{version} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -j1 -C m17n-db-%{version} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/m17n/docs

%find_lang m17n-db

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}/{AUTHORS,ChangeLog,NEWS,README,TODO}
%attr(755,root,root) %{_bindir}/m17n-conv
%attr(755,root,root) %{_bindir}/m17n-date
%attr(755,root,root) %{_bindir}/m17n-dump
%attr(755,root,root) %{_bindir}/m17n-edit
%attr(755,root,root) %{_bindir}/m17n-view
%attr(755,root,root) %{_libdir}/libm17n*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libm17n*.so.0
%dir %{_libdir}/m17n/
%dir %{_libdir}/m17n/1.0
%{_libdir}/m17n/1.0/lib*.so
%{_mandir}/man1/m17n-conv.1*
%{_mandir}/man1/m17n-date.1*
%{_mandir}/man1/m17n-dump.1*
%{_mandir}/man1/m17n-edit.1*
%{_mandir}/man1/m17n-view.1*

%files -n m17n-db -f m17n-db.lang
%doc m17n-db-%{version}/{AUTHORS,ChangeLog,NEWS,README}
%attr(755,root,root) %{_bindir}/m17n-db
%{_mandir}/man1/m17n-db.1*
%{_mandir}/man5/*.5*
%{_datadir}/m17n
%{_npkgconfigdir}/m17n-db.pc

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/m17n-config
%{_libdir}/libm17n*.so
%{_includedir}/m17n*.h
%{_pkgconfigdir}/m17n*.pc
%{_mandir}/man1/m17n-config.1*
%{_mandir}/man3/*.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libm17n*.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc m17n-docs-%{version}/usr/html
%doc m17n-docs-%{version}/usr/latex/m17n-lib.pdf
%endif
