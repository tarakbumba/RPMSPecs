%define oname   simple-ccsm

Name:           simple-bcsm
Version:        0.8.12
Release:        %mkrel 1
Summary:        Simple settings manager for Beryl/Compiz
License:        GPLv2+
Group:          System/X11
Url:            https://github.com/compiz-reloaded/simple-ccsm
Source:         %{url}/releases/download/v%{version}/%{oname}-%{version}.tar.xz
BuildArch:      noarch

BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  intltool
BuildRequires:  pkgconfig(python-2.7)
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(beryl) >= 0.8.12
BuildRequires:  pkgconfig(libberylconfig) >= 0.8.12

Requires:       beryl-plugins-main >= 0.8.12
Requires:       bcsm >= 0.8.12
Requires:       python-gobject
Requires:       python-gi-cairo
Recommends:     beryl-plugins-extra >= 0.8.12


%description
Beryl settings manager focused on simplicity for an end-user.


%prep
%autosetup -n %{oname}-%{version}
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
for project in $(grep -rl Compiz); do sed -i "s|Compiz|Beryl|g" $project; done
for project in $(grep -rl decoration); do sed -i "s|decoration|beryldecor|g" $project; done
for project in $(grep -rl gtk-window-decorator); do sed -i "s|gtk-window-decorator|beryl-gtk-decorator|g" $project; done
for project in $(grep -rl ccsm); do sed -i "s|ccsm|bcsm|g" $project; done
for project in $(grep -rl ccm); do sed -i "s|ccm|bcm|g" $project; done

%build
%py2_build -- --prefix=%{_prefix} --enableDesktopEffects --with-gtk=3.0

%install
%py2_install -- --prefix=%{_prefix}

%find_lang %{name} --with-gnome --all-name

%files -f %{name}.lang
%license COPYING
%doc AUTHORS README.md NEWS
%{_bindir}/%{name}
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/appdata/%{name}.appdata.xml
%{python2_sitelib}/simple_bcsm-0.8.12-py%{python2_version}.egg-info
