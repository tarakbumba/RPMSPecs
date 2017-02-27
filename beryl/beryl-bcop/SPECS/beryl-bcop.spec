%define debug_package %{nil}

%define	oname		compiz-bcop
%define	shortname	bcop
%define	version		0.8.12
%define	rel			1
%define	git			0

%if  %{git}
%define	srcname		%{shortname}-%{git}.tar.lzma
%define	distname	%{shortname}
%define	release		%mkrel 0.%{git}.%{rel}
%else
%define	srcname		%{oname}-%{version}.tar.xz
%define	distname	%{oname}-%{version}
%define	release		%mkrel %{rel}
%endif

Name:		beryl-bcop
Version:	%{version}
Release:	%{release}
Summary:	BCOP: Beryl/Compiz plugin build utility
Group:		System/X11
URL:		https://github.com/compiz-reloaded/%{oname}
Source:		https://github.com/compiz-reloaded/%{oname}/releases/download/v%{version}/%{srcname}
License:	GPLv2+
BuildRequires:  pkgconfig(libxslt)
Requires:	xsltproc

%description
BCOP: Beryl/Compiz plugin build utility

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

%files
%{_bindir}/%{shortname}
%dir %{_datadir}/%{shortname}
%{_datadir}/%{shortname}/%{shortname}.xslt
%{_datadir}/pkgconfig/%{shortname}.pc

%install
%makeinstall_std


