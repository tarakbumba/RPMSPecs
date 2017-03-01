%define oname emerald
%define major 0
%define libname %mklibname %{name} %major
%define libname_devel %mklibname -d %{name}

%define conflict_libname %mklibname %{oname} %major
%define conflict_libname_devel %mklibname -d %{oname}

Name:               beryl-emerald
Version:            0.8.12.4
Release:            %mkrel 1
Summary:            Window Decorator for Compiz/Beryl
Group:              System/X11
License:            GPLv2+
URL:                https://github.com/compiz-reloaded/%{oname}
Source0:            https://github.com/compiz-reloaded/%{oname}/releases/download/v%{version}/%{oname}-%{version}.tar.xz
Patch0:             emerald-add_beryl_support.patch

BuildRequires:      pkgconfig(gtk+-3.0) >= 3.0.0
BuildRequires:      pkgconfig(libwnck-3.0) >= 3.0.0
BuildRequires:      pkgconfig(beryl) >= 0.8.0
BuildRequires:      desktop-file-utils
BuildRequires:      gettext-devel
BuildRequires:      pkgconfig(uuid)
BuildRequires:      pkgconfig(libberyldecor)
BuildRequires:      pkgconfig(xrender) >= 0.8.4
BuildRequires:      pkgconfig(cairo) >= 1.4
BuildRequires:      pkgconfig(pangocairo)
BuildRequires:      intltool

Requires(post):     desktop-file-utils
Requires(postun):   desktop-file-utils
Requires:           beryl
Provides:           beryl-decorator
Conflicts:          %{oname}

Recommends:         %{name}-themes

%description
Themeable window decorator for the Beryl/Compiz window manager/compositor.

#----------------------------------------------------------------------------

%package -n %libname
Summary:   Library files for %{name}
Group:     System/X11
Requires:  %{name} = %{version}-%{release}
Provides:  %{libname} = %{version}
Conflicts:  %{conflict_libname}

%description -n %{libname}
Emerald Window Decorator for Compiz/Beryl.

This package contains library files for %{name}

#----------------------------------------------------------------------------

%package -n %libname_devel
Group:     Development/C
Summary:   Devel package for %{name}

Requires:  %{name} = %{version}-%{release}
Requires:  %{libname} = %{version}-%{release}
Provides:  %{name}-devel = %{version}
Conflicts:  %{conflict_libname_devel}

%description -n %libname_devel
Emerald - Window Decorator for Compiz/Beryl.

This package contains static libraries and header files needed for development.

#----------------------------------------------------------------------------

%prep
%autosetup -n %{oname}-%{version} -p1

%build
# Patch0 requires this:
NOCONFIGURE=1 ./autogen.sh
%configure2_5x --disable-mime-update \
    --with-gtk=3.0  \
    --with-compositor=beryl

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

%make_build

%install
%make_install

desktop-file-install \
  --vendor="" \
  --add-category="GTK" \
  --dir %{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/*.desktop

mkdir -p %{buildroot}%{_datadir}/mimelnk/application
cat >%{buildroot}%{_datadir}/mimelnk/application/x-%{oname}-theme.desktop <<EOF
[Desktop Entry]
Type=MimeType
Comment=%{oname} Theme
MimeType=application/x-%{oname}-theme
Patterns=*.%{oname}
EOF

rm -rf %{buildroot}%{_libdir}/*.*a
rm -rf %{buildroot}%{_libdir}/%{oname}/engines/*.*a

%find_lang %{oname}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{oname}-theme-manager.desktop

#----------------------------------------------------------------------------

%files -f %{oname}.lang
%doc AUTHORS COPYING NEWS
%{_bindir}/%{oname}*
%{_datadir}/applications/%{oname}-theme-manager.desktop
%dir %{_datadir}/%{oname}
%dir %{_datadir}/%{oname}/theme
%{_datadir}/%{oname}/theme/*
%{_datadir}/%{oname}/settings.ini
%{_datadir}/mime-info/%{oname}.mime
%{_datadir}/mime/packages/%{oname}.xml
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/*/apps/*.svg
%{_datadir}/mimelnk/application/x-%{oname}-theme.desktop
%{_mandir}/man1/*.1.*

%files -n %libname
%{_libdir}/%{oname}/engines/*.so
%{_libdir}/libemeraldengine.so.%{major}{,.*}

%files -n %libname_devel
%dir %{_includedir}/%{oname}
%{_includedir}/%{oname}/*.h
%{_libdir}/lib%{oname}engine.so
%{_libdir}/pkgconfig/%{oname}engine.pc
