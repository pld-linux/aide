Summary:	Advanced Intrusion Detection Environment
Summary(pl):	Zaawansowany System Wykrywania W�ama� (AIDE)
Summary(pt_BR):	AIDE - ferramenta de verifica��o de integridade do sistema
Name:		aide
Version:	0.10
Release:	2
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	39eb7d21064cac7b409c45d038b86cd8
Source1:	%{name}.conf
Source2:	%{name}-0.7-doc.tar.bz2
# Source2-md5:	f8d01112f839957b3061bb6b5f262174
Source3:	%{name}-check
Source4:	%{name}.sysconfig
Patch0:		%{name}-autoconf.patch
Patch1:		%{name}-NLS.patch
Patch2:		%{name}-ac_fix.patch
Patch3:		%{name}-no_md.patch
Patch4:		%{name}-language-ru.patch
URL:		http://www.cs.tut.fi/~rammer/aide.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	findutils
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	glibc-static
BuildRequires:	mhash-static
BuildRequires:	perl-modules
BuildRequires:	zlib-static >= 1.1.4
Requires:	crondaemon
Requires:	grep
Requires:	mailx
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

%description -l pl
AIDE tworzy baz� danych z wyra�e� regularnych, kt�re znajduj� si� w
pliku konfiguracyjnym. Gdy baza zostanie zainicjowana mo�na sprawdza�
integralno�� plik�w. U�ywanych jest kilka algorytm�w sprawdzania
sp�jno�ci (md5,sha1,rmd160,tiger,haval,itp.). Inne mog� by� dodane
stosunkowo �atwo. Zwyk�e atrybuty plik�w tak�e mog� by� sprawdzane.

%description -l pt_BR
O AIDE tem por objetivo ser a vers�o gratuita do Tripwire, e ajuda
a detectar viola��es de integridade pelo uso de hashes como MD5.

%prep
%setup -q -b 0 -a 2
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
rm -f missing po/Makefile*
find . -name "*.c" -type f > po/POTFILES.in

%{__gettextize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-config-file=%{_sysconfdir}/aide.conf
#	--with-extra-includes=/usr/include/
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_pkglibdir},/etc/cron.daily,/etc/sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/cron.daily
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/aide

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README doc/aide.conf doc/manual.html aide-*/doc/aide.html
%attr(750,root,root) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/aide.conf
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/aide
%attr(750,root,root) %dir %{_pkglibdir}
%attr(755,root,root) %{_bindir}/aide
%attr(700,root,root) %config(noreplace) /etc/cron.daily/aide-check
%{_mandir}/man[15]/*
