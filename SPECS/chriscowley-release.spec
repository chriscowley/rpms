Name:           chriscowley-release       
Version:        0
Release:        1
Summary:        Chris Cowley's packages for Enterprise Linux repository configuration
Group:          System Environment/Base 
License:        GPLv2

URL:            http://yum.chriscowley.me.uk
Source0:        http://yum.chriscowley.me.uk/RPM-GPG-KEY-ChrisCowley
Source1:        GPL	
Source2:        chriscowley.repo

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:     noarch
Requires:     fedora-release

%if "%{distribution}" == "Fedora"
Requires:      fedora-release
%endif

%description
This package contains the the Chris Cowley repository
GPG key as well as configuration for Yum

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

%postun 


%files
%defattr(-,root,root,-)
%doc GPL
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/*


%changelog

* Wed Oct 17 2012 Chris Cowley <chris@chriscowley.me.uk> - 0.1
- Initial build

