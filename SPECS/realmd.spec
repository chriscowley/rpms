Name:		realmd
Version:	0.3
Release:	3%{?dist}
Summary:	Kerberos realm enrollment service
License:	LGPLv2+
URL:		http://cgit.freedesktop.org/~stefw/realmd/
Source0:	http://people.freedesktop.org/~stefw/source/realmd-0.3.tar.gz

BuildRequires:	intltool pkgconfig
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 2.22.0
BuildRequires:	PackageKit-glib-devel
BuildRequires:	polkit-devel
BuildRequires:	krb5-devel
Requires:	polkit

%description
realmd is a dbus system service which manages discovery and enrollment in realms
and domains like Active Directory or IPA. The control center uses realmd as the
backend to 'join' a domain simply and automatically configure things correctly.

%define _hardened_build 1

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%clean

%files
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.realmd.conf
%{_bindir}/realm-discover
%{_bindir}/realm-enroll
%dir %{_libdir}/realmd
%dir %{_libdir}/realmd/provider.d
%{_libdir}/realmd/net-ads-smb.conf
%{_libdir}/realmd/provider.d/org.freedesktop.realmd.Samba.provider
%{_libdir}/realmd/realmd
%{_libdir}/realmd/realmd-defaults.conf
%{_libdir}/realmd/realmd-distro.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.realmd.Samba.service
%{_datadir}/dbus-1/system-services/org.freedesktop.realmd.service
%{_datadir}/polkit-1/actions/org.freedesktop.realmd.policy
%doc AUTHORS COPYING ChangeLog NEWS README

%changelog
* Sat Jan 12 2013 Chris Cowley <chris@chriscowley.me.uk> - 0.3-3
- Rebuild for EPEL-6

* Tue Jun 19 2012 Stef Walter <stefw@redhat.com> - 0.3-2
- Add doc files
- Own directories
- Remove obsolete parts of spec file
- Remove explicit dependencies
- Updated License line to LGPLv2+

* Tue Jun 19 2012 Stef Walter <stefw@redhat.com> - 0.3
- Build fixes

* Mon Jun 18 2012 Stef Walter <stefw@redhat.com> - 0.2
- Initial RPM
