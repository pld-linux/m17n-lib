#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries

%define	doc_ver	1.6.2
Summary:	A multilingual text processing library
Summary(pl.UTF-8):	Biblioteka przetwarzania tekstów wielojęzycznych
Name:		m17n-lib
Version:	1.6.3
Release:	4
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: http://www.m17n.org/m17n-lib-en/download.html
Source0:	http://www.m17n.org/m17n-lib-download/%{name}-%{version}.tar.gz
# Source0-md5:	24c8f0a2fb167e1a0e25815c8421a2a4
Source1:	http://www.m17n.org/m17n-lib-download/m17n-docs-%{doc_ver}.tar.gz
# Source1-md5:	5b9652fb714772fc7c7946e282ebedb3
Source2:	http://www.m17n.org/m17n-lib-download/m17n-db-%{version}.tar.gz
# Source2-md5:	0c4723d0e6f6f5b2e8f40705ad5ab7d3
Patch0:		DESTDIR.patch
URL:		http://www.m17n.org/
BuildRequires:	anthy-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2
BuildRequires:	fribidi-devel
BuildRequires:	gd-devel
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	ispell
BuildRequires:	libotf-devel >= 0.9.4
BuildRequires:	libthai-devel
BuildRequires:	libxml2-devel
BuildRequires:	localedb-src
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXaw-devel
BuildRequires:	xorg-lib-libXft-devel >= 2.0.0
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libXt-devel
Requires:	ispell
Requires:	m17n-db = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The m17n library is a multilingual text processing library for the C
language. This library has following features:
 - The m17n library is an open source software.
 - The m17n library for any Linux/Unix applications.
 - The m17n library realizes multilingualization of many aspects of
   applications.
 - The m17n library represents multilingual text as an object named
   M-text. M-text is a string with attributes called text properties, and
   designed to substitute for string in C. Text properties carry any
   information required to input, display and edit the text.
 - The m17n library supports functions to handle M-texts.

m17n is an abbreviation of Multilingualization.

%description -l pl.UTF-8
Biblioteka m17n jest przeznaczona do przetwarzania tekstów
wielojęzycznych w języku C. Ma następujące cechy:
 - jest oprogramowaniem o otwartych źródłach
 - może być używana przez dowolne aplikacje linuksowe/uniksowe
 - realizuje wielojęzyczność w wielu aspektach i zastosowaniach
 - reprezentuje tekst wielojęzyczny jako obiekt o nazwie M-text (M-text
   to łańcuch z atrybutami będącymi właściwościami tekstu, zaprojektowany
   do podstawienia do dowolnego łańcucha w C. Właściwości tekstu
   przechowują dowolne informacje wymagane przy wprowadzaniu,
   wyświetlaniu i edycji tekstu)
 - obsługuje funkcje przetwarzające M-text.

m17n to skrót od "multilingualization", czyli uwielojęzycznienie.

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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API and internal documentation for m17n library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki m17n.

%package -n m17n-db
Summary:	Database files for m17n library
Summary(pl.UTF-8):	Baza danych biblioteki m17n
Group:		Development/Libraries

%description -n m17n-db
Database files for m17n library.

%description -n m17n-db -l pl.UTF-8
Baza danych biblioteki m17n.

%prep
%setup -q -T -c -a0 -a1 -a2

cd m17n-docs-%{doc_ver}
%patch0 -p1

%build
cd %{name}-%{version}
%configure \
	--enable-gui \
	%{!?with_static_libs:--disable-static}
%{__make} -j1

cd ../m17n-docs-%{doc_ver}
%{__aclocal}
%{__autoconf}
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

%{__make} -j1 -C m17n-docs-%{doc_ver} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -j1 -C m17n-db-%{version} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/m17n/docs

# dlopened modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/m17n/1.0/lib*.{la,a}
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libm17n*.la

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
%attr(755,root,root) %{_libdir}/libm17n.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libm17n.so.0
%attr(755,root,root) %{_libdir}/libm17n-core.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libm17n-core.so.0
%attr(755,root,root) %{_libdir}/libm17n-flt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libm17n-flt.so.0
%attr(755,root,root) %{_libdir}/libm17n-gui.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libm17n-gui.so.0
%dir %{_libdir}/m17n
%dir %{_libdir}/m17n/1.0
%attr(755,root,root) %{_libdir}/m17n/1.0/libm17n-X.so
%attr(755,root,root) %{_libdir}/m17n/1.0/libm17n-gd.so
%attr(755,root,root) %{_libdir}/m17n/1.0/libmimx-anthy.so
%attr(755,root,root) %{_libdir}/m17n/1.0/libmimx-ispell.so
%{_mandir}/man1/m17n-conv.1*
%{_mandir}/man1/m17n-date.1*
%{_mandir}/man1/m17n-dump.1*
%{_mandir}/man1/m17n-edit.1*
%{_mandir}/man1/m17n-view.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/m17n-config
%attr(755,root,root) %{_libdir}/libm17n.so
%attr(755,root,root) %{_libdir}/libm17n-core.so
%attr(755,root,root) %{_libdir}/libm17n-flt.so
%attr(755,root,root) %{_libdir}/libm17n-gui.so
%{_includedir}/m17n*.h
%{_pkgconfigdir}/m17n-core.pc
%{_pkgconfigdir}/m17n-flt.pc
%{_pkgconfigdir}/m17n-gui.pc
%{_pkgconfigdir}/m17n-shell.pc
%{_mandir}/man1/m17n-config.1*
%{_mandir}/man3/m17n*.3*
%{_mandir}/man3/mchar*.3*
%{_mandir}/man3/mconv_*.3*
%{_mandir}/man3/mdatabase_*.3*
%{_mandir}/man3/mdebug_*.3*
%{_mandir}/man3/mdraw_*.3*
%{_mandir}/man3/mface*.3*
%{_mandir}/man3/mflt_*.3*
%{_mandir}/man3/mfont*.3*
%{_mandir}/man3/mframe*.3*
%{_mandir}/man3/minput_*.3*
%{_mandir}/man3/mlocale_*.3*
%{_mandir}/man3/mplist*.3*
%{_mandir}/man3/msymbol*.3*
%{_mandir}/man3/mtext*.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libm17n.a
%{_libdir}/libm17n-core.a
%{_libdir}/libm17n-flt.a
%{_libdir}/libm17n-gui.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc m17n-docs-%{doc_ver}/usr/{html,latex/m17n-lib.pdf}
%endif

%files -n m17n-db -f m17n-db.lang
%defattr(644,root,root,755)
%doc m17n-db-%{version}/{AUTHORS,ChangeLog,NEWS,README}
%attr(755,root,root) %{_bindir}/m17n-db
%{_mandir}/man1/m17n-db.1*
%{_mandir}/man5/mdb*.5*
%{_datadir}/m17n
%{_npkgconfigdir}/m17n-db.pc
