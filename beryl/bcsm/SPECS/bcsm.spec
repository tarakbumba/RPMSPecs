%define oldname ccsm
%define version 0.8.12.4
%define rel 1
%define git 0

%if  %{git}
%define srcname %{oldname}-%{git}.tar.xz
%define distname %{oldname}
%define release %mkrel 0.%{git}.%{rel}
%else
%define srcname %{oldname}-%{version}.tar.xz
%define distname %{oldname}-%{version}
%define release %mkrel %{rel}
%endif

Name:       bcsm
Version:    %version
Release:    %release
Summary:    Beryl/Compiz Config Settings Manager
License:    GPLv2+
Group:      System/X11
URL:	    https://github.com/compiz-reloaded
BuildArch:  noarch
Source0:    https://github.com/compiz-reloaded/%{oldname}/releases/download/v%{version}/%{srcname}

BuildRequires:  pkgconfig(python-2.7)
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  desktop-file-utils
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

Requires: berylconfig-python
Requires: python-gobject
Requires: python-cairo
Requires: pango


%description
Configuration tool for Compiz/Beryl when used with the ccp configuration plugin (default).

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
for project in $(grep -rl Compiz); do sed -i "s|Compiz|Beryl|g" $project; done
for project in $(grep -rl decoration); do sed -i "s|decoration|beryldecor|g" $project; done
for project in $(grep -rl gtk-window-decorator); do sed -i "s|gtk-window-decorator|beryl-gtk-decorator|g" $project; done
for project in $(grep -rl ccsm); do sed -i "s|ccsm|bcsm|g" $project; done
for project in $(grep -rl ccm); do sed -i "s|ccm|bcm|g" $project; done


%build
%py2_build --with-gtk=3.0

%install
# py2_install macro won't work
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

desktop-file-install \
  --vendor="" \
  --remove-category="Beryl" \
  --add-category="GTK" \
  --add-category="Settings" \
  --add-category="DesktopSettings" \
  --add-category="X-MandrivaLinux-CrossDesktop" \
  --dir %{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/%{name}.desktop
  
%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS COPYING VERSION
%{_bindir}/bcsm
%{_datadir}/appdata/bcsm.appdata.xml
%{_datadir}/applications/bcsm.desktop
%dir %{_datadir}/bcsm
%{_datadir}/bcsm/*
%{_datadir}/icons/hicolor/*/apps/bcsm.*
%dir %{python2_sitelib}/bcm
%{python2_sitelib}/bcm/*
%{python2_sitelib}/bcsm-%{version}-py?.?.egg-info


