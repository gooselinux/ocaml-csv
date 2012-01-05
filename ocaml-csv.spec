%define opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%define debug_package %{nil}

Name:           ocaml-csv
Version:        1.1.7
Release:        6.2%{?dist}
Summary:        OCaml library for reading and writing CSV files

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://merjis.com/developers/csv
Source0:        http://merjis.com/_file/ocaml-csv-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExcludeArch:    sparc64 s390 s390x

Patch0:         csv-extlib.patch
Patch1:         csv-install.patch

BuildRequires:  ocaml >= 3.10.1
BuildRequires:  ocaml-findlib-devel, ocaml-extlib-devel
BuildRequires:  gawk

%define _use_internal_dependency_generator 0
%define __find_requires /usr/lib/rpm/ocaml-find-requires.sh
%define __find_provides /usr/lib/rpm/ocaml-find-provides.sh

%description
This OCaml library can read and write CSV files, including all
extensions used by Excel - eg. quotes, newlines, 8 bit characters in
fields, quote-0 etc.

The library comes with a handy command line tool called csvtool for
handling CSV files from shell scripts.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p0
%patch1 -p1


%build
#make all
make csv.cma
%if %opt
make csvtool csv.cmxa
strip csvtool
%else
ocamlfind ocamlc -package extlib -linkpkg csv.cma csvtool.ml -o csvtool
%endif


%install
rm -rf $RPM_BUILD_ROOT
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR
mkdir -p $DESTDIR%{_bindir}
make install BINDIR=%{_bindir}

# Create some documentation.
if [ ! -f README ]; then
  cat <<EOM > README
OCaml library for reading and writing CSV files.
For more information, see http://merjis.com/developers/csv .
This library is released under the GNU LGPL + OCaml linking exception.
EOM
fi


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README
%{_libdir}/ocaml/csv
%if %opt
%exclude %{_libdir}/ocaml/csv/*.a
%exclude %{_libdir}/ocaml/csv/*.cmxa
%exclude %{_libdir}/ocaml/csv/*.cmx
%endif
%exclude %{_libdir}/ocaml/csv/*.mli
%{_bindir}/csvtool


%files devel
%defattr(-,root,root,-)
%doc README
%if %opt
%{_libdir}/ocaml/csv/*.a
%{_libdir}/ocaml/csv/*.cmxa
%{_libdir}/ocaml/csv/*.cmx
%endif
%{_libdir}/ocaml/csv/*.mli


%changelog
* Mon Jan 11 2010 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-6.2
- Rebuild against OCaml 3.11.2.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.1.7-6.1
- Rebuilt for RHEL 6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-5
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-3
- Rebuild.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-2
- Rebuild for OCaml 3.11.0

* Mon Oct 27 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-1
- New upstream version 1.1.7.

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-8
- Rebuild for OCaml 3.10.2

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-7
- Rebuild for ppc64.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-6
- Force rebuild for OCaml 3.10.1.

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-5
- Force rebuild because of base OCaml.

* Thu Aug 30 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-4
- Force rebuild because of changed BRs in base OCaml.

* Fri Aug 24 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-3
- License clarified to LGPLv2+ (and fixed/clarified upstream).
- Added ExcludeArch ppc64

* Mon Jun 11 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-2
- Updated to latest packaging guidelines.

* Tue May 29 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-1
- Initial RPM release.
