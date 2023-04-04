Name: gsl
Version: 2.7
Release: 1
Summary: The GNU Scientific Library for numerical analysis
URL: http://www.gnu.org/software/gsl/
License: GPLv3 and GFDL-1.3-or-later and BSD
Source: ftp://ftp.gnu.org/gnu/gsl/%{name}-%{version}.tar.gz

Patch0: gsl-test.patch

BuildRequires: gcc pkgconfig

%description
The GNU Scientific Library (GSL) is a collection of routines for
numerical analysis, written in C.

%package devel
Summary: Libraries and the header files for GSL development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Requires: pkgconfig, automake

%description devel
The gsl-devel package contains the header files necessary for
developing programs using the GSL (GNU Scientific Library).

%package_help

%prep
%autosetup -n %{name}-%{version} -p1
iconv -f windows-1252 -t utf-8 THANKS  > THANKS.aux
touch -r THANKS THANKS.aux
mv THANKS.aux THANKS

%build
# disable FMA
%ifarch aarch64 loongarch64
export CFLAGS="$RPM_OPT_FLAGS -ffp-contract=off"
%endif
%configure
%{make_build}

%check
make check || ( cat */test-suite.log && exit 1 )

%install
%{make_install}
# remove unpackaged files from the buildroot
%install_info_rm
%delete_la_and_a

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
if [ -f %{_infodir}/gsl-ref.info.gz ]; then
    /sbin/install-info %{_infodir}/gsl-ref.info %{_infodir}/dir || :
fi

%preun devel
if [ "$1" = 0 ]; then
    if [ -f %{_infodir}/gsl-ref.info.gz ]; then
	/sbin/install-info --delete %{_infodir}/gsl-ref.info %{_infodir}/dir || :
    fi
fi

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_libdir}/libgsl.so.25*
%{_libdir}/libgslcblas.so.0*
%{_bindir}/gsl-histogram
%{_bindir}/gsl-randist

%files devel
%{_bindir}/gsl-config*
%{_datadir}/aclocal/*
%{_includedir}/*
%{_infodir}/*info*
%{_libdir}/*.so
%{_libdir}/pkgconfig/gsl.pc

%files help
%{_mandir}/man1/gsl-histogram.1*
%{_mandir}/man1/gsl-randist.1*
%{_mandir}/man1/gsl-config.1*
%{_mandir}/man3/*.3*

%changelog
* Sat Feb 04 2023 wenchaofan <349464272@qq.com> - 2.7-1
- Update to 2.7 version

* Wed Dec 07 2022 xu_ping <xuping33@h-partners.com> - 2.4-10
- Adaptation Loongarch

* Fri Feb 14 2020 fengbing <fengbing7@huawei.com> - 2.4-9
- Package init
