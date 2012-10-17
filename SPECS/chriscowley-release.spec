%define is_fedora %(test -e /etc/fedora-release && echo 1 || echo 0)
%define is_el %(test -e /etc/redhat-release && echo 1 || echo 0)
%if %is_fedora
%define distribution Fedora
%endif
%if %is_el
%define distribution EL
%endif

Name:           chriscowley-release       
Version:        1
Release:        2
Summary:        Chris Cowley's packages for Enterprise Linux repository configuration

Group:          System Environment/Base 
License:        GPLv2

# This is a Red Hat maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.
URL:            http://yum.chriscowley.me.uk
Source0:        http://yum.chriscowley.me.uk/RPM-GPG-KEY-ChrisCowley
Source1:        GPL	
%if  "%{distribution}" == "EL"
Source2:        chriscowley.repo.el	
%endif
%if  "%{distribution}" == "Fedora"
Source2:        chriscowley.repo.fedora
%endif
#Source3:        epel-testing.repo	

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:     noarch
%if  "%{distribution}" == "EL"
Requires:      redhat-release >=  %{version} 
Conflicts:     fedora-release
%endif

%if "%{distribution}" == "Fedora"
Requires:      fedora-release
%endif

%description
This package contains the the Chris Cowley repository
GPG key as well as configuration for yum and up2date.

%prep
%setup -q  -c -T
install -pm 644 %{SOURCE0} .
install -pm 644 %{SOURCE1} .

%build


%install
rm -rf $RPM_BUILD_ROOT

#GPG Key
install -Dpm 644 %{SOURCE0} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-ChrisCowley

# yum
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%clean
rm -rf $RPM_BUILD_ROOT

%post
# Not needed for el6 as sources has been removed
#echo "# epel repo -- added by epel-release " \
#    >> %{_sysconfdir}/sysconfig/rhn/sources
#echo "yum epel http://download.fedora.redhat.com/pub/epel/%{version}/\$ARCH" \
#    >> %{_sysconfdir}/sysconfig/rhn/sources

%postun 
#sed -i '/^yum\ epel/d' %{_sysconfdir}/sysconfig/rhn/sources
#sed -i '/^\#\ epel\ repo\ /d' %{_sysconfdir}/sysconfig/rhn/sources


%files
%defattr(-,root,root,-)
%doc GPL
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/*


%changelog
* Sun Oct 23 2011 Chris Cowley <chris@chriscowley.me.uk> - 1-2
- Added test repository

* Sun Oct 23 2011 Chris Cowley <chris@chriscowley.me.uk> - 1-1
- Initial build

