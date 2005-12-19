Summary: imake source code configuration and build system
Name: imake
Version: 1.0.0
Release: 2
License: MIT/X11
Group: User Interface/X
URL: http://www.x.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define xorgurl http://xorg.freedesktop.org/releases/X11R7.0-RC4/everything
Source0: %{xorgurl}/imake-%{version}.tar.bz2
Source1: %{xorgurl}/makedepend-%{version}.tar.bz2
Source2: %{xorgurl}/gccmakedep-1.0.0.tar.bz2
Source3: %{xorgurl}/xorg-cf-files-%{version}.tar.bz2
Source4: %{xorgurl}/lndir-1.0.0.tar.bz2
Patch0: xorg-cf-files-1.0.0-misc.patch
Patch1: xorg-cf-files-1.0.0-ProjectRoot.patch
Patch2: xorg-cf-files-1.0.0-man.patch

BuildRequires: pkgconfig
BuildRequires: xorg-x11-util-macros

# libxkbfile-devel needed for setxkbmap, xkbcomp, xkbevd, xkbprint
#BuildRequires: libxkbfile-devel
# libX11-devel needed for setxkbmap, xkbcomp, xkbevd, xkbprint
#BuildRequires: libX11-devel
# libXaw-devel needed for xkbutils
#BuildRequires: libXaw-devel
# libXt-devel needed for xkbutils
#BuildRequires: libXt-devel
# FIXME: xkbvleds requires libXext, but autotools doesn't check/require it:
# gcc  -O2 -g -march=i386 -mcpu=i686   -o xkbvleds  xkbvleds-xkbvleds.o
# xkbvleds-LED.o xkbvleds-utils.o -lXaw7 -lXmu -lXt -lSM -lICE -lXext -lXpm -lX11 -ldl
# /usr/bin/ld: cannot find -lXext
# libXext-devel needed for xkbutils (from above error)
#BuildRequires: libXext-devel
# FIXME: xkbvleds requires libXext, but autotools doesn't check/require it:
# gcc  -O2 -g -march=i386 -mcpu=i686   -o xkbvleds  xkbvleds-xkbvleds.o
# xkbvleds-LED.o xkbvleds-utils.o -lXaw7 -lXmu -lXt -lSM -lICE -lXext -lXpm -lX11 -ldl
# /usr/bin/ld: cannot find -lXpm
# libXpm-devel needed for xkbutils (from above error)
#BuildRequires: libXpm-devel

# FIXME:
# Obsoletes: <each package the following commands used to be present in>
Provides: ccmakedep cleanlinks gccmakedep imake lndir makedepend makeg
Provides: mergelib mkdirhier mkhtmlindex revpath xmkmf

%description
Imake is a deprecated source code configuration and build system which
has traditionally been supplied by and used to build the X Window System
in X11R6 and previous releases.  As of the X Window System X11R7 release,
the X Window system has switched to using GNU autotools as the primary
build system, and the Imake system is now deprecated, and should not be
used by new software projects.  Software developers are encouraged to
migrate software to the GNU autotools system.

%prep
%setup -q -c %{name}-%{version} -a1 -a2 -a3 -a4
#%patch0 -p0 -b .imake
#%patch1 -p0 -b .ProjectRoot
%patch2 -p0 -b .redhat

%build
# Build everything
{
   for pkg in imake makedepend gccmakedep lndir xorg-cf-files ; do
      pushd $pkg-*
      case $pkg in
         imake|xorg-cf-files)
            %configure --with-config-dir=%{_datadir}/X11/config
            ;;
         *)
            %configure
            ;;
      esac
      make
      popd
   done
}

%install
rm -rf $RPM_BUILD_ROOT

# Install everything
{
   for pkg in imake makedepend gccmakedep lndir xorg-cf-files ; do
      pushd $pkg-*
      case $pkg in
#         xorg-cf-files)
#            make install DESTDIR=$RPM_BUILD_ROOT libdir=%{_datadir}
#            ;;
         *)
            make install DESTDIR=$RPM_BUILD_ROOT
            ;;
      esac
      popd
   done
}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc
%dir %{_bindir}
%{_bindir}/ccmakedep
%{_bindir}/cleanlinks
%{_bindir}/gccmakedep
%{_bindir}/imake
%{_bindir}/lndir
%{_bindir}/makedepend
%{_bindir}/makeg
%{_bindir}/mergelib
%{_bindir}/mkdirhier
%{_bindir}/mkhtmlindex
%{_bindir}/revpath
%{_bindir}/xmkmf
%dir %{_datadir}/X11
%dir %{_datadir}/X11/config
%{_datadir}/X11/config/*.cf
%{_datadir}/X11/config/*.def
%{_datadir}/X11/config/*.rules
%{_datadir}/X11/config/*.tmpl
%dir %{_mandir}
%dir %{_mandir}/man1
%{_mandir}/man1/ccmakedep.1x*
%{_mandir}/man1/cleanlinks.1x*
%{_mandir}/man1/gccmakedep.1x*
%{_mandir}/man1/imake.1x*
%{_mandir}/man1/lndir.1x*
%{_mandir}/man1/makedepend.1x*
%{_mandir}/man1/makeg.1x*
%{_mandir}/man1/mergelib.1x*
%{_mandir}/man1/mkdirhier.1x*
%{_mandir}/man1/mkhtmlindex.1x*
%{_mandir}/man1/revpath.1x*
%{_mandir}/man1/xmkmf.1x*

%changelog
* Mon Dec 19 2005 Than Ngo <than@redhat.com> 1.0.0-2
- add some macros to fix problem in building of manpages

* Sat Dec 17 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated all packages to version 1.0.0 from X11R7 RC4
- Added new lndir, gccmakedep tarballs.
- Changed manpage dirs from man1x to man1 to match upstream RC4 default.
- Removed all previous 'misc' patch, as we now pass --with-config-dir to
  configure to specify the location of the Imake config files.
- Renamed imake patch to xorg-cf-files-1.0.0-ProjectRoot.patch as it did not
  patch imake at all.  This should probably be changed to be a custom Red Hat
  host.def file that is added as a source line instead of randomly patching
  various files.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> 0.99.2-5.1
- rebuilt

* Mon Nov 28 2005 Than Ngo <than@redhat.com> 0.99.2-5
- add correct ProjectRoot for modular X

* Wed Nov 16 2005 Than Ngo <than@redhat.com> 0.99.2-4 
- add missing host.conf

* Wed Nov 16 2005 Than Ngo <than@redhat.com> 0.99.2-3
- fix typo 

* Wed Nov 16 2005 Than Ngo <than@redhat.com> 0.99.2-2
- fix xmkmf to look config files in /usr/share/X11/config
  instead /usr/%%{_lib}/X11/config/
- add host.conf

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Updated to imake-0.99.2, xorg-cf-files-0.99.2, makedepend-0.99.2 from
  X11R7 RC2.

* Thu Nov 10 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Initial build.
