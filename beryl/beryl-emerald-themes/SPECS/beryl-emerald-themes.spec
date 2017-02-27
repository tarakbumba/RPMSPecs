%define oname emerald-themes


Name:           beryl-%{oname}
Version:		0.8.12.1
Release:		%mkrel 1
Summary:		Themes for Emerald, a window decorator for Compiz/Beryl
Group:			System/X11
License:		GPLv2+
URL:            https://github.com/compiz-reloaded/emerald-themes
Source0:        https://github.com/compiz-reloaded/%{oname}/releases/download/v%{version}/%{oname}-%{version}.tar.xz

BuildArch:      noarch

BuildRequires:  libtool

Requires:       beryl >= 0.8.0
Requires:       beryl-emerald >= 0.8.12.1

%description
Emerald is themeable window decorator for
the Compiz/Beryl window manager/compositor.

This package contains themes for emerald.


%prep
%autosetup -n %{oname}-%{version}

%build
%configure2_5x

%make_build

%install
%make_install

%files
%doc COPYING NEWS
%{_datadir}/emerald/themes/
