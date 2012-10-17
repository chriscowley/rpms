Name:		lessfs
Version:	1.5.12
Release:	2%{?dist}
Summary:	A high performance inline data deduplicating filesystem for Linux

Group:		System Environment/Kernel
License:	GPLv3+
URL:		http://www.lessfs.com/
Source0:	http://sourceforge.net/projects/lessfs/files/lessfs/lessfs-%{version}/lessfs-%{version}.tar.gz
Source1:    lessfs.cfg
#Source2:    lessfs-init
Source2:    lessfs.service
Source3:    lessfs.syscfg

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: mhash-devel
BuildRequires: fuse-devel
BuildRequires: tokyocabinet-devel
BuildRequires: systemd-units


%description
A high performance inline data deduplicating filesystem for Linux.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
mkdir -p %{RPM_BUILD_ROOT}/lessfs
install -D %{SOURCE1} %{buildroot}%{_sysconfdir}/lessfs.cfg
install -D -m 755 %{SOURCE2} %{buildroot}%{_unitdir}/lessfs.service


%clean
rm -rf $RPM_BUILD_ROOT


%pre
getent group lessfs  >/dev/null || groupadd -r lessfs
getent passwd lessfs > /dev/null || \
	useradd -r -g lessfs -d %{_localstatedir}/lib/%{name} -s /sbin/nologin \
	-c "LessFS de-duplicated Filesystem" lessfs
exit 0

%post
if [ "$1" -eq "1" ]; then 
	        /sbin/chkconfig --add %{name}
else
	chown -R lessfs.lessfs %{_localstatedir}/lib/%{name} > /dev/null 2>&1 ||:
fi

%files
%defattr(-,root,root,-)
%{_sysconfdir}/lessfs.cfg
%{_unitdir}/lessfs.service
%{_bindir}/lessfs
%{_sbindir}/lessfsck
%{_sbindir}/listdb
%{_sbindir}/mklessfs
%{_sbindir}/replogtool
%doc
%{_mandir}/man1/lessfs.1.gz
%{_mandir}/man1/replogtool.1.gz

%changelog
* Mon Oct 14 2012 Chris Cowley <chris@chriscowley.me.uk> - 1.5.12-2
- Updated to use Systemd instead of SysV.
- Refactored to better match packaging guidelines
* Mon May 21 2012 Chris Cowley <chris@chriscowley.me.uk> - 1.5.12-1
- Updated to 1.5.12-1
* Fri Oct 7 2011 Chris Cowley <chris@chriscowley.me.uk> - 1.5.8-1
- 1st release
