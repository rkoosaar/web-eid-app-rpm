%global _hardened_build 1
%define debug_package %{nil}

Name: web-eid
Version: 2.6.0
Release: 1%{?dist}
Summary: Web eID
License: MIT
URL: https://github.com/web-eid/web-eid-app
Source0: %{name}-%{version}.tar.gz

BuildRequires: cmake >= 3.13
BuildRequires: gcc-c++
BuildRequires: desktop-file-utils
BuildRequires: git
BuildRequires: openssl-devel
BuildRequires: pcsc-lite-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtsvg-devel
BuildRequires: qt5-qttools-devel
BuildRequires: googletest-devel

Requires: openssl
Requires: pcsc-lite
Requires: pcsc-lite-ccid
Requires: qt5-qtbase
Requires: qt5-qtsvg
Requires: qt5-qtdeclarative
Requires: qt5-qttools

%description
The Web eID application performs cryptographic digital signing and authentication
operations with electronic ID smart cards for the Web eID browser extension (it
is the native messaging host for the extension). Also works standalone without
the extension in command-line mode.

%prep
%setup -q

%build
pushd web-eid-app
cmake -S . -B redhat-linux-build \
    -DCMAKE_C_FLAGS_RELEASE:STRING=-DNDEBUG \
    -DCMAKE_CXX_FLAGS_RELEASE:STRING=-DNDEBUG \
    -DCMAKE_Fortran_FLAGS_RELEASE:STRING=-DNDEBUG \
    -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
    -DCMAKE_INSTALL_DO_STRIP:BOOL=OFF \
    -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
    -DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \
    -DLIB_INSTALL_DIR:PATH=%{_libdir} \
    -DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \
    -DSHARE_INSTALL_PREFIX:PATH=%{_datadir} \
    -DLIB_SUFFIX=%{_lib} \
    -DBUILD_SHARED_LIBS:BOOL=ON
cmake --build redhat-linux-build -j2 --verbose
popd

%install
pushd web-eid-app
%cmake_install

%install
pushd web-eid-app
cmake --install redhat-linux-build --prefix "%{buildroot}%{_prefix}"

# Install Chrome/Chromium native messaging manifest files.
install -d -m 0755 %{buildroot}%{_sysconfdir}/chromium/native-messaging-hosts/
install -p -m 0644 %{buildroot}%{_datadir}/web-eid/eu.webeid.json %{buildroot}%{_sysconfdir}/chromium/native-messaging-hosts/eu.webeid.json

install -d -m 0755 %{buildroot}%{_sysconfdir}/opt/chrome/native-messaging-hosts/
install -p -m 0644 %{buildroot}%{_datadir}/web-eid/eu.webeid.json %{buildroot}%{_sysconfdir}/opt/chrome/native-messaging-hosts/eu.webeid.json

# Install Chromium extension manifest file.
install -d -m 0755 %{buildroot}%{_datadir}/chromium/extensions/
install -p -m 0644 %{buildroot}%{_datadir}/web-eid/ncibgoaomkmdpilpocfeponihegamlic.json %{buildroot}%{_datadir}/chromium/extensions/ncibgoaomkmdpilpocfeponihegamlic.json
popd

%check
pushd web-eid-app
export QT_QPA_PLATFORM=offscreen
ctest --test-dir redhat-linux-build --output-on-failure --force-new-ctest-process -j2
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
popd

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache-3.0 %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache-3.0 %{_datadir}/icons/hicolor &>/dev/null || :

%files
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_libdir}/mozilla/native-messaging-hosts/eu.webeid.json
%{_sysconfdir}/chromium/native-messaging-hosts/eu.webeid.json
%{_sysconfdir}/opt/chrome/native-messaging-hosts/eu.webeid.json
%{_datadir}/chromium/extensions/ncibgoaomkmdpilpocfeponihegamlic.json

%changelog
* Thu Nov 07 2024 Raiko Koosaar <koosaar@live.com> 2.6.0-1
- v2.6.0 release (koosaar@live.com)

* Thu Nov 07 2024 Raiko Koosaar <koosaar@live.com> 2.5.0-1
- v2.5.0 release (koosaar@live.com)

* Thu Nov 07 2024 Raiko Koosaar <koosaar@live.com> 2.4.0-2
- adding version 2.4.0-2 (koosaar@live.com)

* Thu Nov 07 2024 Raiko Koosaar <koosaar@live.com> 2.4.0-1
- adding version 2.4.0 (koosaar@live.com)
* Thu Nov 07 2024 Raiko Koosaar <koosaar@live.com> 2.3.1-1
- adding version 2.3.1 (koosaar@live.com)
- mozilla extensions missing (koosaar@live.com)
* Thu Nov 07 2024 Raiko Koosaar <koosaar@live.com> 2.3.0-1
- new package (2.3.0) built with tito

