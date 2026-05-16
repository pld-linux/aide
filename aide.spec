Summary:	Advanced Intrusion Detection Environment
Summary(pl.UTF-8):	Zaawansowany System Wykrywania Włamań (AIDE)
Summary(pt_BR.UTF-8):	AIDE - ferramenta de verificação de integridade do sistema
Name:		aide
Version:	0.19.3
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	https://github.com/aide/aide/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4129c3250f1cd8437ab59f35a427956e
Source1:	%{name}.conf
Source3:	%{name}-check
Source4:	%{name}.sysconfig
URL:		https://aide.github.io/
BuildRequires:	autoconf
BuildRequires:	autoconf-archive
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	e2fsprogs-devel
BuildRequires:	flex
BuildRequires:	gettext-tools
BuildRequires:	acl-devel
BuildRequires:	attr-devel
BuildRequires:	libcap-devel
BuildRequires:	libselinux-devel
BuildRequires:	nettle-devel >= 3.7
BuildRequires:	pcre2-8-devel
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
Requires:	crondaemon
Requires:	grep
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		_pkglibdir	/var/lib/%{name}

%description
AIDE creates a database from the regular expression rules that it
finds from the config file. Once this database is initialized it can
be used to verify the integrity of the files. It has several message
digest algorithms (md5,sha1,rmd160,tiger,haval,etc.) that are used to
check the integrity of the file. More algorithms can be added with
relative ease. All of the usual file attributes can also be checked
for inconsistencies.

%description -l pl.UTF-8
AIDE tworzy bazę danych z wyrażeń regularnych, które znajdują się w
pliku konfiguracyjnym. Gdy baza zostanie zainicjowana można sprawdzać
integralność plików. Używanych jest kilka algorytmów sprawdzania
spójności (md5,sha1,rmd160,tiger,haval,itp.). Inne mogą być dodane
stosunkowo łatwo. Zwykłe atrybuty plików także mogą być sprawdzane.

%description -l pt_BR.UTF-8
O AIDE tem por objetivo ser a versão gratuita do Tripwire, e ajuda a
detectar violações de integridade pelo uso de hashes como MD5.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-config-file=%{_sysconfdir}/aide.conf
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_pkglibdir},/etc/cron.daily,/etc/sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/cron.daily/aide-check
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/aide

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(750,root,root) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/aide.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/aide
%attr(750,root,root) %dir %{_pkglibdir}
%attr(755,root,root) %{_bindir}/aide
%attr(700,root,root) %config(noreplace) /etc/cron.daily/aide-check
%{_mandir}/man[15]/*
