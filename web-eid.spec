%global _hardened_build 1
%define debug_package %{nil}

Name:    web-eid
Version: 2.6.0
Release: 1
Summary: Web eID browser extension helper application
License: MIT
URL:     https://github.com/web-eid/web-eid-app
Source0: %{name}-%{version}.tar.gz
# Source for the extension manifest
Source2:        %{name}-extension.json

BuildRequires: bash
BuildRequires: desktop-file-utils
BuildRequires: git
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtsvg-devel
BuildRequires: qt5-qttools-devel
BuildRequires: pcsc-lite
BuildRequires: pcsc-lite-devel
BuildRequires: clang
BuildRequires: git-clang-format
BuildRequires: valgrind
BuildRequires: gtest
BuildRequires: gtest-devel
BuildRequires: openssl-devel

Requires: hicolor-icon-theme
Requires: libstdc++
Requires: mozilla-filesystem
Requires: openssl-libs
Requires: pcsc-lite-libs
Requires: qt5-qtbase
Requires: qt5-qtsvg

%description
The Web eID application performs cryptographic digital signing and authentication
operations with electronic ID smart cards for the Web eID browser extension (it
is the native messaging host for the extension). Also works standalone without
the extension in command-line mode.

%prep
%autosetup -n %{name}-app-%{version}
# Rename the extension manifest to the correct name
cp ../%{name}-extension.json ncibgoaomkmdpilpocfeponihegamlic.json

%build
pushd web-eid-app
%cmake
%cmake_build
popd

%install
pushd web-eid-app
%cmake_install

# Remove the eu.webeid.json file that cmake installs, as we're installing it separately
rm -f %{buildroot}%{_datadir}/web-eid/eu.webeid.json

# Install native messaging manifests for Chrome/Chromium
install -m 644 -Dt %{buildroot}%{_sysconfdir}/chromium/native-messaging-hosts/ %{buildroot}%{_datadir}/web-eid/eu.webeid.json
install -m 644 -Dt %{buildroot}%{_sysconfdir}/opt/chrome/native-messaging-hosts/ %{buildroot}%{_datadir}/web-eid/eu.webeid.json

# Install extension manifest for Chromium (Chrome uses a different path)
install -m 644 -Dt %{buildroot}%{_datadir}/chromium/extensions ncibgoaomkmdpilpocfeponihegamlic.json
popd

%check
pushd web-eid-app
export QT_QPA_PLATFORM='offscreen' # needed for running headless tests
%ctest
popd

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%license LICENSE.md
%doc README.md
%{_bindir}/%{name}
%{_libdir}/mozilla/native-messaging-hosts/eu.webeid.json
%{_datadir}/web-eid/eu.webeid.json
%dir %{_sysconfdir}/chromium/native-messaging-hosts/
%{_sysconfdir}/chromium/native-messaging-hosts/eu.webeid.json
%dir %{_sysconfdir}/opt/chrome/native-messaging-hosts/
%{_sysconfdir}/opt/chrome/native-messaging-hosts/eu.webeid.json
%dir %{_datadir}/chromium/extensions/
%{_datadir}/chromium/extensions/ncibgoaomkmdpilpocfeponihegamlic.json
%{_datadir}/google-chrome/extensions/ncibgoaomkmdpilpocfeponihegamlic.json
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

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

