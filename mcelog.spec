%define		subver	20130601
%define		rel	1
Summary:	x86-64/x86 Machine Check Exceptions collector and decoder
Summary(pl.UTF-8):	Narzędzie do zbierania i dekodowania wyjątków MCE na platformie x86-64/x86
Name:		mcelog
Version:	1.0
Release:	1.%{subver}.%{rel}
License:	GPL v2
Group:		Applications/System
#Source0:	http://www.kernel.org/pub/linux/utils/cpu/mce/%{name}-%{version}%{subver}.tar.gz
Source0:	https://github.com/andikleen/mcelog/tarball/master/%{name}-%{version}-%{subver}.tgz
# Source0-md5:	c48d3d3296ad0d5cbdf661e44375ea64
Source1:	%{name}.logrotate
Source2:	%{name}.cron
Source3:	%{name}.init
Source4:	%{name}.sysconfig
Patch1:		%{name}-FHS.patch
Patch2:		bashism.patch
URL:		https://github.com/andikleen/mcelog.git
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Suggests:	crondaemon
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		statdir		/var/lib/misc

%description
mcelog is the user space backend for logging machine check errors
reported by the hardware to the kernel. The kernel does the immediate
actions (like killing processes etc.) and mcelog decodes the logs the
errors.

Starting with version 2.6.4 for x86-64 and 2.6.32 for x86, the Linux
kernel no longer decodes and logs recoverable Machine Check Exception
events to the kernel log on its own. It is recommended that mcelog
runs on all those machines.

Instead, the MCE data is kept in a buffer which can be read from
userpace via the /dev/mcelog device node. You need this tool to
collect and decode those events; it will log the decoded MCE events
into /var/log/mcelog.

%description -l pl.UTF-8
mcelog to program do logowania błędów sprzętowych Machine Check
Exception zgłaszanych przez sprzęt (x86 i x86-64) do jądra. Jądro
podejmuje natychmiastowe akcje (takie jak odłączanie procesorów), a
mcelog dekoduje logi tych błędów.

Począwszy od wersji 2.6.4 dla x86-64 i 2.6.32 dla x86 jądro Linuksa
już samodzielnie nie dekoduje ani nie loguje niekrytycznych zdarzeń
MCE - zaleca się uruchamianie mceloga na tych wszystkich maszynach.

Zamiast logowania przez jądro, dane MCE są przechowywane w buforze,
który może być czytany z przestrzeni użytkownika poprzez urządzenie
/dev/mcelog. To narzędzie jest potrzebne do zbierania i dekodowania
tych zdarzeń; loguje ono zdekodowane zdarzenia MCE do /var/log/mcelog.

%prep
%setup -qc
mv andikleen-mcelog-*/* .
%patch1 -p1
%patch2 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fpie -pie"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig,{cron,logrotate}.d},/var/log,%{statdir}}

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	etcprefix=$RPM_BUILD_ROOT

cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.d/%{name}
cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
install -p %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

:> $RPM_BUILD_ROOT%{statdir}/memory-errors

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc CHANGES README TODO TODO-diskdb mce.pdf
%attr(755,root,root) %{_sbindir}/mcelog
%attr(640,root,root) /etc/cron.d/mcelog
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/mcelog
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.conf
# do replace on upgrade, in fact, these should be moved to /lib/mcelog as they
# all support foo.local invocation at the end
%attr(755,root,root) %config %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*-trigger
%attr(640,root,root) %ghost %{statdir}/memory-errors
%{_mandir}/man8/mcelog.8*
