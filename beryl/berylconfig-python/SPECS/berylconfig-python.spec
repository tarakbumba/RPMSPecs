%define oldname     compizconfig-python
%define	shortname	berylconfig

%define	version		0.8.12.1
%define	rel			1
%define	git			0

%define	libname	%mklibname %name
%define	libname_devel	%mklibname -d %name

%if %{git}
%define	srcname		%{oldname}-%{git}.tar.xz
%define	distname	%{oldname}
%define	release		%mkrel 0.%{git}.%{rel}
%else
%define	srcname		%{oldname}-%{version}.tar.xz
%define	distname	%{oldname}-%{version}
%define	release		%mkrel %{rel}
%endif

Name:		berylconfig-python
Version:	%{version}
Release:	%{release}
Summary:	Python bindings for libberylconfig
Group:		System/X11

URL:		https://github.com/compiz-reloaded
Source0:	https://github.com/compiz-reloaded/%{oldname}/releases/download/v%{version}/%{srcname}
License:	LGPLv2+

BuildRequires:	pkgconfig(beryl)
BuildRequires:	pkgconfig(libberylconfig)
BuildRequires:	pkgconfig(python-2.7)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	python-cython

%description
Python bindings for libberylconfig

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Library files for %{name}
Group:		System/X11

Provides:	%{name} = %{version}-%{release}
Requires:	libberylconfig-common

%description -n %libname
Python Bindings for Compiz/Beryl Settings

%files -n %{libname}
%{py_platsitedir}/%{shortname}.so

#----------------------------------------------------------------------------

%package -n %{libname_devel}
Summary:	Development files from %{name}
Group:		Development/Other

Requires:	%{libname} = %{version}-%{release}
Requires:	libberylconfig-devel
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{libname_devel}
Development files relating to the Python Bindings for Compiz/Beryl Settings

%files -n %{libname_devel}
%{_libdir}/pkgconfig/%{name}.pc

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
  # This is a GIT snapshot, so we need to generate makefiles.
  sh autogen.sh -V
%endif
%configure2_5x
%make_build

%install
%make_install
find %{buildroot} -name *.la -exec rm -f {} \;
find %{buildroot} -name *.a -exec rm -f {} \;

#----------------------------------------------------------------------------
