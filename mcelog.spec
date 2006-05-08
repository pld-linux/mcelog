Summary:	x86-64 Machine Check Exceptions collector and decoder
Name:		mcelog
Version:	0.7
Release:	0.1
License:	GPL v2
Group:		Applications/System
Source0:	ftp://ftp.x86-64.org/pub/linux/tools/mcelog/%{name}-%{version}.tar.gz
# Source0-md5:	21ba1a4d748c71c28f212ea57a7be7a1
Source1:	%{name}.logrotate
Patch0:		%{name}-DESTDIR.patch
Requires:	crondaemon
Requires:	logrotate
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mcelog decodes machine check events (hardware errors) on x86-64
machines running a 64-bit Linux kernel.

Starting with version 2.6.4, the Linux kernel for x86-64 no longer
decodes and logs recoverable Machine Check Exception events to the
kernel log on its own.

Instead, the MCE data is kept in a buffer which can be read from
userpace via the /dev/mcelog device node. You need this tool to
collect and decode those events; it will log the decoded MCE events
into /var/log/mcelog. Currently, mcelog can decode MCE from AMD K8 and
Intel P4 (including Xeon) processors.

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,/etc/{logrotate.d,cron.d},/var/log}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
cat <<'EOF' > $RPM_BUILD_ROOT/etc/cron.d/%{name}
0 * * * * root /usr/sbin/mcelog --ignorenodev --filter >> /var/log/mcelog
EOF
install %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES README
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) /etc/cron.d/mcelog
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/mcelog
%{_mandir}/man8/mcelog.8*
