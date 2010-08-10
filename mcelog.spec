%define		subver	pre3
Summary:	x86-64 Machine Check Exceptions collector and decoder
Summary(pl.UTF-8):	Narzędzie do zbierania i dekodowania wyjątków MCE na platformie x86-64
Name:		mcelog
Version:	1.0
Release:	0.%{subver}.1
License:	GPL v2
Group:		Applications/System
Source0:	http://www.kernel.org/pub/linux/utils/cpu/mce/%{name}-%{version}%{subver}.tar.gz
# Source0-md5:	b42f2214de6f4feb992556149edc67fa
Source1:	%{name}.logrotate
Source2:	%{name}.cron
Patch1:		%{name}-FHS.patch
Patch2:		manual.patch
Requires:	crondaemon
Requires:	logrotate
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		statdir		/var/lib/misc

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

%description -l pl.UTF-8
mcelog dekoduje zdarzenia Machine Check Exception (błędy sprzętowe) na
maszynach x86-64 pracujących pod kontrolą 64-bitowego jądra Linuksa.

Począwszy od wersji 2.6.4 jądro Linuksa dla x86-64 już samodzielnie
nie dekoduje ani nie loguje niekrytycznych zdarzeń MCE.

Zamiast tego dane MCE są przechowywane w buforze, który może być
czytany z przestrzeni użytkownika poprzez urządzenie /dev/mcelog. To
narzędzie jest potrzebne do zbierania i dekodowania tych zdarzeń;
loguje ono zdekodowane zdarzenia MCE do /var/log/mcelog. Aktualnie
mcelog potrafi dekodować MCE z procesorów AMD K8 i Intel P4 (w tym
Xeon).

%prep
%setup -q -n %{name}-%{version}%{subver}
%patch1 -p1
%patch2 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{cron,logrotate}.d,/var/log,%{statdir}}

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	etcprefix=$RPM_BUILD_ROOT

cp -a %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.d/%{name}
cp -a %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

:> $RPM_BUILD_ROOT%{statdir}/memory-errors

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES README TODO TODO-diskdb mce.pdf
%attr(755,root,root) %{_sbindir}/mcelog
%attr(640,root,root) /etc/cron.d/mcelog
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/mcelog
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}
%attr(640,root,root) %ghost %{statdir}/memory-errors
%{_mandir}/man8/mcelog.8*
