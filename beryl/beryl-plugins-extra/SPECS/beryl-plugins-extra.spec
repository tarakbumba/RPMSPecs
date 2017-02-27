%define _disable_ld_no_undefined 1
%global plugins     3d addhelper animationaddon bench bicubic crashhandler cubeaddon extrawm fadedesktop firepaint gears grid group loginout maximumize mblur notification reflex scalefilter shelf showdesktop showmouse splash trailfocus wallpaper widget

%define	oldname	compiz-plugins-extra
%define	version	0.8.12.1
%define	rel		1
%define	git		0

%if %{git}
%define	srcname		plugins-extra-%{git}.tar.xz
%define	distname	plugins-extra
%define	release		%mkrel 0.%{git}.%{rel}
%else
%define	srcname		%{oldname}-%{version}.tar.xz
%define	distname	%{oldname}-%{version}
%define	release		%mkrel %{rel}
%endif

Summary:	Extra Plugin Set for beryl/compiz
Name:		beryl-plugins-extra
Version:	%{version}
Release:	%{release}
License:    GPLv2+ and MIT
Group:		System/X11
URL:		https://github.com/compiz-reloaded

Source0:	https://github.com/compiz-reloaded/%{oldname}/releases/download/v%{version}/%{srcname}
Patch0:		0001-Treat-screenlets-windows-as-widgets.patch

BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(beryl)
BuildRequires:  pkgconfig(beryl-animation)
BuildRequires:  gettext-devel
BuildRequires:  intltool
BuildRequires:  beryl-bcop >= 0.7.3
BuildRequires:  pkgconfig(cairo-xlib-xrender)
BuildRequires:  pkgconfig(cairo) >= 1.4
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(libturbojpeg)
BuildRequires:  pkgconfig(libnotify) >= 0.7.0
BuildRequires:  pkgconfig(glu)
BuildRequires:  perl(XML::Parser)
BuildRequires:  pkgconfig(xrender) >= 0.9.3

Requires:       beryl
Requires:       beryl-plugins-main

%description
This is the extra plugin set from the Compiz-Reloaded community.

This is a combination of the Compiz Extras and Beryl communities

%files -f %{name}.lang
%doc COPYING AUTHORS NEWS
%{_libdir}/beryl/*.so
%{_datadir}/beryl/*.xml
%{_datadir}/beryl/*.png

#----------------------------------------------------------------------------

%package	devel
Summary:	Development files for Compiz Fusion Extra Plugin Set for compiz/beryl
Group:		Development/X11

%description devel
Development files for Compiz Fusion Extra Plugin Set for compiz/beryl

%files devel
%{_includedir}/beryl/*
%{_libdir}/pkgconfig/*.pc

#----------------------------------------------------------------------------

%prep
%autosetup -n %{distname} -p1

# Rename project to avoid conflicts with compiz > 0.9.0
# This changes file names
find . -depth -name '*compiz*' -execdir bash -c 'mv -i "$1" "${1//compiz/beryl}"' bash {} \;
#find . -depth -name '*decoration*' -execdir bash -c 'mv -i "$1" "${1//decoration/beryldecor}"' bash {} \;
find . -depth -name '*gtk-window-decorator*' -execdir bash -c 'mv -i "$1" "${1//gtk-window-decorator/beryl-gtk-decorator}"' bash {} \;
find . -depth -name '*ccsm*' -execdir bash -c 'mv -i "$1" "${1//ccsm/bcsm}"' bash {} \;
find . -depth -name '*ccm*' -execdir bash -c 'mv -i "$1" "${1//ccm/bcm}"' bash {} \;
# This changes strings in files
for project in $(grep -rl compiz); do sed -i "s|compiz|beryl|g" $project; done
for project in $(grep -rl COMPIZ); do sed -i "s|COMPIZ|BERYL|g" $project; done
#for project in $(grep -rl decoration); do sed -i "s|decoration|beryldecor|g" $project; done
for project in $(grep -rl gtk-window-decorator); do sed -i "s|gtk-window-decorator|beryl-gtk-decorator|g" $project; done
for project in $(grep -rl ccsm); do sed -i "s|ccsm|bcsm|g" $project; done
for project in $(grep -rl ccm); do sed -i "s|ccm|bcm|g" $project; done



%build
%configure2_5x
%make_build

%install
%make_install

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'

%find_lang %{name}

#----------------------------------------------------------------------------
