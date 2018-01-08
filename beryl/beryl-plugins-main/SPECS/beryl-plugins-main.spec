%global plugins      animation colorfilter expo ezoom imgjpeg mag mousepoll neg opacify put resizeinfo ring scaleaddon session shift snap staticswitcher text thumbnail titleinfo vpswitch winrules workarounds

%define	name	beryl-plugins-main
%define	oldname	compiz-plugins-main
%define	version	0.8.14
%define	rel		1
%define	git		0

%if %{git}
%define	srcname		plugins-main-%{git}.tar.xz
%define	distname	plugins-main
%define	release		%mkrel 0.%{git}.%{rel}
%else
%define	srcname		%{oldname}-%{version}.tar.xz
%define	distname	%{oldname}-%{version}
%define	release		%mkrel %{rel}
%endif

Summary:	Compiz Fusion Main Plugin Set for beryl/compiz
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:		System/X11
URL:		https://github.com/compiz-reloaded

Source0:	https://github.com/compiz-reloaded/%{oldname}/releases/download/v%{version}/%{srcname}

BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(beryl-scale)
BuildRequires:  gettext-devel
BuildRequires:  intltool
BuildRequires:  beryl-bcop >= 0.7.3
BuildRequires:  pkgconfig(cairo-xlib-xrender)
BuildRequires:  pkgconfig(cairo) >= 1.4
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(glu)
BuildRequires:  perl(XML::Parser)
BuildRequires:  pkgconfig(xrender) >= 0.9.3

Requires:       beryl

%description
This is the main plugin set from the Compiz Fusion community.

This is a combination of the Compiz Extras and Beryl communities

%files -f %{name}.lang
%{_libdir}/beryl/lib*.so
%{_datadir}/beryl/*.xml
%dir %{_datadir}/beryl/filters
%{_datadir}/beryl/filters/*
%{_datadir}/beryl/*/*.png

#----------------------------------------------------------------------------

%package	devel
Summary:	Development files for Compiz Main Plugin Set for beryl/compiz
Group:		Development/X11

%description devel
Development files for Compiz Main Plugin Set for beryl/compiz

%files devel
%{_includedir}/beryl/*.h
%{_libdir}/pkgconfig/*.pc

#----------------------------------------------------------------------------

%prep
%autosetup -n %{distname}

# Rename project to avoid conflicts with compiz > 0.9.0
# This changes file names
find . -depth -name '*compiz*' -execdir bash -c 'mv -i "$1" "${1//compiz/beryl}"' bash {} \;
find . -depth -name '*decoration*' -execdir bash -c 'mv -i "$1" "${1//decoration/beryldecor}"' bash {} \;
find . -depth -name '*gtk-window-decorator*' -execdir bash -c 'mv -i "$1" "${1//gtk-window-decorator/beryl-gtk-decorator}"' bash {} \;
find . -depth -name '*ccsm*' -execdir bash -c 'mv -i "$1" "${1//ccsm/bcsm}"' bash {} \;
find . -depth -name '*ccm*' -execdir bash -c 'mv -i "$1" "${1//ccm/bcm}"' bash {} \;
# This changes strings in files
for project in $(grep -rl compiz); do sed -i "s|compiz|beryl|g" $project; done
for project in $(grep -rl COMPIZ); do sed -i "s|COMPIZ|BERYL|g" $project; done
for project in $(grep -rl decoration); do sed -i "s|decoration|beryldecor|g" $project; done
for project in $(grep -rl gtk-window-decorator); do sed -i "s|gtk-window-decorator|beryl-gtk-decorator|g" $project; done
for project in $(grep -rl ccsm); do sed -i "s|ccsm|bcsm|g" $project; done
for project in $(grep -rl ccm); do sed -i "s|ccm|bcm|g" $project; done

%build
%if %{git}
  # This is a CVS snapshot, so we need to generate makefiles.
  sh autogen.sh -V
%endif

%configure2_5x

%make_build

%install

%make_install

find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'

%find_lang %{name}
#----------------------------------------------------------------------------
%changelog
* Tue Jan 09 2018 Atilla ÖNTAŞ <tarakbumba@gmail.com> 0.8.14-1
- Update to 0.8.14 version

* Tue Feb 28 2017 Atilla ÖNTAŞ <tarakbumba@gmail.com> 0.8.12.2-1
- Initial package
