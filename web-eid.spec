%global _hardened_build 1
%define debug_package %{nil}

Name:    web-eid
Version: 2.6.0
Release: 10%{?dist}
Summary: Web eID browser extension helper application
License: MIT
URL:     https://github.com/web-eid/web-eid-app
Source0: %{name}-%{version}.tar.gz
Patch0: 126.patch

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
%autosetup -p1

%build
pushd web-eid-app
%cmake
%cmake_build

%install
pushd web-eid-app
%cmake_install

install -m 644 -Dt %{buildroot}/%{_sysconfdir}/chromium/native-messaging-hosts %{buildroot}/%{_datadir}/web-eid/eu.webeid.json
install -m 644 -Dt %{buildroot}/%{_sysconfdir}/opt/chrome/native-messaging-hosts %{buildroot}/%{_datadir}/web-eid/eu.webeid.json


# # Install Chrome/Chromium native messaging manifest files.
# # Create the destination directories
# install -d -m 0755 %{buildroot}%{_sysconfdir}/chromium/native-messaging-hosts/
# install -d -m 0755 %{buildroot}%{_sysconfdir}/opt/chrome/native-messaging-hosts/

# # Copy the manifest files from the build directory
# install -p -m 0644 %{buildroot}%{_datadir}/web-eid/eu.webeid.json %{buildroot}%{_sysconfdir}/chromium/native-messaging-hosts/
# install -p -m 0644 %{buildroot}%{_datadir}/web-eid/eu.webeid.json %{buildroot}%{_sysconfdir}/opt/chrome/native-messaging-hosts/

# # Install Chromium extension manifest file.
# # Create the destination directory
# install -d -m 0755 %{buildroot}/%{_datadir}/chromium/extensions/

# # Copy the manifest file from the build directory
# install -p -m 0644 redhat-linux-build/ncibgoaomkmdpilpocfeponihegamlic.json %{buildroot}/%{_datadir}/chromium/extensions/

#    /usr/share/chromium/extensions/ncibgoaomkmdpilpocfeponihegamlic.json
#    -- Installing: /builddir/build/BUILD/web-eid-2.6.0-build/BUILDROOT/usr/share/chromium/extensions/ncibgoaomkmdpilpocfeponihegamlic.json

# Remove the temporarily installed eu.webeid.json file from the standard install location.
rm -f %{buildroot}%{_datadir}/web-eid/eu.webeid.json

# rm -f %{buildroot}/%{_datadir}/web-eid/eu.webeid.json
# rm -f %{buildroot}%{_sysconfdir}/opt/chrome/native-messaging-hosts/eu.webeid.json
# rm -f %{buildroot}%{_sysconfdir}/usr/etc/chromium/native-messaging-hosts/eu.webeid.json
popd


%check
pushd web-eid-app
export QT_QPA_PLATFORM='offscreen' # needed for running headless tests
%ctest

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

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
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_sysconfdir}/chromium/native-messaging-hosts/
%{_sysconfdir}/opt/chrome/native-messaging-hosts/
%{_libdir}/mozilla/native-messaging-hosts/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/google-chrome/extensions/
%{_datadir}/icons/hicolor/*/apps/%{name}.png
# Ugly hack - I have to put in absolute paths as the above ones are not working for some reason.
/usr/etc/chromium/native-messaging-hosts/eu.webeid.json
/usr/etc/opt/chrome/native-messaging-hosts/eu.webeid.json
/usr/share/chromium/extensions/ncibgoaomkmdpilpocfeponihegamlic.json

%changelog
* Mon Jun 16 2025 Raiko Koosaar <koosaar@live.com> 2.6.0-10
- fix patch 126 fix (koosaar@live.com)

* Mon Jun 16 2025 Raiko Koosaar <koosaar@live.com> 2.6.0-9
- patch 126 fix fix fix (koosaar@live.com)

* Mon Jun 16 2025 Raiko Koosaar <koosaar@live.com> 2.6.0-8
- patch 126 fix fix (koosaar@live.com)

* Mon Jun 16 2025 Raiko Koosaar <koosaar@live.com> 2.6.0-7
- patch 126 fix (koosaar@live.com)

* Mon Jun 16 2025 Raiko Koosaar <koosaar@live.com> 2.6.0-6
- patch 126 (koosaar@live.com)

* Mon Jun 16 2025 Raiko Koosaar <koosaar@live.com> 2.6.0-5
- adding patch 126

* Mon Jun 16 2025 Raiko Koosaar <koosaar@live.com> 2.6.0-4
- Rolling back the .patch

* Mon Jun 16 2025 Raiko Koosaar <koosaar@live.com> 2.6.0-3
- Fix: Add cstdint fix patch to be applied via autosetup (koosaar@live.com)
* Mon Jun 16 2025 Raiko Koosaar <koosaar@live.com>
- Fix: Add cstdint fix patch to be applied via autosetup (koosaar@live.com)
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

