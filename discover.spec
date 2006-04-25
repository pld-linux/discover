# TODO
# - shared linking?
# - do sth with source1
# - docbook-to-man isn't present in pld, use sth else?
# - update Group
Summary:	discover - set of libraries and utilities for gathering and reporting information about a system's hardware
Name:		discover - zbiór bibliotek oraz narzêdzi do zbierania oraz raportowania informacji o systemie
Version:	2.0.7
Release:	0.1
License:	GPL
Group:		Applications
Source0:	http://archive.progeny.com/progeny/discover/%{name}-%{version}.tar.gz
# Source0-md5:	49d971828fee06a5d9cde8526ef497ea
Source1:	http://archive.progeny.com/progeny/discover/%{name}-data-2.2005.02.13.tar.gz
# Source1-md5:	6c95ebd652b32d0e0daa546eb3dc4911
URL:		http://platform.progeny.com/discover/
BuildRequires:	curl-devel
BuildRequires:	curl-static
BuildRequires:	db-devel
BuildRequires:	db-static
#BuildRequires:	docbook-utils
BuildRequires:	expat-devel
BuildRequires:	expat-static
BuildRequires:	heimdal-devel
BuildRequires:	heimdal-static
BuildRequires:	libidn-devel
BuildRequires:	libidn-static
BuildRequires:	openssl-devel
BuildRequires:	openssl-static
BuildRequires:	zlib-devel
BuildRequires:	zlib-static
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Discover 2.0 is a cross-platform hardware detection system, using
system-dependent modules (selected at build time) for detecting the
hardware on the system, and provides system-independent interfaces for
querying XML data sources about this hardware. Data files are also
available.

Discover 2.0 is a complete redesign and rewrite of Discover 1.0,
supporting the association of arbitrary data with specific hardware
devices. As an improvement to Discover 1.0, which was limited to
reporting Linux kernel modules and XFree86 server module names,
Discover 2.0 allows the specification of any data (that can be
expressed in XML format) to any software interface.

%package devel
Summary:	Header files for discover library
Summary(pl):	Pliki nag³ówkowe biblioteki discover
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is the package containing the header files for discover library.

%description -l pl devel
Ten pakiet zawiera pliki nag³ówkowe dla biblioteki discover.

%prep
%setup -q -a1

%build
%configure \
	--enable-shared=yes \
	--enable-static=no \

# bad deps. build hack. fails otherwise
%{__make} -C buildtools
%{__make} -C doc \
	DOCBOOKTOMAN=db2man || :
# another bug
%{__make} -C discover discover.o

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf api-reference
mv $RPM_BUILD_ROOT%{_docdir}/discover/api-reference .
rm -rf _doc
mv $RPM_BUILD_ROOT/usr/share/doc/discover _doc

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
mv $RPM_BUILD_ROOT/etc/{init.d/*,rc.d/init.d}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc _doc/*
%{_sysconfdir}/discover-modprobe.conf
%{_sysconfdir}/discover.conf.d/00discover
%attr(754,root,root) /etc/rc.d/init.d/discover
%attr(755,root,root) %{_libdir}/libdiscover.so.*.*.*
%attr(755,root,root) %{_bindir}/discover
%attr(755,root,root) %{_sbindir}/discover-modprobe
%{_mandir}/man1/discover.1*
%{_mandir}/man5/discover-modprobe.conf.5*
%{_mandir}/man5/discover.conf.5*
%{_mandir}/man8/discover-modprobe.8*

%files devel
%defattr(644,root,root,755)
%doc api-reference
%attr(755,root,root) %{_bindir}/discover-config
%attr(755,root,root) %{_bindir}/discover-static
%attr(755,root,root) %{_bindir}/discover-xml
%{_includedir}/discover
%{_libdir}/libdiscover.la
%dir %{_datadir}/discover
%dir %{_datadir}/discover/dtd
%{_datadir}/discover/dtd/conffile.dtd
%{_datadir}/discover/dtd/discover.dtd
%{_mandir}/man1/discover-config.1*
