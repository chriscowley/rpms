%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:           graphite-web
Version:        0.9.12
Release:        5%{?dist}
Summary:        A Django webapp for enterprise scalable realtime graphing
Group:          Applications/Internet

License:        ASL 2.0
URL:            https://launchpad.net/graphite/
Source0:        https://github.com/graphite-project/graphite-web/archive/0.9.12.tar.gz#/%{name}-%{version}.tar.gz
Source1:        graphite-web-vhost.conf
Source2:        graphite-web-README.fedora
Source3:        graphite-web-README.selinux
Patch0:         graphite-web-0.9.12-fhs-thirdparty.patch
Patch1:         graphite-web-0.9.12-dashboard-load.patch
Patch2:         graphite-web-0.9.12-carbonlink-exception-log.patch
Patch3:         graphite-web-0.9.12-safe-unpickle-deque-addition.patch
BuildRoot:      %{_tmppath}/graphite-web-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
Requires:       python-whisper >= %{version}, mod_wsgi, pytz, pyparsing, python-simplejson
Requires:       dejavu-sans-fonts, dejavu-serif-fonts, pycairo, django-tagging

%if 0%{?fedora} >= 18
Requires:       python-django >= 1.3
%else
Requires:       Django >= 1.3
%endif

%if 0%{?el5}
Requires:       python-sqlite2
%endif


%description
Graphite consists of a storage backend and a web-based visualization frontend.
Client applications send streams of numeric time-series data to the Graphite
backend (called carbon), where it gets stored in fixed-size database files
similar in design to RRD. The web frontend provides user interfaces
for visualizing this data in graphs as well as a simple URL-based API for
direct graph generation.

Graphite's design is focused on providing simple interfaces (both to users and
applications), real-time visualization, high-availability, and enterprise
scalability.


%package selinux
Summary:        SELinux labeling for graphite files
Group:          Applications/Internet
Requires:       %name = %version-%release
%if 0%{?el5}
Requires(post): policycoreutils
Requires(postun): policycoreutils
%else
Requires(post): policycoreutils-python
Requires(postun): policycoreutils-python
%endif


%description selinux
SELinux labeling for graphite files.


%prep
%setup -q -n graphite-web-%{version}
# Patch for Filesystem Hierarchy Standard
# Remove thridparty libs
%patch0 -p1
# Fix loading dashboards by name (https://github.com/graphite-project/graphite-web/issues/411)
%patch1 -p1
# Log name of metric that throws exception for CarbonLink (https://github.com/graphite-project/graphite-web/pull/446)
%patch2 -p1
# Add deque to the PICKLE_SAFE filter (https://github.com/graphite-project/graphite-web/issues/423)
%patch3 -p1
%{__install} -m 644 %{SOURCE2} README.fedora
%{__install} -m 644 %{SOURCE3} README.selinux


%build
%{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Create directories 
%{__mkdir_p} %{buildroot}%{_localstatedir}/lib/graphite-web
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/graphite-web
%{__mkdir_p} %{buildroot}%{_sysconfdir}/graphite-web

# Install some default configurations and wsgi
%{__install} -Dp -m0644 conf/dashboard.conf.example %{buildroot}%{_sysconfdir}/graphite-web/dashboard.conf
%{__install} -Dp -m0644 webapp/graphite/local_settings.py.example %{buildroot}%{_sysconfdir}/graphite-web/local_settings.py
%{__install} -Dp -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/graphite-web.conf

%if 0%{?el5}
%{__install} -Dp -m0644 conf/graphite.wsgi.example %{buildroot}%{_datadir}/graphite/graphite-web.wsgi
%else
%{__install} -Dp -m0644 conf/graphite.wsgi.example %{buildroot}%{_datarootdir}/graphite/graphite-web.wsgi
%endif

# Configure django /media/ location
sed -i 's|##PYTHON_SITELIB##|%{python_sitelib}|' %{buildroot}%{_sysconfdir}/httpd/conf.d/graphite-web.conf

# Create local_settings symlink
pushd %{buildroot}%{python_sitelib}/graphite
%{__ln_s} %{_sysconfdir}/graphite-web/local_settings.py
popd

# Don't ship bins that are not needed for prodcution
%{__rm} %{buildroot}%{_bindir}/{build-index.sh,run-graphite-devel-server.py}

# Fix permissions
%{__chmod} 0644 conf/graphite.wsgi.example
%{__chmod} 0755 %{buildroot}%{python_sitelib}/graphite/manage.py

%if 0%{?el5}
%{__chmod} 0644 %{buildroot}%{_datadir}/graphite/webapp/content/js/window/*
%else
%{__chmod} 0644 %{buildroot}%{_datarootdir}/graphite/webapp/content/js/window/*
%endif


# Don't ship thirdparty
%{__rm} -rf %{buildroot}%{python_sitelib}/graphite/thirdparty

# Don't ship js/ext/resources/*.swf
%{__rm} -rf %{buildroot}%{_datarootdir}/graphite/webapp/content/js/ext/resources/*.swf


%post selinux
semanage fcontext -a -t httpd_sys_content_t '%{_localstatedir}/lib/graphite-web(/.*)?' 2>/dev/null || :
restorecon -R %{_localstatedir}/lib/graphite-web || :


%postun selinux
if [ $1 -eq 0 ] ; then
semanage fcontext -d -t httpd_sys_content_t '%{_localstatedir}/lib/graphite-web(/.*)?' 2>/dev/null || :
fi


%files
%doc README.fedora LICENSE conf/* examples/*
%{python_sitelib}/graphite*

%config(noreplace) %{_sysconfdir}/httpd/conf.d/graphite-web.conf
%config(noreplace) %{_sysconfdir}/graphite-web/local_settings.py
%ghost %{_sysconfdir}/graphite-web/local_settings.pyc
%ghost %{_sysconfdir}/graphite-web/local_settings.pyo
%config(noreplace) %{_sysconfdir}/graphite-web/dashboard.conf
%attr(-,apache,apache) %dir %{_localstatedir}/log/graphite-web

%if 0%{?el5}
%{_datadir}/graphite
%attr(-,apache,apache) %dir %{_localstatedir}/lib/graphite-web
%else
%{_datarootdir}/graphite
%attr(-,apache,apache) %dir %{_sharedstatedir}/graphite-web
%endif

%files selinux
%doc README.selinux

%changelog
* Tue Oct 01 2013 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.12-5
- Patch for fix loading dashboards by name (RHBZ#1014349)
- Patch for log name of metric that throws exception for CarbonLink (RHBZ#1014349)
- Add deque to the PICKLE_SAFE filter (RHBZ#1014356)
- Merge in EL5 conditionals for single spec

* Mon Sep 30 2013 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.12-4
- Remove logrotate configuration as it conflicts with internal
  log rotation (RHBZ#1008616)

* Tue Sep 24 2013 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.12-3
- Reorder Requires conditionals to fix amzn1 issues (RHBZ#1007300)
- Ensure python-whisper is also updated

* Tue Sep 17 2013 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.12-2
- Don't ship js/ext/resources/*.swf (RHBZ#1000253)

* Mon Sep 02 2013 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.12-1
- Update to 0.9.12
- Require Django >= 1.3
- Add EL5 conditional for SELinux policycoreutils

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.10-7
- Update required fonts to actually include fonts (RHBZ#917361)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 30 2012 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.10-5
- Conditionally require python-sqlite2
- Conditionally require new Django namespace

* Sat Dec 29 2012 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.10-4
- Update to use mod_wsgi
- Update vhost configuration file to correctly work on multiple python
  versions

* Sat Nov 24 2012 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.10-3
- Address all rpmlint errors
- Add SELinux subpackage README
- Patch out thirdparty code, Require it instead

* Fri Nov 09 2012 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.10-2
- Add logrotate

* Thu May 31 2012 Jonathan Steffan <jsteffan@fedoraproject.org> - 0.9.10-1
- Initial Package
