%global         source_name Flat-Plat

Name:           flat-plat-gtk-theme
Version:        20170323
Release:        %mkrel 1
Summary:        A Material Design-like theme for GNOME/GTK+ based desktop environments
Group:          Graphical desktop/Other
License:        GPLv2+
URL:            https://github.com/nana-4/%{source_name}
Source0:        %{url}/archive/v%{version}.tar.gz#/%{source_name}-%{version}.tar.gz

BuildArch:      noarch

Requires:       gdk-pixbuf2.0
Requires:       gnome-themes-standard
Requires:       gtk-murrine-engine

%description
Flat-Plat is a Material Design-like theme for GNOME/GTK+ based desktop environments.
It supports GTK3, GTK2, Metacity, GNOME Shell, Unity, MATE, LightDM, GDM, Chrome theme, etc.


%prep
%autosetup -n %{source_name}-%{version}

%build


%install
destdir=%{buildroot} ./install.sh


%files
%{_datadir}/themes/%{source_name}*



%changelog
* Sat Mar 25 2017 Atilla ÖNTAŞ <tarakbumba@gmail.com> - 20170323-1.mga6
- Initial import from Laurent Tréguier's copr repository

* Sat Mar 25 2017 Laurent Tréguier <laurent@treguier.org> - 20170323-2
- added glib-compile-resources dependency to fix .gresource files not being built

* Thu Mar 23 2017 Laurent Tréguier <laurent@treguier.org> - 20170323-1
- new version

* Wed Mar 22 2017 Laurent Tréguier <laurent@treguier.org>
- created specfile
