# Binary package, no debuginfo should be generated
%global debug_package %{nil}
# Avoid binary manipulation or the main executable gets corrupted
%global __spec_install_post /usr/lib/rpm/brp-compress

Name:           skype
Version:        4.3.0.37
Release:        4%{?dist}
Summary:        Skype Messaging and Telephony Client

License:        Skype End User License Agreement
URL:            http://www.skype.com/products/skype/linux/
# Download at:
# http://www.skype.com/go/getskype-linux-beta-dynamic
Source0:        http://download.skype.com/linux/%{name}-%{version}.tar.bz2

%if 0%{?fedora} == 24 || 0%{?fedora} == 23 || 0%{?rhel}
BuildRequires:  desktop-file-utils
%endif

Requires:       hicolor-icon-theme
Requires:       %{name}-data = %{version}-%{release}
# Needed for the welcome screen, not pulled in by dependencies
Requires:       webkitgtk%{_isa}
# Loaded at runtime
Requires:       pulseaudio-libs%{_isa}

ExclusiveArch:  %{ix86}

%description
Millions of individuals and businesses use Skype to make free video and voice
calls, send instant messages and share files with other Skype users. Everyday,
people also use Skype to make low-cost calls to landlines and mobiles.

%package data
Summary:        Skype Messaging and Telephony Client data files
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description data
This package contains icons, sounds and support files for the main Skype
package.

%prep
%setup -q

sed -i 's/\r$//' LICENSE

%build
# Nothing to build

%install
mkdir -p %{buildroot}%{_sysconfdir}/prelink.conf.d/

install -p -D -m 655 %{name} %{buildroot}%{_bindir}/%{name}
echo "-b %{_bindir}/skype" > %{buildroot}%{_sysconfdir}/prelink.conf.d/%{name}-%{_arch}.conf

install -p -D -m 644 %{name}.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/%{name}.conf

for size in 16 24 32 48 64 96 128 256; do
    install -p -D -m 644 icons/SkypeBlue_${size}x${size}.png \
        %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{name}.png
done

mkdir -p %{buildroot}%{_datadir}/%{name}
cp -afr sounds avatars lang %{buildroot}%{_datadir}/%{name}

sed -i -e 's/.png//g' %{name}.desktop
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{name}.desktop

%post data
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
%if 0%{?fedora} == 24 || 0%{?fedora} == 23 || 0%{?rhel}
%{_bindir}/update-desktop-database &> /dev/null || :
%endif

%postun data
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
%if 0%{?fedora} == 24 || 0%{?fedora} == 23 || 0%{?rhel}
%{_bindir}/update-desktop-database &> /dev/null || :
%endif

%posttrans data
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
# Always replace the prelink information, the binary gets corrupted otherwise
%config %{_sysconfdir}/prelink.conf.d/%{name}-%{_arch}.conf
%{_bindir}/%{name}

%files data
%doc LICENSE README third-party_attributions.txt
# DBus information comes from upstream
%config %{_sysconfdir}/dbus-1/system.d/%{name}.conf
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/%{name}

%changelog
* Fri Nov 04 2016 Simone Caronni <negativo17@gmail.com> - 4.3.0.37-4
- Do not run update-desktop-database on Fedora 25 as per packaging guidelines.

* Wed Jan 07 2015 Simone Caronni <negativo17@gmail.com> - 4.3.0.37-3
- Add pulseaudio libraries as requirement. Not linked from main executable but
  loaded at runtime.

* Tue Aug 26 2014 Simone Caronni <negativo17@gmail.com> - 4.3.0.37-2
- Latency fix no longer required.

* Wed Jun 18 2014 Simone Caronni <negativo17@gmail.com> - 4.3.0.37-1
- Update to 4.3.0.37.

* Mon May 19 2014 Simone Caronni <negativo17@gmail.com> - 4.2.0.13-3
- Allow command line parameters to be passed to wrapper.

* Wed May 14 2014 Simone Caronni <negativo17@gmail.com> - 4.2.0.13-2
- Fix desktop file Exec line.

* Wed Jan 29 2014 Simone Caronni <negativo17@gmail.com> - 4.2.0.13-1
- Updated to 4.2.0.13.

* Wed Nov 20 2013 Simone Caronni <negativo17@gmail.com> - 4.2.0.11-8
- Split main executable from data files (preparation for x86_64 binaries).

* Wed Nov 6 2013 Alec Leamas <leamas@nowhere.net>  - 4.2.0.11-7
- Importing spec from rpmfusion #2978 into lpf-skype package.
- Kudos Simone Caronni for writing that spec!
- Generate skype-wrapper in the spec file.
- Add -a to cp command.

* Mon Oct 21 2013 Simone Caronni <negativo17@gmail.com> - 4.2.0.11-6
- Add webkitgtk as requirement; it's required by the welcome screen and not
  pulled in automatically.

* Thu Oct 10 2013 Simone Caronni <negativo17@gmail.com> - 4.2.0.11-5
- Convert the profile to wrapper for Fedora 20.

* Tue Oct 08 2013 Simone Caronni <negativo17@gmail.com> - 4.2.0.11-4
- Force PulseAudio latency in Fedora 20+ through an alias to the skype command
  in /etc/profile.d/.

* Fri Sep 20 2013 Simone Caronni <negativo17@gmail.com> - 4.2.0.11-3
- Rpmlint fixes.

* Tue May 21 2013 Simone Caronni <negativo17@gmail.com> - 4.2.0.11-2
- Added new icon sizes.

* Mon May 20 2013 Simone Caronni <negativo17@gmail.com> - 4.2.0.11-1
- Update to 4.2.0.11.

* Thu Nov 15 2012 Simone Caronni <negativo17@gmail.com> - 4.1.0.20-1
- Updated to 4.1.0.20.

* Thu Sep 06 2012 Simone Caronni <negativo17@gmail.com> - 4.0.0.8-1
- Updated to 4.0.0.8.

* Thu Feb 16 2012 Simone Caronni <negativo17@gmail.com> - 2.2.0.35-3
- Removed main binary from prelinking.

* Thu Feb 09 2012 Simone Caronni <negativo17@gmail.com> - 2.2.0.35-2
- Do not strip debuginfo.

* Tue Dec 20 2011 Simone Caronni <negativo17@gmail.com> - 2.2.0.35-1
- First build.

