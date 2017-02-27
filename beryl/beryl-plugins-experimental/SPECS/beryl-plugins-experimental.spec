%define _disable_ld_no_undefined 1
%define	oldname	compiz-plugins-experimental

%define	version	0.8.12
%define	rel		1
%define	git		0

%if %{git}
%define	srcname		plugins-experimental
-%{git}.tar.xz
%define	distname	plugins-experimental

%define	release		%mkrel 0.%{git}.%{rel}
%else
%define	srcname		%{oldname}-%{version}.tar.xz
%define	distname	%{oldname}-%{version}
%define	release		%mkrel %{rel}
%endif

Summary:	Extra Plugin Set for beryl/compiz
Name:		beryl-plugins-experimental
Version:	%{version}
Release:	%{release}
License:    GPLv2+ and MIT
Group:		System/X11
URL:		https://github.com/compiz-reloaded

Source0:	https://github.com/compiz-reloaded/%{oldname}/releases/download/v%{version}/%{srcname}

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
BuildRequires:  pkgconfig(xscrnsaver)

Requires:       beryl
Requires:       beryl-plugins-main

%description
This is the experimental plugin set from the Compiz-Reloaded community.
This is a combination of the Compiz Extras and Beryl communities

%files -f %{name}.lang
%doc COPYING AUTHORS NEWS
%{_libdir}/beryl/lib*.so
%{_datadir}/beryl/*.xml
%{_datadir}/beryl/elements/*.png
%{_datadir}/beryl/elements/*.svg
%{_datadir}/beryl/fireflies/*.png
%{_datadir}/beryl/snow/*.png
%{_datadir}/beryl/stars/*.png

#----------------------------------------------------------------------------

%package	devel
Summary:	Development files for Experimental Plugin Set for compiz/beryl
Group:		Development/X11

%description devel
Development files for Experimental Plugin Set for compiz/beryl

%files devel
%{_includedir}/beryl/*

#----------------------------------------------------------------------------

%prep
%autosetup -n %{distname} -p1

# Rename project to avoid conflicts with compiz > 0.9.0
# This changes file names
find . -depth -name '*compiz*' -execdir bash -c 'mv -i "$1" "${1//compiz/beryl}"' bash {} \;
find . -depth -name '*Compiz*' -execdir bash -c 'mv -i "$1" "${1//Compiz/Beryl}"' bash {} \;
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
%configure2_5x
%make_build

%install
%make_install

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'

%find_lang %{name}

#----------------------------------------------------------------------------
