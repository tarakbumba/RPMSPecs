%define debug_package %{nil}
%define srcname ubuntu-sounds

Summary:    Ubuntu's GNOME audio theme
Name:       warty-sound-theme
Version:    0.3
Release:    %mkrel 1
Url:        https://www.ubuntu.com
License:    Creative Commons Attribution-ShareAlike
Group:      System/X11
Source0:    http://old-releases.ubuntu.com/ubuntu/pool/main/u/%{srcname}/%{srcname}_%{version}.tar.gz
BuildArch:  noarch
BuildRequires:  vorbis-tools

Requires:   sound-theme-freedesktop

%description
Sounds to spruce up the Desktop environment

%prep
%autosetup -n %{srcname}-%{version}


%build


%install
mkdir -p %{buildroot}%{_datadir}/sounds/ubuntu-warty/stereo

# Move some files to upper directory to ease copying
for file in $(find . -name "*.wav"); do
	oggenc -q3 -o $(dirname $file)/$(basename $file .wav).ogg $file
done

for oggfile in $(find . -name "*.ogg"); do
    cp -f $oggfile %{buildroot}%{_datadir}/sounds/ubuntu-warty/stereo/
done

cat > %{buildroot}%{_datadir}/sounds/ubuntu-warty/index.theme <<EOF
[Sound Theme]
Name=Ubuntu Warty Warthog Sound Theme
Comment=Ubuntu 04.10 Warty Warthog's GNOME audio theme
Directories=stereo

[stereo]
OutputProfile=stereo
EOF

%files
%doc COPYING
%{_datadir}/sounds/ubuntu-warty/*




