%global    core_plugins    blur clone cube fade ini inotify minimize move place png regex resize rotate scale screenshot switcher video water wobbly zoom fs obs commands wall annotate svg matecompat
 
# List of plugins passed to ./configure.  The order is important
 
%global    plugins         core,dbus,beryldecor,fade,minimize,move,obs,place,png,resize,scale,screenshot,svg,switcher,wall

%define oname compiz
%define	version	0.8.12.3
%define	rel		1
%define	git		0

%define	major	0
%define	libname	%mklibname %{name} %major
%define	libname_devel %mklibname -d %{name}

%if %{git}
%define srcname %{oname}-%{git}.tar.xz
%define distname %{oname}-%{git}
%define release %mkrel 0.%{git}.%{rel}
%else
%define srcname %{oname}-%{version}.tar.xz
%define distname %{oname}-%{version}
%define release %mkrel %{rel}
%endif



Name:		beryl
Version:	%{version}
Release:	%{release}
Summary:	OpenGL composite manager
Group:		System/X11
URL:		https://github.com/compiz-reloaded
License:	GPLv2+ and LGPLv2+ and MIT

Source0:	https://github.com/compiz-reloaded/compiz/releases/download/v%{version}/%{srcname}
Source1:	beryl.defaults
Source2:    beryl-manager
Patch0:     Add-Mageia-graphic-to-the-top-of-the-cube.patch

BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libstartup-notification-1.0) >= 0.7
BuildRequires:  pkgconfig(xrender) >= 0.9.3
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(glib-2.0) >= 2.32
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(fuse)
BuildRequires:  pkgconfig(cairo-xlib-xrender)
BuildRequires:  pkgconfig(cairo) >= 1.4
BuildRequires:  pkgconfig(librsvg-2.0) >= 2.14.0
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libwnck-3.0)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(gio-2.0) >= 2.25.0
BuildRequires:  pkgconfig(libmarco-private)
BuildRequires:  pkgconfig(libberylconfig)
BuildRequires:  libtool
BuildRequires:	intltool
BuildRequires:	xsltproc

Requires:	%{libname} = %{version}-%{release}
Requires:	compositing-wm-common
Requires:	beryl-decorator
Recommends: bcsm

Provides:	compositing-wm

%description
beryl is an OpenGL composite manager for Xgl and AIGLX.

%files -f core-files.txt
%doc AUTHORS ChangeLog COPYING.GPL COPYING.LGPL README.md TODO NEWS
%{_bindir}/beryl
%{_bindir}/beryl-decorator
%{_bindir}/beryl-manager
%dir %{_datadir}/beryl
%{_datadir}/beryl/*.png
%{_datadir}/beryl/core.xml
%{_datadir}/beryl/dbus.xml
%{_datadir}/beryl/glib.xml
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/applications/beryl.desktop
%{_datadir}/applications/beryl-start.desktop
%{_datadir}/compositing-wm/%{name}.defaults

#----------------------------------------------------------------------------

%package decorator-gtk
Summary:	GTK window decorator for beryl
Group:		System/X11

Provides:	beryl-decorator = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}

%description decorator-gtk
This package provides a GTK window decorator for the beryl OpenGL
compositing manager.

%files decorator-gtk
%{_bindir}/beryl-gtk-decorator
%{_datadir}/glib-2.0/schemas/org.beryl-0.gwd.gschema.xml

#----------------------------------------------------------------------------
%package -n %libname
Summary:	Shared libraries for beryl
Group:		System/X11
Provides:   beryl-decorator

%description -n %libname
This package provides shared libraries for beryl.

%files -n %libname

%{_libdir}/libberyldecor.so.%{major}{,.*}
%{_libdir}/beryl/libdbus.so
%{_libdir}/beryl/libglib.so

#----------------------------------------------------------------------------

%package -n %libname_devel
Summary:	Development files for beryl
Group:		Development/X11
Provides:	%{name}-devel = %{version}-%{release}

Requires:	%{libname} = %{version}-%{release}
Requires:	pkgconfig(libpng)
Requires:	pkgconfig(xcomposite)
Requires:	pkgconfig(xdamage)
Requires:	pkgconfig(xfixes)
Requires:	pkgconfig(xrandr)
Requires:	pkgconfig(xinerama)
Requires:	pkgconfig(ice)
Requires:	pkgconfig(sm)
Requires:	pkgconfig(libstartup-notification-1.0)
Requires:	pkgconfig(glu)
Requires:	pkgconfig(libxslt)
Requires:	pkgconfig(glib-2.0)


%description -n %libname_devel
This package provides development files for beryl.

%files -n %libname_devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/beryl/
%{_libdir}/libberyldecor.so

#----------------------------------------------------------------------------

%prep
%autosetup -n %{distname} -p1
# Rename project to avoid conflicts with compiz > 0.9.0
find . -depth -name '*compiz*' -execdir bash -c 'mv -i "$1" "${1//compiz/beryl}"' bash {} \;
find . -depth -name '*Compiz*' -execdir bash -c 'mv -i "$1" "${1//Compiz/Beryl}"' bash {} \;
find . -depth -name '*decoration*' -execdir bash -c 'mv -i "$1" "${1//decoration/beryldecor}"' bash {} \;
find . -depth -name '*gtk-window-decorator*' -execdir bash -c 'mv -i "$1" "${1//gtk-window-decorator/beryl-gtk-decorator}"' bash {} \;
for project in $(grep -rl compiz); do sed -i "s|compiz|beryl|g" $project; done
for project in $(grep -rl COMPIZ); do sed -i "s|COMPIZ|BERYL|g" $project; done
for project in $(grep -rl decoration); do sed -i "s|decoration|beryldecor|g" $project; done
for project in $(grep -rl gtk-window-decorator); do sed -i "s|gtk-window-decorator|beryl-gtk-decorator|g" $project; done
for project in $(grep -rl gtk_window_decorator); do sed -i "s|gtk_window_decorator|beryl_gtk_decorator|g" $project; done

%build
%if %{git}
  # This is a CVS snapshot, so we need to generate makefiles.
  sh autogen.sh -V
%endif

%configure2_5x \
    --with-gtk=3.0 \
    --enable-librsvg \
    --enable-gtk \
    --enable-marco \
    --enable-gsettings \
    --enable-menu-entries \
    --with-default-plugins=%{plugins}

%make_build

%install
%make_install

install -D -m644 %{_sourcedir}/beryl.defaults %{buildroot}%{_datadir}/compositing-wm/%{name}.defaults
install -D -m 0755 %{_sourcedir}/beryl-manager %{buildroot}%{_bindir}/beryl-manager

# Fix the paths in the beryl-manager script
sed -i "s|/usr/local|/usr|g" %{buildroot}%{_bindir}/beryl-manager
sed -i "s|/usr/bin|%{_bindir}|g" %{buildroot}%{_bindir}/beryl-manager
sed -i "s|/usr/lib|%{_libdir}|g" %{buildroot}%{_bindir}/beryl-manager

desktop-file-install                              \
    --delete-original                             \
    --dir=%{buildroot}%{_datadir}/applications \
%{buildroot}%{_datadir}/applications/*.desktop

find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'

%find_lang %{name}
 
cat %{name}.lang > core-files.txt
 
for f in %{core_plugins}; do
  echo %{_libdir}/beryl/lib$f.so
  echo %{_datadir}/beryl/$f.xml
done >> core-files.txt

# After project renaming decor plugin needs attention
echo %{_libdir}/beryl/libberyldecor.so >> core-files.txt
echo %{_datadir}/beryl/beryldecor.xml >> core-files.txt
#----------------------------------------------------------------------------
