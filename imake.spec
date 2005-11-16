Summary: imake source code configuration and build system
Name: imake
Version: 0.99.2
Release: 2
License: MIT/X11
Group: User Interface/X
URL: http://www.x.org
%define xorgurl http://xorg.freedesktop.org/releases/X11R7.0-RC1/everything
Source0: %{xorgurl}/imake-%{version}.tar.bz2
Source1: %{xorgurl}/xmkmf-0.99.1.tar.bz2
Source2: %{xorgurl}/xorg-cf-files-%{version}.tar.bz2
Source3: %{xorgurl}/makedepend-%{version}.tar.bz2
Patch0: imake-0.99.2-misc.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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

#Provides: %{pkgname}
#Provides: setxkbmap, xkbcomp, xkbevd, xkbprint, xkbutils
# NOTE: The XFree86, and xorg-x11 packages used to contain the xkb utilities
# in the previous monolithic based releases.  This Conflicts line ensures
# that upgrades are handled properly.
#Conflicts: XFree86, xorg-x11
Provides: imake, xmkmf, makedepend

%description
Imake is a deprecated source code configuration and build system which
has traditionally been supplied by and used to build the X Window System
in X11R6 and previous releases.  As of the X Window System X11R7 release,
the X Window system has switched to using GNU autotools as the primary
build system, and the Imake system is now deprecated, and should not be
used by new software projects.  Software developers are encouraged to
migrate software to the GNU autotools system.

%prep
%setup -q -c %{name}-%{version} -a1 -a2 -a3
%patch0 -p0 -b .imake

%build
# Build everything
{
   for pkg in imake xmkmf xorg-cf-files makedepend ; do
      pushd $pkg-*
      %configure
      make
      popd
   done
}

%install
rm -rf $RPM_BUILD_ROOT

# Install everything
{
   for pkg in imake xmkmf makedepend ; do
      pushd $pkg-*
      %makeinstall
      popd
   done
   pushd xorg-cf-files-%{version}
   make install DESTDIR=$RPM_BUILD_ROOT libdir=%{_datadir}
   popd

}
# FIXME: Move/rename manpages to correct location
{
    ls -al $RPM_BUILD_ROOT%{_mandir}/man1
    mv $RPM_BUILD_ROOT%{_mandir}/man1 $RPM_BUILD_ROOT%{_mandir}/man1x
#    ls -al $RPM_BUILD_ROOT%{_mandir}/man1
    ls -al $RPM_BUILD_ROOT%{_mandir}/man1x
    for each in $RPM_BUILD_ROOT%{_mandir}/man1x/* ; do
        mv $each ${each}x
    done
}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc
%dir %{_bindir}
%{_bindir}/imake
%{_bindir}/makedepend
%{_bindir}/xmkmf
%dir %{_datadir}/X11
%dir %{_datadir}/X11/config
%{_datadir}/X11/config/*.cf
%{_datadir}/X11/config/*.def
%{_datadir}/X11/config/*.rules
%{_datadir}/X11/config/*.tmpl
%dir %{_mandir}
%dir %{_mandir}/man1x
%{_mandir}/man1x/imake.1x*
%{_mandir}/man1x/xmkmf.1x*
%{_mandir}/man1x/makedepend.1x*

%changelog
* Wed Nov 16 2005 Than Ngo <than@redhat.com>
- fix xmkmf to look config files in /usr/share/X11/config
  instead /usr/%%{_lib}/X11/config/
- add host.conf

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Updated to imake-0.99.2, xorg-cf-files-0.99.2, makedepend-0.99.2 from
  X11R7 RC2.

* Thu Nov 10 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Initial build.
