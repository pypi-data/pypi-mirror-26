Name: libsmraw
Version: 20171105
Release: 1
Summary: Library to access the storage media (SM) (split) RAW format
Group: System Environment/Libraries
License: LGPL
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libsmraw
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
             
             

%description
Library to access the storage media (SM) (split) RAW format

%package devel
Summary: Header files and libraries for developing applications for libsmraw
Group: Development/Libraries
Requires: libsmraw = %{version}-%{release}

%description devel
Header files and libraries for developing applications for libsmraw.

%package python
Summary: Python 2 bindings for libsmraw
Group: System Environment/Libraries
Requires: libsmraw = %{version}-%{release} python
BuildRequires: python-devel

%description python
Python 2 bindings for libsmraw

%package python3
Summary: Python 3 bindings for libsmraw
Group: System Environment/Libraries
Requires: libsmraw = %{version}-%{release} python3
BuildRequires: python3-devel

%description python3
Python 3 bindings for libsmraw

%package tools
Summary: Several tools for reading and writing storage media (SM) (split) RAW files
Group: Applications/System
Requires: libsmraw = %{version}-%{release} openssl fuse-libs 
BuildRequires: openssl-devel fuse-devel 

%description tools
Several tools for reading and writing storage media (SM) (split) RAW files

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python2 --enable-python3
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.so.*

%files devel
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README ChangeLog
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/libsmraw.pc
%{_includedir}/*
%{_mandir}/man3/*

%files python
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%{_libdir}/python2*/site-packages/*.a
%{_libdir}/python2*/site-packages/*.la
%{_libdir}/python2*/site-packages/*.so

%files python3
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.la
%{_libdir}/python3*/site-packages/*.so

%files tools
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sun Nov  5 2017 Joachim Metz <joachim.metz@gmail.com> 20171105-1
- Auto-generated

