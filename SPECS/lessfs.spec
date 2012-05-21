Name:		lessfs
Version:	1.5.12
Release:	1%{?dist}
Summary:	A high performance inline data deduplicating filesystem for Linux

Group:		System Environment/Kernel
License:	GPLv3
URL:		http://www.lessfs.com/
Source0:	http://sourceforge.net/projects/lessfs/files/lessfs/lessfs-${version}/lessfs-%{version}.tar.gz
Source1:    lessfs.cfg
Source2:    lessfs-init
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: gcc
BuildRequires: mhash-devel
BuildRequires: fuse-devel
BuildRequires: tokyocabinet-devel
Requires:	tokyocabinet

%description
A high performance inline data deduplicating filesystem for Linux.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p %{buildroot}/data
install -D %{SOURCE1} %{buildroot}%{_sysconfdir}/lessfs.cfg
install -D -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/init.d/lessfs


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_sysconfdir}/lessfs.cfg
%{_sysconfdir}/init.d/lessfs
%{_bindir}/lessfs
%{_sbindir}/lessfsck
%{_sbindir}/listdb
%{_sbindir}/mklessfs
%{_sbindir}/replogtool
%doc
%{_mandir}/man1/lessfs.1.gz
%{_mandir}/man1/replogtool.1.gz

%changelog
* Mon May 21 2012 Chris Cowley <chris@chriscowley.me.uk> - 1.5.12-1
- Updated to 1.5.12-1 and also now in git
* Fri Oct 7 2011 Chris Cowley <chris@chriscowley.me.uk> - 1.5.8-1
- 1st release
