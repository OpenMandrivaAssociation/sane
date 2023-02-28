# sane is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define iscanversion 2.30.4
%define beta %nil
%define major 1
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} %{major} -d
%define lib32name %mklib32name %{name} %{major}
%define dev32name %mklib32name %{name} %{major} -d

%define _disable_lto 1
%define _disable_rebuild_configure 1

# All sane backends have SONAME libsane.so.1. We do not want
# sane-backends-iscan to provide libsane.so.1, so filter these out.
%define _exclude_files_from_autoprov %{_libdir}/%{name}/
%define __libtoolize /bin/true

# Setting this makes the /etc/sane.d/dll.conf empty so that scanning apps
# do not search for all existing scanner models which makes their startup
# slow (the user or "scannerdrake" has to insert the names of the really
# installed scanners then)
%define empty_dll_conf 0

%bcond_without gphoto2
%bcond_without v4l
%ifnarch alpha ppc sparc %{armx}
# Switch to disable the compilation of the "primax" backend in case of
# problems
%bcond_with primax
# Switch to disable the compilation of the "epkowa" backend in case of
# problems
%bcond_with epkowa
%else
%bcond_with primax
# Switch to disable the compilation of the "epkowa" backend in case of
# problems
%bcond_with epkowa
%endif

Summary:	SANE - local and remote scanner access
Name:		sane
Version:	1.1.1
Release:	5
# lib/ is LGPLv2+, backends are GPLv2+ with exceptions
# Tools are GPLv2+, docs are public domain
License: 	GPLv2+ and GPLv2+ with exceptions and Public Domain
Group:		Graphics
Url:		http://www.sane-project.org/
Source0:	https://gitlab.com/sane-project/backends/-/releases/%{version}/sane-backends-%{version}.tar.gz
Source3:	http://belnet.dl.sourceforge.net/sourceforge/px-backend/primaxscan-1.1.beta1.tar.bz2
Source9:	http://heanet.dl.sourceforge.net/sourceforge/hp44x0backend/sane_hp_rts88xx-0.18.tar.bz2
Source10:	http://heanet.dl.sourceforge.net/sourceforge/brother-mfc/sane-driver-0.2.tar.bz2
Source11:	http://www.geocities.com/trsh0101/SANE/primascan.h
Source12:	http://www.geocities.com/trsh0101/SANE/primascan.c
# The free part of Epson's scanner driver package IScan, full package
# downloaded from http://www.avasys.jp/english/linux_e/index.html
# Non-free part stripped out with
# mkdir x; cd x; tar -xvzf ../iscan_2.31.0-1.tar.gz; rm -f */non-free/EAPL*.txt */non-free/lib*.so; tar -cvjf ../iscan_2.31.0-1-free.tar.bz2 *; cd ..; rm -rf x
Source13:	iscan-%{iscanversion}-2-free.tar.bz2
Source14:	http://downloads.sourceforge.net/project/geniusvp2/sane-backend-geniusvp2/1.0.16.1/sane-backend-geniusvp2_1.0.16.1.tar.gz
Source15:	sane.rpmlintrc
Source16:	saned.socket
Source17:	saned@.service.in
Source18:	66-saned.rules
Source19:	saned.sysusers

Patch0:		sane-backends-1.0.18-plustek-s12.patch
# (fc) list Brother MFC-260C, DCP130C as supported (Mdv bug # 52951)
Patch2:		sane-backends-1.0.22-brother2list.patch
Patch3:		sane-backends-1.0.20-strformat.patch
Patch5:		epkowa-compile.patch

# Debian patches
# new build system breaks build when using pthreads.
Patch10:	01_missing_pthreads.dpatch
# add back SANE_CAP_ALWAYS_SETTABLE which was mistakenly
# removed from SANE 1.0.20
Patch11:	06_cap_always_settable.dpatch

# Fedora patches
# (tpg) based on https://src.fedoraproject.org/rpms/sane-backends/raw/rawhide/f/sane-backends-1.0.25-udev.patch
Patch21:	sane-backends-1.0.32-udev.patch
Patch22:	xsane-network.patch

# for iscan source
Patch30:	iscan-2.28.1-fix-preserving-lc_ctype.patch
Patch31:	iscan-2.30.4-fix-link.patch
Patch32:	iscan-2.20.1-no_non-free_please.diff
Patch33:	iscan-2.28.1-linkage_fix.patch

Patch34:	aarch64-io-header.patch

BuildRequires:	autoconf automake autoconf-archive
BuildRequires:	gettext
BuildRequires:	gettext-devel
BuildRequires:	ieee1284-devel
BuildRequires:	libtool-devel
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(avahi-client)
BuildRequires:	avahi-common-devel
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(libxml-2.0)
%if %{with gphoto2}
BuildRequires:	pkgconfig(libgphoto2)
%endif
%if %{with v4l}
BuildRequires:	pkgconfig(libv4l1)
%endif
%if %{with epkowa}
BuildRequires:	autoconf
%endif
# ensure resmgr is not pulled
BuildConflicts:	resmgr-devel
%if %{with compat32}
# BuildRequires:	devel(libintl)
BuildRequires:	devel(libieee1284)
BuildRequires:	devel(libltdl)
BuildRequires:	devel(libjpeg)
BuildRequires:	devel(libtiff)
BuildRequires:	devel(libusb-1.0)
BuildRequires:	devel(libsystemd)
BuildRequires:	devel(libxml2)
BuildRequires:	devel(libudev)
BuildRequires:	devel(libcurl)
BuildRequires:	devel(libv4l2)
%endif

%description
SANE (Scanner Access Now Easy) is a sane and simple interface
to both local and networked scanners and other image acquisition devices
like digital still and video cameras.  SANE currently includes modules for
accessing a range of scanners, including models from Agfa SnapScan, Apple,
Artec, Canon, CoolScan, Epson, HP, Microtek, Mustek, Nikon, Siemens,
Tamarack, UMAX, Connectix, QuickCams and other SANE devices via network.

For the latest information on SANE, the SANE standard definition, and
mailing list access, see http://www.mostang.com/sane/

This package does not enable network scanning by default; if you wish
to enable it, install the saned package.

%package -n %{libname}
Group:		System/Kernel and hardware
License:	LGPLv2
Summary:	SANE - local and remote scanner access. This package contains the sane library

%description -n %{libname}
This package contains the shared libraries for %{name}.

%package -n %{devname}
Group:		Development/C
License:	LGPL
Summary:	SANE - local and remote scanner access
Requires:	%{libname} = %{version}-%{release}
Provides:	sane-devel = %{version}-%{release}

%description -n %{devname}
This package contains the headers and development libraries necessary 
to develop applications using SANE.

%package backends
Group:		System/Kernel and hardware
License:	LGPLv2
Summary:	SANE - local and remote scanner access
Provides:	%{name} = %{version}-%{release}
%if %{with epkowa}
Suggests:	iscan
%endif

%description backends
This package contains the backends for different scanners.

%if %{with epkowa}
%package backends-iscan
Group:		System/Kernel and hardware
License:	LGPLv2
Summary:	SANE - local and remote scanner access
Provides:	iscan = %{iscanversion}

%description backends-iscan
This package contains the iscan backend, in order to not conflict with
manufacturer-supplied packages.
%endif

%package backends-doc
Summary:	Documentation for SANE backends
Group:		System/Kernel and hardware

%description backends-doc
This package contains the SANE backend documentation for different
scanners.

%package -n saned
Group:		System/Kernel and hardware
License:	LGPLv2
Summary:	SANE - local and remote scanner access
Provides:	%{name} = %{version}-%{release}
Provides:	saned = %{version}-%{release}
Requires:	sane-backends >= %{version}-%{release}
%systemd_requires
Requires(pre):	systemd

%description -n saned
This package contains saned, a daemon that allows remote clients to
access image acquisition devices available on the local host.

%if %{with compat32}
%package -n %{lib32name}
Group:		System/Kernel and hardware
License:	LGPLv2
Summary:	SANE - local and remote scanner access. This package contains the sane library (32-bit)

%description -n %{lib32name}
This package contains the shared libraries for %{name}.

%package -n %{dev32name}
Group:		Development/C
License:	LGPL
Summary:	SANE - local and remote scanner access (32-bit)
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}

%description -n %{dev32name}
This package contains the headers and development libraries necessary 
to develop applications using SANE.
%endif

%prep
%setup -qn sane-backends-%{version}

%patch0 -p1 -b .plusteks12
%patch2 -p1 -b .brother2list
%patch3 -p1 -b .strformat

%patch10 -p1 -b .pthread~
%patch11 -p1

# Fedora patches
%patch21 -p1 -b .udev
%patch22 -p1 -b .net

# Primax parallel port scanners
%if %{with primax}
%setup -q -T -D -a 3 -n sane-backends-%{version}
%patch34 -p1
# "primascan" backend
# (commented out in dll.conf, as it claims to support every USB scanner)
cat %{SOURCE11} > backend/primascan.h
cat %{SOURCE12} > backend/primascan.c
##perl -p -i -e 's:(BACKENDS=\"):$1primascan :' configure.in
# <mrl> avoid autoconf by applying change to configure too.
##perl -p -i -e 's:(BACKENDS=\"):$1primascan :' configure
##perl -p -i -e 's:(DISTFILES\s*=\s*):$1primascan.h primascan.c :' backend/Makefile.in
echo '#primascan' >> backend/dll.conf.in
autoreconf -fi
perl -pi -e "s@/lib/@/%_lib/@" primaxscan*/configure
%endif

# Epson Avasys driver for Epson scanners
%if %{with epkowa}
%setup -q -T -D -a 13 -n sane-backends-%{version}
%endif

# lib64 fixes (avoid patch)
# NOTE: don't regenerate configure script past this line
perl -pi -e "s@/lib(\"|\b[^/])@/%{_lib}\1@g if /LDFLAGS=.*with_ptal/" configure

# Reduce number of retries done by the "snapscan" backend when accessing
# the scanner
perl -p -i -e 's:for \(retries = 20; retries; retries--\):for (retries = 5; retries; retries--):' backend/snapscan-scsi.c

%if %{with epkowa}
cd iscan-%{iscanversion}
%patch5 -p2 -b .epkowa~
%patch30 -p0
%patch31 -p0
%patch32 -p0
%patch33 -p2
cd -
%endif

# Remove the backend/dll.conf file generated by the patches, it prevents
# the Makefile from generating  the real dll.conf file
rm -f backend/dll.conf

%if %{with primax}
# clang uses newer inline semantics
if echo %__cc |grep -q clang; then
    sed -i -e 's,inline ,,g' primax*/lp.c
fi
%endif

%build
export CONFIGURE_TOP="$(pwd)"
%if %{with compat32}
mkdir build32
cd build32
CPPFLAGS="$(pkg-config --cflags libusb-1.0)" %configure32 \
	--enable-rpath \
	--enable-libusb_1_0

cd ..
%endif

mkdir build
cd build
CPPFLAGS="$(pkg-config --cflags libusb-1.0)" %configure \
	--disable-static \
	--enable-rpath=no \
	--enable-avahi \
	--enable-libusb_1_0 \
	--with-systemd \
%if !%{with gphoto2}
	--without-gphoto2
%endif

cd ..

%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

# Write udev/hwdb files
_topdir="$PWD"
cd build/tools
./sane-desc -m udev+hwdb -s "${_topdir}/doc/descriptions:${_topdir}/doc/descriptions-external" -d0 > udev/sane-backends.rules
./sane-desc -m hwdb -s "${_topdir}/doc/descriptions:${_topdir}/doc/descriptions-external" -d0 > udev/sane-backends.hwdb
cd -

# Primax parallel port scanners
%if %{with primax}
chmod a+rx build/tools/sane-config
cd primaxscan*
PATH=$(pwd)/../build/tools:${PATH}
CFLAGS="${RPM_OPT_FLAGS/-ffast-math/} -fPIC -I$(pwd)/../build/include -L$(pwd)/../build/backend/.libs/" \
%configure

%make_build
%make_build primax_scan
cd ..
%endif

# Epson Avasys driver for Epson scanners
%if %{with epkowa}
chmod a+rx build/tools/sane-config
PATH=$(pwd)/build/tools:${PATH}
cd iscan-%{iscanversion}
cp -f /usr/share/aclocal/libtool.m4 m4/.
autoreconf -fi
export CFLAGS="${RPM_OPT_FLAGS/-ffast-math/} $(pkg-config --cflags libusb-1.0) -I$(pwd)/../include -L$(pwd)/../build/backend/ -fPIC"
export CXXFLAGS="${RPM_OPT_FLAGS/-ffast-math/} $(pkg-config --cflags libusb-1.0) -I$(pwd)/../include -L$(pwd)/../build/backend/ -fPIC"
export LDFLAGS="${RPM_OPT_FLAGS/-ffast-math/} %{?ldflags} -lusb-1.0"
%configure \
	--disable-static \
	--disable-frontend
%make_build
cd ..
%endif

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

# Create missing lock dir
install -d %{buildroot}/var/lib/lock/sane

perl -pi -e "s/installed.*/installed=yes/g" %{buildroot}%{_libdir}/libsane.la
/sbin/ldconfig -n %{buildroot}%{_libdir} %{buildroot}%{_libdir}/sane

# Comment out entry for the "geniusvp2" backend in
# /etc/sane.d/dll.conf as it makes SANE hanging on some systems when
# the appropriate scanner is not present
perl -p -i -e 's/^(\s*geniusvp2)/\#$1/g' %{buildroot}%{_sysconfdir}/sane.d/dll.conf

# Remove "hpoj" line from /etc/sane.d/dll.con
perl -p -i -e 's/HP\s+OfficeJet/HPLIP/g' %{buildroot}%{_sysconfdir}/sane.d/dll.conf
perl -p -i -e 's/hpoj.sf.net/hplip.sf.net/g' %{buildroot}%{_sysconfdir}/sane.d/dll.conf
perl -p -i -e 's/hpoj/hpaio/g' %{buildroot}%{_sysconfdir}/sane.d/dll.conf

%if %{empty_dll_conf}
# The /etc/sane.d/dll.conf contains lines for every backend, so every
# backend probes for a scanner when a SANE frontend (e. g. xsane) is
# started. With this the user has always to wait around one minute
# before he can scan. We simply replace the file by a nearly empty one
# and let scannerdrake only insert the needed backends. So the
# frontends will start immediately
mv %{buildroot}%{_sysconfdir}/sane.d/dll.conf %{buildroot}%{_sysconfdir}/sane.d/dll.conf.orig
cat > %{buildroot}%{_sysconfdir}/sane.d/dll.conf <<EOF
# enable the next line if you want to allow access through the network:
net
EOF
%endif

# Move documentation from /usr/doc to /usr/share/doc
install -d %{buildroot}%{_docdir}/sane-backends-%{version}/
install -d %{buildroot}%{_docdir}/sane-backends-doc-%{version}/
cd %{buildroot}%{_docdir}/sane-backends
mv $(find -mindepth 1 -type d) *.html *.txt %{buildroot}%{_docdir}/sane-backends-doc-%{version}/
mv README README.linux %{buildroot}%{_docdir}/sane-backends-%{version}/
rm -f README.*
mv * %{buildroot}%{_docdir}/sane-backends-%{version}/
cd -

# Primax parallel port scanners
%if %{with primax}
cd primaxscan*
%make_install
rm -f %{buildroot}%{_libdir}/libsane-primax.a
%if "%{_lib}" == "lib64"
mv %{buildroot}%{_prefix}/lib/sane/libsane-primax* %{buildroot}%{_libdir}/sane/ ||:
rm -rf %{buildroot}%{_prefix}/lib/sane
%endif
cd ..
%endif

# Epson Avasys driver for Epson scanners
%if %{with epkowa}
cd iscan-%{iscanversion}
%make_install
rm -f %{buildroot}%{_libdir}/sane/libsane-epkowa.a
rm -f %{buildroot}%{_mandir}/man1/iscan.1*
rm -rf %{buildroot}%{_libdir}/iscan
cp backend/epkowa.conf %{buildroot}%{_sysconfdir}/sane.d/
echo 'epkowa' >> %{buildroot}%{_sysconfdir}/sane.d/dll.conf
cd ..
%endif

# udev rules for libusb user support
mkdir -p %{buildroot}/%{_sysconfdir}/udev/rules.d
mkdir -p %{buildroot}%{_udevhwdbdir}
install -m 0644 build/tools/udev/sane-backends.rules %{buildroot}%{_sysconfdir}/udev/rules.d/65-sane-backends.rules
install -m 0644 build/tools/udev/sane-backends.hwdb %{buildroot}%{_udevhwdbdir}/20-sane-backends.hwdb

# Shorten too long comments
perl -p -i -e 's/(\#.{500}).*$/$1 .../' %{buildroot}/%{_sysconfdir}/udev/rules.d/65-libsane.rules

# (tpg) install services
mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE16} %{buildroot}%{_unitdir}/saned.socket
install -m 644 %{SOURCE17} %{buildroot}%{_unitdir}/saned@.service
sed -i -e 's|@CONFIGDIR@|%{_sysconfdir}/sane.d|g' %{buildroot}%{_unitdir}/saned@.service
install -Dpm 644 %{SOURCE18} %{buildroot}%{_udevrulesdir}/66-saned.rules
install -Dpm 644 %{SOURCE19} %{buildroot}%{_sysusersdir}/saned.conf

%find_lang sane-backends

sed -i '/^%dir/d' sane-backends.lang

%pre -n saned
%sysusers_create_package %{name} %{SOURCE6}

%post -n saned
%systemd_post saned.socket

%preun -n saned
%systemd_preun saned.socket

%postun -n saned
%systemd_postun_with_restart saned.socket

%files backends -f sane-backends.lang
%doc %{_docdir}/sane-backends-%{version}
%{_bindir}/sane-find-scanner
%{_bindir}/scanimage
%{_bindir}/gamma4scanimage
%if %{with primax}
%{_bindir}/primax_scan
%endif
%{_bindir}/umax_pp
%doc %{_mandir}/man1/*
%doc %{_mandir}/man5/*
%doc %{_mandir}/man7/*
%dir %{_sysconfdir}/sane.d
%config(noreplace) %{_sysconfdir}/sane.d/*
%{_sysconfdir}/udev/rules.d/*.rules
%{_udevrulesdir}/66-saned.rules
%{_udevhwdbdir}/*.hwdb
%{_sysusersdir}/saned.conf
%attr(1777,root,root) %dir /var/lib/lock/sane
%if %{with epkowa}
# iscan files
%exclude %{_sysconfdir}/sane.d/epkowa.conf
%exclude %{_mandir}/man5/sane-epkowa.5*
%endif

%if %{with epkowa}
#-f iscan.lang
%files backends-iscan
%{_libdir}/sane/libsane-epkowa.*
%{_sysconfdir}/sane.d/epkowa.conf
%doc %{_mandir}/man5/sane-epkowa.5*
%doc %{_mandir}/man8/iscan-registry.*
%endif

%files backends-doc
%doc %{_docdir}/sane-backends-doc-%{version}

%files -n %{libname}
%{_libdir}/*.so.%{major}*
%dir %{_libdir}/sane
%{_libdir}/sane/*.so.*
%if %{with epkowa}
%exclude %{_libdir}/sane/libsane-epkowa.*
%endif

%files -n %{devname}
%{_bindir}/sane-config
%{_libdir}/*.so
%{_libdir}/sane/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/sane
%if %{with epkowa}
%exclude %{_libdir}/sane/libsane-epkowa*
%endif

%files -n saned
%{_sbindir}/*
%doc %{_mandir}/man8/saned*
#config(noreplace) %{_sysconfdir}/sane.d/saned.conf
%{_unitdir}/saned*.s*

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/*.so.%{major}*
%{_prefix}/lib/sane/*.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/*.so
%{_prefix}/lib/sane/*.so
%{_prefix}/lib/pkgconfig/*.pc
%endif
