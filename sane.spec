%define iscanversion 2.24.0
%define beta	%nil
%define major	1
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} %{major} -d


# All sane backends have SONAME libsane.so.1. We do not want
# sane-backends-iscan to provide libsane.so.1, so filter these out.
%if %{_use_internal_dependency_generator}
%define __noautoprovfiles %{_libdir}/sane
%else
%define _exclude_files_from_autoprov  %{_libdir}/%{name}/
%endif

%define __libtoolize /bin/true

# Setting this makes the /etc/sane.d/dll.conf empty so that scanning apps
# do not search for all existing scanner models which makes their startup
# slow (the user or "scannerdrake" has to insert the names of the really
# installed scanners then)
%define empty_dll_conf 0

%define gphoto2_support 1
%define v4l_support 1
# Switch to disable the compilation of the "primax" backend in case of
# problems
%define primax_support 1
# Switch to disable the compilation of the "epkowa" backend in case of
# problems
%define epkowa_support 1
#ifarch alpha ppc sparc %arm %mips
#define primax_support 0
#define epkowa_support 0
#endif

Summary:	SANE - local and remote scanner access
Name:		sane
Version:	1.0.24
Release:	14
# lib/ is LGPLv2+, backends are GPLv2+ with exceptions
# Tools are GPLv2+, docs are public domain
License: 	GPLv2+ and GPLv2+ with exceptions and Public Domain
Group:		Graphics
Url:		http://www.sane-project.org/
Source0:	https://alioth.debian.org/frs/download.php/file/3958/sane-backends-%{version}.tar.gz
Source3:	http://belnet.dl.sourceforge.net/sourceforge/px-backend/primaxscan-1.1.beta1.tar.bz2
Source5:	saned-xinetd
Source9:	http://heanet.dl.sourceforge.net/sourceforge/hp44x0backend/sane_hp_rts88xx-0.18.tar.bz2
Source10:	http://heanet.dl.sourceforge.net/sourceforge/brother-mfc/sane-driver-0.2.tar.bz2
Source11:	http://www.geocities.com/trsh0101/SANE/primascan.h
Source12:	http://www.geocities.com/trsh0101/SANE/primascan.c
# The free part of Epson's scanner driver package IScan, full package
# downloaded from http://www.avasys.jp/english/linux_e/index.html
# Non-free part stripped out with
# mkdir x; cd x; tar -xvzf ../iscan_2.21.0-6.tar.gz; rm -f */non-free/EAPL*.txt */non-free/lib*.so; tar -cvjf ../iscan_2.21.0-6-free.tar.bz2 *; cd ..; rm -rf x
Source13:	iscan_%{iscanversion}-4-free.tar.bz2
Source14:	http://downloads.sourceforge.net/project/geniusvp2/sane-backend-geniusvp2/1.0.16.1/sane-backend-geniusvp2_1.0.16.1.tar.gz
Source15:	sane.rpmlintrc
Source16:	saned.socket
Source17:	saned.service
Patch1:		sane-backends-1.0.18-plustek-s12.patch
Patch21:	sane-hp_rts88xx-0.18_fix_link.patch
Patch23:	iscan-2.10.0-1_fix_link.patch
Patch26:	iscan-2.20.1-no_non-free_please.diff
Patch27:	iscan-2.20.1-linkage_fix.patch
# (fc) 1.0.19-12mdv fix group for device
Patch28:	sane-backends-1.0.20-group.patch
# (fc) 1.0.20-1mdv primascan build support
Patch29:	sane-backends-1.0.22-primascan.patch
# (fc) list Brother MFC-260C, DCP130C as supported (Mdv bug # 52951)
Patch30:	sane-backends-1.0.20-brother2list.patch
Patch31:	sane-backends-1.0.22-strformat.patch
# Debian patches
# new build system breaks build when using pthreads.
Patch101:       01_missing_pthreads.dpatch
# add back SANE_CAP_ALWAYS_SETTABLE which was mistakenly
# removed from SANE 1.0.20
Patch106:       06_cap_always_settable.dpatch
# Update es translation and add new gl translation, courtesy of
# Use fedora's patch to remove rpath
# Patch to the dll backend to look for pieces of dll.conf inside the
# /etc/sane.d/dll.d/ directory. This is a facility for packages providing
# external backends (like libsane-extras, hpoj and hplip).
Patch113:       22_dll_backend_conf.dpatch
Patch115:       24_sane-desc.c_debian_mods.dpatch

# Fedora patches
Patch202:	sane-backends-1.0.20-open-macro.patch
Patch205:	sane-backends-1.0.20-epson-expression800.patch

Patch206:	xsane-fix-segfault-avahi-fix-kodakio.patch
Patch207:	xsane-network.patch

BuildRequires:	gettext
BuildRequires:	gettext-devel
BuildRequires:	ieee1284-devel
BuildRequires:	libtool-devel
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(avahi-client)
BuildRequires:	avahi-common-devel
%if %{gphoto2_support}
BuildRequires:	pkgconfig(libgphoto2)
%endif
%if %{v4l_support}
BuildRequires:	pkgconfig(libv4l1)
%endif
# ensure resmgr is not pulled
BuildConflicts:	resmgr-devel

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
Group: 		System/Kernel and hardware
License: 	LGPLv2
Summary: 	SANE - local and remote scanner access. This package contains the sane library

%description -n %{libname}
This package contains the shared libraries for %{name}.

%package -n %{devname}
Group: 		Development/C
License:	LGPL
Summary: 	SANE - local and remote scanner access
Requires: 	%{libname} = %{version}-%{release}
Provides:	sane-devel = %{version}-%{release}

%description -n %{devname}
This package contains the headers and development libraries necessary 
to develop applications using SANE.

%package backends
Group:		System/Kernel and hardware
License:	LGPLv2
Summary:	SANE - local and remote scanner access
Provides:	%{name} = %{version}-%{release}
%if %epkowa_support
Suggests:	iscan
%endif

%description backends
This package contains the backends for different scanners.

%if %epkowa_support
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
Group:          System/Kernel and hardware
License:        LGPLv2
Summary:        SANE - local and remote scanner access
Provides:       %{name} = %{version}-%{release}
Provides:	saned = %{version}-%{release}
Requires:	sane-backends >= %{version}-%{release}
Requires:	xinetd
Requires(preun,post):	rpm-helper

%description -n saned
This package contains saned, a daemon that allows remote clients to
access image acquisition devices available on the local host.

%prep
%setup -qn sane-backends-%{version}%{beta}
%patch1 -p1 -b .plusteks12
%patch28 -p1 -b .group
%patch30 -p1 -b .brother2list
%patch31 -p1 -b .strformat

%patch101 -p1
%patch106 -p1
%patch113 -p1
%patch115 -p1

# Fedora patches
%patch202 -p1 -b .open-macro
%patch205 -p1 -b .epson-expression800
%patch206 -p1
%patch207 -p1

# Primax parallel port scanners
%if %{primax_support}
%setup -q -T -D -a 3 -n sane-backends-%{version}%{beta}
%endif

# "primascan" backend 
# (commented out in dll.conf, as it claims to support every USB scanner)
%patch29 -p1 -b .primascan
cat %{SOURCE11} > backend/primascan.h
cat %{SOURCE12} > backend/primascan.c
##perl -p -i -e 's:(BACKENDS=\"):$1primascan :' configure.in
# <mrl> avoid autoconf by applying change to configure too.
##perl -p -i -e 's:(BACKENDS=\"):$1primascan :' configure
##perl -p -i -e 's:(DISTFILES\s*=\s*):$1primascan.h primascan.c :' backend/Makefile.in
echo '#primascan' >> backend/dll.conf.in
autoreconf -fi

# Epson Avasys driver for Epson scanners
%if %{epkowa_support}
%setup -q -T -D -a 13 -n sane-backends-%{version}%{beta}
%endif

# lib64 fixes (avoid patch)
# NOTE: don't regenerate configure script past this line
perl -pi -e "s@/lib(\"|\b[^/])@/%{_lib}\1@g if /LDFLAGS=.*with_ptal/" configure

# Reduce number of retries done by the "snapscan" backend when accessing
# the scanner
perl -p -i -e 's:for \(retries = 20; retries; retries--\):for (retries = 5; retries; retries--):' backend/snapscan-scsi.c

%if %epkowa_support
pushd iscan-%{iscanversion}
%patch23 -p0 -b .iscan-2.10.0-1_fix_link
%patch26 -p0 -b .no_non-free_please
%patch27 -p2 -b .linkage_fix
sed -i -e 's,\[usb\],usb-1.0,g;s,usb_get_busses,libusb_open,g' configure.ac
popd
%endif

# Remove the backend/dll.conf file generated by the patches, it prevents
# the Makefile from generating  the real dll.conf file
rm -f backend/dll.conf


# clang uses newer inline semantics
if echo %__cc |grep -q clang; then
	sed -i -e 's,inline ,,g' primax*/lp.c
fi

%build
CPPFLAGS="`pkg-config --cflags libusb-1.0`" %configure \
	--disable-static \
	--enable-rpath=no \
	--enable-avahi \
	--enable-libusb_1_0 \
%if !%{gphoto2_support}
	--without-gphoto2
%endif

%make

# Primax parallel port scanners
%if %{primax_support}
chmod a+rx tools/sane-config
cd primaxscan*
autoreconf -fi
PATH=`pwd`/../tools:${PATH}
CFLAGS="${RPM_OPT_FLAGS/-ffast-math/} -fPIC -I`pwd`/../include -L`pwd`/../backend/.libs/"\
%configure2_5x \
	--disable-static

%make
%make primax_scan
cd ..
%endif

# Epson Avasys driver for Epson scanners
%if %{epkowa_support}
chmod a+rx tools/sane-config
PATH=`pwd`/tools:${PATH}
cd iscan-%{iscanversion}
sh ./bootstrap
export CFLAGS="${RPM_OPT_FLAGS/-ffast-math/} `pkg-config --cflags libusb-1.0` -I`pwd`/../include -L`pwd`/../backend/ -fPIC"
export CXXFLAGS="${RPM_OPT_FLAGS/-ffast-math/} `pkg-config --cflags libusb-1.0` -I`pwd`/../include -L`pwd`/../backend/ -fPIC"
%configure \
	--disable-static \
	--disable-frontend
%make
cd ..
%endif

%install
%makeinstall_std

# Create missing lock dir
install -d %{buildroot}/var/lib/lock/sane

perl -pi -e "s/installed.*/installed=yes/g" %{buildroot}%{_libdir}/libsane.la
/sbin/ldconfig -n %{buildroot}%{_libdir} %{buildroot}%{_libdir}/sane

# Comment out entry for the "geniusvp2" backend in
# /etc/sane.d/dll.conf as it makes SANE hanging on some systems when
# the appropriate scanner is not present
perl -p -i -e 's/^(\s*geniusvp2)/\#$1/g' %{buildroot}%{_sysconfdir}/sane.d/dll.conf

# Comment out entry for the "epson" backend in /etc/sane.d/dll.conf as
# we have also Epson's "epkowa" backend which supports the same
# scanners
perl -p -i -e 's/^(\s*epson)/\#$1/g' %{buildroot}%{_sysconfdir}/sane.d/dll.conf

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
pushd %{buildroot}/usr/doc/sane-%{version}
#pushd %{buildroot}/usr/doc/sane-1.0.18-cvs
mv `find -mindepth 1 -type d` *.html *.txt %{buildroot}%{_docdir}/sane-backends-doc-%{version}/
mv README README.linux %{buildroot}%{_docdir}/sane-backends-%{version}/
rm -f README.*
mv * %{buildroot}%{_docdir}/sane-backends-%{version}/
popd

# Primax parallel port scanners
%if %{primax_support}
cd primaxscan*
%makeinstall
rm -f %{buildroot}%{_libdir}/libsane-primax.a
mv %{buildroot}%{_libdir}/libsane-primax* %{buildroot}%{_libdir}/sane/
cp primax_scan %{buildroot}%{_bindir}
cd ..
%endif

# Epson Avasys driver for Epson scanners
%if %{epkowa_support}
cd iscan-%{iscanversion}
%makeinstall
rm -f %{buildroot}%{_libdir}/sane/libsane-epkowa.a
rm -f %{buildroot}%{_mandir}/man1/iscan.1*
rm -rf %{buildroot}%{_libdir}/iscan
cp backend/epkowa.conf %{buildroot}%{_sysconfdir}/sane.d/
echo 'epkowa' >> %{buildroot}%{_sysconfdir}/sane.d/dll.conf
cd ..
%endif

# Xinetd.d entry
mkdir %{buildroot}/etc/xinetd.d
cat %{SOURCE5} > %{buildroot}/etc/xinetd.d/saned

# udev rules for libusb user support
mkdir -p %{buildroot}/%{_sysconfdir}/udev/rules.d
install -m644 tools/udev/libsane.rules %{buildroot}/%{_sysconfdir}/udev/rules.d/60-libsane.rules
# Shorten too long comments
perl -p -i -e 's/(\#.{500}).*$/$1 .../' %{buildroot}/%{_sysconfdir}/udev/rules.d/60-libsane.rules

# (tpg) install services
mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE16} %{buildroot}%{_unitdir}/saned.socket
install -m 644 %{SOURCE17} %{buildroot}%{_unitdir}/saned@.service

%find_lang sane-backends

sed -i '/^%dir/d' sane-backends.lang

%pre -n saned
# Add saned to group cdwriter and ub for scanner access.
#/usr/sbin/useradd -r -M -s /bin/false  -c "system user for saned" saned -G cdwriter,usb || :
%_pre_useradd saned /etc/sane.d /bin/false
/usr/sbin/usermod -G cdwriter,usb saned

%files backends -f sane-backends.lang
%doc %{_docdir}/sane-backends-%{version}
%{_bindir}/sane-find-scanner
%{_bindir}/scanimage
%{_bindir}/gamma4scanimage
%if %{primax_support}
%{_bindir}/primax_scan
%endif
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%dir %{_sysconfdir}/sane.d
#config(noreplace) %{_sysconfdir}/sane.d/*[^saned]
%config(noreplace) %{_sysconfdir}/sane.d/*
%{_sysconfdir}/udev/rules.d/*-libsane.rules
%attr(1777,root,root) %dir /var/lib/lock/sane
%if %epkowa_support
# iscan files
%exclude %{_sysconfdir}/sane.d/epkowa.conf
%exclude %{_mandir}/man5/sane-epkowa.5*
%endif

%if %epkowa_support
#-f iscan.lang
%files backends-iscan
%{_libdir}/sane/libsane-epkowa.*
%{_sysconfdir}/sane.d/epkowa.conf
%{_mandir}/man5/sane-epkowa.5*
%dir %{_datadir}/iscan
%{_datadir}/iscan/*
%endif

%files backends-doc
%doc %{_docdir}/sane-backends-doc-%{version}

%files -n %{libname}
%{_libdir}/*.so.%{major}*
%dir %{_libdir}/sane
%{_libdir}/sane/*.so.*
%if %epkowa_support
%exclude %{_libdir}/sane/libsane-epkowa.*
%endif

%files -n %{devname}
%{_bindir}/sane-config
%{_libdir}/*.so
%{_libdir}/sane/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/sane
%if %epkowa_support
%exclude %{_libdir}/sane/libsane-epkowa*
%endif

%files -n saned
%{_sbindir}/*
%{_mandir}/man8/saned*
#config(noreplace) %{_sysconfdir}/sane.d/saned.conf
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/xinetd.d/saned
%{_unitdir}/saned*.s*
