%define debug_package %{nil}
%define srcname ubuntu-sounds

Summary:    Ubuntu's GNOME audio theme
Name:       ubuntu-sound-theme
Version:    0.13
Release:    %mkrel 1
Url:        https://www.ubuntu.com
License:    Creative Commons Attribution-ShareAlike
Group:      System/X11
Source0:    https://launchpad.net/ubuntu/+archive/primary/+files/%{srcname}_%{version}.tar.gz
BuildArch:  noarch

Requires:   sound-theme-freedesktop

%description
Sounds to spruce up the Desktop environment

%prep
%autosetup -n %{srcname}-%{version}


%build

%install
mkdir -p %{buildroot}%{_datadir}/sounds

cp -r ubuntu %{buildroot}%{_datadir}/sounds/

%files
%doc COPYING
%{_datadir}/sounds/ubuntu/*




