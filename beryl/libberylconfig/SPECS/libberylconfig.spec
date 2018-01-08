%define oname       libcompizconfig
%define	shortname	berylconfig
%define	version		0.8.14
%define	rel			1
%define	git			0

%define	major			0
%define	libname			%mklibname %shortname %major
%define	libname_devel	%mklibname -d %shortname

%if  %{git}
%define srcname %{oname}-%{git}.tar.xz
%define distname %{oname}
%define release %mkrel 0.%{git}.%{rel}
%else
%define srcname %{oname}-%{version}.tar.xz
%define distname %{oname}-%{version}
%define release %mkrel %{rel}
%endif


Summary:	Backend configuration library for Beryl/Compiz
Name:		libberylconfig
Version:	%{version}
Release:	%{release}
# backends/libini.so is GPLv2+, other parts are LGPLv2+
License:     LGPLv2+ and GPLv2+
Group:		System/X11
URL:		https://github.com/compiz-reloaded

Source0:	https://github.com/compiz-reloaded/%{oname}/releases/download/v%{version}/%{srcname}

BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(beryl) >= %{version}
BuildRequires:	gettext-devel
BuildRequires:	intltool
BuildRequires:	pkgconfig(protobuf)
BuildRequires:  perl(XML::Parser)
BuildRequires:  pkgconfig(glu)

%description
Backend configuration library from Beryl/Compiz

#----------------------------------------------------------------------------

%package -n %libname
Summary:	Backend configuration library from Beryl/Compiz
Group:		System/X11
Provides:	%{name} = %{version}-%{release}

%description -n %libname
Backend configuration library from Beryl/Compiz

%files -n %libname
%{_libdir}/%{name}.so.%{major}*

#----------------------------------------------------------------------------

%package common
Summary:	Common files for libberylconfig
Group:		System/X11
Provides:	%{shortname}-common = %{version}-%{release}

%description common
Common files for libberylconfig

%files common
%dir %{_sysconfdir}/%{shortname}
%{_sysconfdir}/%{shortname}/config
%{_libdir}/beryl/libccp.so
%{_libdir}/%{shortname}/backends/libini.so
%{_datadir}/beryl/ccp.xml

#----------------------------------------------------------------------------

%package -n %libname_devel
Summary:	Development files for libberylconfig
Group:		Development/X11
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %libname_devel
Development files for libberylconfig

%files -n %libname_devel
%dir %{_includedir}/%{shortname}
%{_includedir}/%{shortname}/ccs.h
%{_includedir}/%{shortname}/ccs-backend.h
%{_libdir}/beryl/libccp.a
%{_libdir}/%{shortname}/backends/libini.a
%{_libdir}/%{name}.a
%{_libdir}/%{name}.so
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
  # This is a git snapshot, so we need to generate makefiles.
  sh autogen.sh -V
%endif
%configure2_5x

#needed to avoid undefined libs at link time (--no-undefined related)
%make_build LDFLAGS="-ldl $LDFLAGS"

%install
%make_install
find %{buildroot} -name *.la -exec rm -f {} \;
#----------------------------------------------------------------------------
